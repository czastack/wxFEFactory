#ifdef _WIN32

#include <wx/wx.h>
#include "wx/wxtypes.h"
#include "../pyutils.h"
#include "../functions.h"
#include "emuhacker.h"
#include "ProcessHandler.h"
#include <windows.h>
#include <psapi.h>
#include <tuple>


namespace emuhacker {
	auto read_ptr(ProcessHandler &self, addr_t addr) { return self.read_uint(addr, self.getPtrSize()); }
	bool write_ptr(ProcessHandler &self, addr_t addr, size_t data) { return self.write_uint(addr, data, self.getPtrSize()); }


	pyobj process_read(ProcessHandler &self, addr_t addr, pycref type, size_t size)
	{
		if (type.ptr() == (PyObject*)&PyLong_Type)
		{
			size_t data = self.read_uint(addr, size ? size : self.getPtrSize());
			return py::cast(data);
		}
		else if (type.ptr() == (PyObject*)&PyFloat_Type)
		{
			if (size == 8)
				return py::cast(self.read<double>(addr));
			return py::cast(self.read<float>(addr));
		}
		else if (type.ptr() == (PyObject*)&PyBool_Type)
		{
			return py::cast(self.read<bool>(addr));
		}
		else if (size)
		{
			char *buf = new char[size];
			self.read(addr, buf, size);
			py::bytes ret(buf, size);
			delete[] buf;
			return ret;
		}
		return None;
	}


	bool process_write(ProcessHandler &self, addr_t addr, pycref data, size_t size)
	{
		if (PyLong_Check(data.ptr()))
		{
			return self.write_uint(addr, data.cast<size_t>(), size ? size : self.getPtrSize());
		}
		else if (PyFloat_Check(data.ptr()))
		{
			if (size == 8)
				return self.write(addr, data.cast<double>());
			return self.write(addr, data.cast<float>());
		}
		else if (PyBool_Check(data.ptr()))
		{
			return self.write(addr, data.cast<bool>());
		}
		else if (PyBytes_Check(data.ptr()))
		{
			if (size == 0)
				size = PyBytes_Size(data.ptr());
			return self.write(addr, PyBytesGetBuff(data), size);
		}
		else if (PyByteArray_Check(data.ptr()))
		{
			if (size == 0)
				size = PyByteArray_Size(data.ptr());
			return self.write(addr, PyByteArray_AsString(data.ptr()), size);
		}

		return false;
	}


	addr_t read_last_addr(ProcessHandler &self, addr_t addr, py::iterable &args)
	{
		wxArrayInt offsets = py::cast<wxArrayInt>(args);
		return self.read_last_addr(addr, offsets);
	}

	auto alloc_data(ProcessHandler &self, py::bytes buf, size_t start) {
		char *buff;
		ssize_t size;
		PyBytes_AsStringAndSize(buf.ptr(), &buff, &size);
		return self.alloc_data(buff, size, start);
	}

	auto write_function(ProcessHandler &self, py::bytes buf, size_t start) {
		// 申请的内存可执行
		char *buff;
		ssize_t size;
		PyBytes_AsStringAndSize(buf.ptr(), &buff, &size);
		return self.write_function(buff, size, start);
	}

	pyobj find_bytes(ProcessHandler &self, py::bytes buf, addr_t start, addr_t end, int ordinal, bool fuzzy)
	{
		char *buff;
		ssize_t size;
		PyBytes_AsStringAndSize(buf.ptr(), &buff, &size);
		addr_t result = self.find_bytes((BYTE*)buff, size, start, end, ordinal, fuzzy);
		if (result != -1)
		{
			return py::int_(result);
		}
		return py::int_(-1);
	}

	wxString getModuleFile(ProcessHandler &self, addr_t module = 0)
	{
		wxChar buff[MAX_PATH];
		if (module == 0)
		{
			module = self.getProcessBaseAddress();
		}
		DWORD result = GetModuleFileNameEx(self.getProcess(), (HMODULE)module, buff, sizeof(buff) / sizeof(wxChar));
		if (result)
		{
			return wxString(buff, result);
		}
		return wxNoneString;
	}

	py::tuple getModuleVersion(ProcessHandler &self)
	{
		DWORD dwInfoSize, dwHandle;
		wxcstr path = getModuleFile(self);
		dwInfoSize = ::GetFileVersionInfoSize(path, &dwHandle);
		wxChar* pData = new wxChar[dwInfoSize];
		void *lpBuffer;
		UINT uLength;
		py::tuple result(2);

		GetFileVersionInfo(path, NULL, dwInfoSize, (LPVOID)pData);
		if (VerQueryValue((LPCVOID)pData, _T("\\"), &lpBuffer, &uLength))
		{
			VS_FIXEDFILEINFO *pFileInfo = (VS_FIXEDFILEINFO*)lpBuffer;
			result[0] = pFileInfo->dwProductVersionMS;
			result[1] = pFileInfo->dwProductVersionLS;
		}
		return result;
	}

	BOOL CALLBACK _enum_window(HWND hWnd, LPARAM lParam)
	{
		TCHAR szWindowName[64];
		DWORD cchWindowName;
		BOOL  bContinue = TRUE;

		cchWindowName = GetWindowText(hWnd, szWindowName, 64);
		auto &pArgs = *(std::tuple<pycref, wxChar*, Py_ssize_t>*)lParam;
		wxChar* prefix = std::get<1>(pArgs);
		if (!prefix || wcsncmp(szWindowName, prefix, std::get<2>(pArgs)) == 0)
		{
			py::object ret = PyCall(std::get<0>(pArgs), (LPARAM)hWnd, szWindowName);
			return PyObject_IsTrue(ret.ptr());
		}
		return TRUE;
	}

