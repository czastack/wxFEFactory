#ifdef _WIN32

#include <wx/wx.h>
#include "emuhacker.h"
#include "../pyutils.h"
#include "../functions.h"
#include "gba/VbaHandler.h"
#include "gba/NogbaHandler.h"
#include "nds/NogbaNdsHandler.h"
#include "nds/DeSmuMEHandler.h"
#include <windows.h>
#include <psapi.h>
#include <tuple>


namespace emuhacker {

	auto read8(ProcessHandler &self, addr_t addr) { return self.readUint(addr, sizeof(u8)); }
	auto read16(ProcessHandler &self, addr_t addr) { return self.readUint(addr, sizeof(u16)); }
	auto read32(ProcessHandler &self, addr_t addr) { return self.readUint(addr, sizeof(u32)); }
	auto read64(ProcessHandler &self, addr_t addr) { return self.readUint(addr, sizeof(UINT64)); }
	auto readPtr(ProcessHandler &self, addr_t addr) { return self.readUint(addr, self.getPtrSize()); }
	auto readFloat(ProcessHandler &self, addr_t addr) { return self.read<float>(addr); }
	auto readDouble(ProcessHandler &self, addr_t addr) { return self.read<double>(addr); }
	bool write8(ProcessHandler &self, addr_t addr, size_t data) { return self.writeUint(addr, data, sizeof(u8)); }
	bool write16(ProcessHandler &self, addr_t addr, size_t data) { return self.writeUint(addr, data, sizeof(u16)); }
	bool write32(ProcessHandler &self, addr_t addr, size_t data) { return self.writeUint(addr, data, sizeof(u32)); }
	bool write64(ProcessHandler &self, addr_t addr, UINT64 data) { return self.writeUint(addr, data, sizeof(UINT64)); }
	bool writePtr(ProcessHandler &self, addr_t addr, size_t data) { return self.writeUint(addr, data, self.getPtrSize()); }
	bool writeFloat(ProcessHandler &self, addr_t addr, float value) { return self.write(addr, value); }
	bool writeDouble(ProcessHandler &self, addr_t addr, double value) { return self.write(addr, value); }


	pyobj process_read(ProcessHandler &self, addr_t addr, pycref type, size_t size)
	{
		const auto &builtin = py::module::import("builtins");
		if (type.is(builtin.attr("int")))
		{
			size_t data = self.readUint(addr, size ? size : self.getPtrSize());
			return py::cast(data);
		}
		else if (type.is(builtin.attr("float")))
		{
			return py::cast(self.read<float>(addr));
		}
		else if (type.is(builtin.attr("bool")))
		{
			return py::cast(self.read<bool>(addr));
		}
		else if (size)
		{
			char *buf = new char[size];
			self.read(addr, buf, size);
			py::bytes ret(buf, size);
			delete buf;
			return ret;
		}
		return None;
	}


	bool process_write(ProcessHandler &self, addr_t addr, pycref data, size_t size)
	{
		if (PY_IS_TYPE(data, PyLong))
		{
			self.writeUint(addr, data.cast<size_t>(), size ? size : self.getPtrSize());
		}
		else if (PY_IS_TYPE(data, PyFloat))
		{
			return self.write(addr, data.cast<float>());
		}
		else if (PY_IS_TYPE(data, PyBool))
		{
			return self.write(addr, data.cast<bool>());
		}
		else if (PY_IS_TYPE(data, PyBytes))
		{
			if (size == 0)
				size = py::len(data);
			return self.write(addr, bytesGetBuff(data), size);
		}
		else if (PY_IS_TYPE(data, PyByteArray))
		{
			if (size == 0)
				size = py::len(data);
			return self.write(addr, PyByteArray_AsString(data.ptr()), size);
		}

		return false;
	}


	addr_t readLastAddr(ProcessHandler &self, addr_t addr, py::iterable &args)
	{
		wxArrayInt offsets = py::cast<wxArrayInt>(args);
		return self.readLastAddr(addr, offsets);
	}


	auto ptrRead(ProcessHandler &self, addr_t addr, u32 offset, pycref type, pycref size) {
		addr = self.readAddr(addr);
		if (addr)
		{
			return process_read(self, addr + offset, type, size.cast<size_t>());
		}
		return py::cast(false);
	}

	auto ptrWrite(ProcessHandler &self, addr_t addr, u32 offset, pycref data, pycref size) {
		addr = self.readAddr(addr);
		if (addr)
		{
			return process_write(self, addr + offset, data, size.cast<size_t>());
		}
		return false;
	}

	auto ptrsRead(ProcessHandler &self, addr_t addr, py::iterable &args, pycref type, pycref size) {
		wxArrayInt &&offsets = py::cast<wxArrayInt>(args);
		addr = self.readLastAddr(addr, offsets);
		if (addr)
		{
			return process_read(self, addr, type, size.cast<size_t>());
		}
		return py::cast(false);
	}

	auto ptrsWrite(ProcessHandler &self, addr_t addr, py::iterable &args, pycref data, pycref size) {
		wxArrayInt &&offsets = py::cast<wxArrayInt>(args);
		addr = self.readLastAddr(addr, offsets);
		if (addr)
		{
			return process_write(self, addr, data, size.cast<size_t>());
		}
		return false;
	}