	void enum_windows(ProcessHandler &self, pycref callback, pycref prefix)
	{
		Py_ssize_t prefix_len = 0;
		wxChar *title_prefix = prefix.is_none() ? nullptr : PyUnicode_AsWideCharString(prefix.ptr(), &prefix_len);
		std::tuple<pycref, wxChar*, Py_ssize_t> args(callback, title_prefix, prefix_len);
		EnumWindows(_enum_window, reinterpret_cast<LPARAM>(&args));
		if (title_prefix)
		{
			PyMem_Free(title_prefix);
		}
	}

	bool attach_handle(ProcessHandler &self, size_t hWnd)
	{
		return self.attach_handle((HWND)hWnd);
	}

	wxString getWindowText(ProcessHandler& self) {
		HWND hWnd = self.getHWnd();
		if (hWnd)
		{
			wxChar buff[128];
			int result = ::GetWindowText(hWnd, buff, 128);
			if (result) {
				return wxString(buff, result);
			}
		}
		return wxNoneString;
	}

	pyobj getProcAddress(ProcAddressHelper& self, pycref data)
	{
		if (PyUnicode_Check(data.ptr()))
		{
			// 直接返回函数地址
			wxArrayString name_list;
			name_list.Add(data.cast<wxString>());
			wxArraySizeT addr_list(1);
			self.getProcAddress(name_list, addr_list);
			return py::int_(addr_list[0]);
		}
		else if (PyIterable_Check(data.ptr()))
		{
			// 返回一个字典
			wxArrayString name_list;
			wxArrayAddAll(name_list, data);
			wxArraySizeT addr_list(name_list.size());
			self.getProcAddress(name_list, addr_list);
			py::dict result;
			for (size_t i = 0; i < name_list.size(); i++)
			{
				result[name_list[i]] = addr_list[i];
			}
			return result;
		}
		return None;
	}
};


class PyProcessHandler: public ProcessHandler
{
public:
	friend void init_emuhacker(py::module &m);

	bool attach() override {
		PYBIND11_OVERLOAD_PURE(
			bool,                /* Return type */
			ProcessHandler,      /* Parent class */
			attach,              /* Name of function in C++ (must match Python name) */
		);
	}

	addr_t address_map(addr_t addr) override {
		PYBIND11_OVERLOAD_PURE(
			addr_t,              /* Return type */
			ProcessHandler,      /* Parent class */
			address_map,         /* Name of function in C++ (must match Python name) */
			addr                 /* Argument(s) */
		);
	};
};


void init_emuhacker(pybind11::module & m)
{
	using namespace py::literals;

	py::module emuhacker = m.def_submodule("emuhacker");

	auto addr_a = "addr"_a;
	auto offsets_a = "offsets"_a;
	auto data_a = "data"_a;
	auto size_a = "size"_a;
	auto start_a = "start"_a;
	auto type_a = "type"_a;

	py::class_<ProcessHandler, PyProcessHandler>(emuhacker, "ProcessHandler")
		.def(py::init<>())
		.def("attach", &ProcessHandler::attach)
		.def("attach_window", &ProcessHandler::attach_window)
		.def("attach_handle", &emuhacker::attach_handle)
		.def("address_map", &ProcessHandler::address_map)
		.def("read_uint", &ProcessHandler::read_uint)
		.def("write_uint", &ProcessHandler::write_uint)
		.def("read_int", &ProcessHandler::read_int)
		.def("write_int", &ProcessHandler::write_int)
		.def("read_ptr", &emuhacker::read_ptr)
		.def("write_ptr", &emuhacker::write_ptr)
		.def("read", &emuhacker::process_read, addr_a, type_a, "size"_a = 0)
		.def("write", &emuhacker::process_write, addr_a, data_a, "size"_a = 0)
		.def("read_addr", &ProcessHandler::read_addr)
		.def("read_last_addr", &emuhacker::read_last_addr)
		.def("add", &ProcessHandler::add)
		.def("get_module", &ProcessHandler::getModuleHandle)
		.def("get_module_file", &emuhacker::getModuleFile, "module"_a = 0)
		.def("get_module_version", &emuhacker::getModuleVersion)
		.def("alloc_memory", &ProcessHandler::alloc_memory, size_a, start_a=0, "protect"_a=PAGE_READWRITE)
		.def("alloc_data", &emuhacker::alloc_data, data_a, start_a=0)
		.def("write_function", &emuhacker::write_function, data_a, start_a = 0)
		.def("free_memory", &ProcessHandler::free_memory, addr_a)
		.def("find_bytes", &emuhacker::find_bytes, data_a, start_a, "end"_a, "ordinal"_a=1, "fuzzy"_a=false)
		.def("remote_call", &ProcessHandler::remote_call, addr_a, "arg"_a)
		// .def("bring_target_top", &ProcessHandler::bring_target_top)
		.def("enum_windows", &emuhacker::enum_windows, "callback"_a, "prefix"_a=None)
		.def("get_proc_helper", &ProcessHandler::getProcAddressHelper)
		.def_property_readonly("active", &ProcessHandler::isValid)
		.def_property_readonly("base_addr", &ProcessHandler::getProcessBaseAddress)
		.def_property_readonly("ptr_size", &ProcessHandler::getPtrSize)
		.def_property_readonly("window_text", &emuhacker::getWindowText)
		.def_readonly_static("is64os", &PyProcessHandler::m_is64os)
		.def_readonly("is32process", &PyProcessHandler::m_is32process)
		.def_readonly("thread_id", &PyProcessHandler::m_thread_id)
		.def_readwrite("raw_addr", &PyProcessHandler::m_raw_addr);

	py::class_<ProcAddressHelper>(emuhacker, "ProcAddressHelper")
		.def("get_proc_address", &emuhacker::getProcAddress);
}

#endif