	auto write_function(ProcessHandler &self, py::bytes buf) {
		char *buff;
		ssize_t size;
		PyBytes_AsStringAndSize(buf.ptr(), &buff, &size);
		return self.write_function(buff, size);
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

	BOOL CALLBACK _enumWindow(HWND hWnd, LPARAM lParam)
	{
		TCHAR szWindowName[64];
		DWORD cchWindowName;
		BOOL  bContinue = TRUE;

		cchWindowName = GetWindowText(hWnd, szWindowName, 64);
		auto &pArgs = *(std::tuple<pycref, wxChar*, Py_ssize_t>*)lParam;
		wxChar* prefix = std::get<1>(pArgs);
		if (!prefix || wcsncmp(szWindowName, prefix, std::get<2>(pArgs)) == 0)
		{
			py::object ret = pyCall(std::get<0>(pArgs), (LPARAM)hWnd, szWindowName);
			return PyObject_IsTrue(ret.ptr());
		}
		return TRUE;
	}

	void enumWindows(ProcessHandler &self, pycref callback, pycref prefix)
	{
		Py_ssize_t prefix_len = 0;
		wxChar *title_prefix = prefix.is_none() ? nullptr : PyUnicode_AsWideCharString(prefix.ptr(), &prefix_len);
		std::tuple<pycref, wxChar*, Py_ssize_t> args(callback, title_prefix, prefix_len);
		EnumWindows(_enumWindow, reinterpret_cast<LPARAM>(&args));
		if (title_prefix)
		{
			PyMem_Free(title_prefix);
		}
	}

	bool attachByWindowHandle(ProcessHandler &self, size_t hWnd)
	{
		return self.attachByWindowHandle((HWND)hWnd);
	}
};


class PyProcessHandler: public ProcessHandler
{
public:
	using ProcessHandler::m_is64os;
	using ProcessHandler::m_is32process;
};


void init_emuhacker(pybind11::module & m)
{
	using namespace py::literals;

	py::module emuhacker = m.def_submodule("emuhacker");

	auto addr_a = "addr"_a;
	auto offsets_a = "offsets"_a;
	auto size_a = "size"_a;
	auto data_a = "data"_a;
	auto type_a = "type"_a;

	py::class_<ProcessHandler>(emuhacker, "ProcessHandler")
		.def(py::init<>())
		.def("attach", &ProcessHandler::attach)
		.def("attachByWindowName", &ProcessHandler::attachByWindowName)
		.def("attachByWindowHandle", &emuhacker::attachByWindowHandle)
		.def("readUint", &ProcessHandler::readUint)
		.def("writeUint", &ProcessHandler::writeUint)
		.def("readInt", &ProcessHandler::readInt)
		.def("writeInt", &ProcessHandler::writeInt)
		.def("read8", &emuhacker::read8)
		.def("read16", &emuhacker::read16)
		.def("read32", &emuhacker::read32)
		.def("read64", &emuhacker::read64)
		.def("write8", &emuhacker::write8)
		.def("write16", &emuhacker::write16)
		.def("write32", &emuhacker::write32)
		.def("write64", &emuhacker::write64)
		.def("readPtr", &emuhacker::readPtr)
		.def("writePtr", &emuhacker::writePtr)
		.def("read", &emuhacker::process_read, addr_a, type_a, "size"_a = 0)
		.def("write", &emuhacker::process_write, addr_a, data_a, "size"_a = 0)
		.def("readAddr", &ProcessHandler::readAddr)
		.def("readFloat", &emuhacker::readFloat)
		.def("writeFloat", &emuhacker::writeFloat)
		.def("readDouble", &emuhacker::readDouble)
		.def("writeDouble", &emuhacker::writeDouble)
		.def("ptrRead", &emuhacker::ptrRead, addr_a, offsets_a, type_a, "size"_a = 4)
		.def("ptrWrite", &emuhacker::ptrWrite, addr_a, offsets_a, data_a, "size"_a = 4)
		.def("readLastAddr", &emuhacker::readLastAddr, addr_a, offsets_a)
		.def("ptrsRead", &emuhacker::ptrsRead, addr_a, offsets_a, type_a, "size"_a = 4)
		.def("ptrsWrite", &emuhacker::ptrsWrite, addr_a, offsets_a, data_a, "size"_a = 4)
		.def("add", &ProcessHandler::add)
		.def("get_module", &ProcessHandler::getModuleHandle)
		.def("get_module_file", &emuhacker::getModuleFile, "module"_a = 0)
		.def("get_module_version", &emuhacker::getModuleVersion)
		.def("write_function", &emuhacker::write_function)
		.def("alloc_memory", &ProcessHandler::alloc_memory, size_a)
		.def("free_memory", &ProcessHandler::free_memory)
		.def("remote_call", &ProcessHandler::remote_call, addr_a, "arg"_a)
		.def("enumWindows", &emuhacker::enumWindows, "callback"_a, "prefix"_a=None)
		.def_property_readonly("active", &ProcessHandler::isValid)
		.def_property_readonly("base", &ProcessHandler::getProcessBaseAddress)
		.def_property_readonly("ptr_size", &ProcessHandler::getPtrSize)
		.def_readonly_static("is64os", &PyProcessHandler::m_is64os)
		.def_readonly("is32process", &PyProcessHandler::m_is32process);

	py::class_<VbaHandler, ProcessHandler>(emuhacker, "VbaHandler")
		.def(py::init<>());
	py::class_<NogbaHandler, ProcessHandler>(emuhacker, "NogbaHandler")
		.def(py::init<>());
	py::class_<NogbaNdsHandler, ProcessHandler>(emuhacker, "NogbaNdsHandler")
		.def(py::init<>());
	py::class_<DeSmuMEHandler, ProcessHandler>(emuhacker, "DeSmuMEHandler")
		.def(py::init<>());
}

#endif