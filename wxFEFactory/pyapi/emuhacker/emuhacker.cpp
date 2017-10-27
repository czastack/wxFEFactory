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


class PyProcessHandler : public ProcessHandler {
public:
	friend void init_emuhacker(py::module &m);

	auto read8(addr_t addr) { return readUint(addr, sizeof(u8)); }
	auto read16(addr_t addr) { return readUint(addr, sizeof(u16)); }
	auto read32(addr_t addr) { return readUint(addr, sizeof(u32)); }
	auto read64(addr_t addr) { return readUint(addr, sizeof(UINT64)); }
	auto readFloat(addr_t addr) { return read<float>(addr); }
	bool write8(addr_t addr, UINT64 data) { return writeUint(addr, data, sizeof(u8)); }
	bool write16(addr_t addr, UINT64 data) { return writeUint(addr, data, sizeof(u16)); }
	bool write32(addr_t addr, UINT64 data) { return writeUint(addr, data, sizeof(u32)); }
	bool write64(addr_t addr, UINT64 data) { return writeUint(addr, data, sizeof(UINT64)); }
	bool writeFloat(addr_t addr, float value) { return write(addr, value); }


	pyobj process_read(addr_t addr, pycref type, size_t size)
	{
		const auto &builtin = py::module::import("builtins");
		if (type == builtin.attr("float"))
		{
			return py::cast(read<float>(addr));
		}
		else if (type == builtin.attr("bool"))
		{
			return py::cast(read<bool>(addr));
		}
		else if (type == builtin.attr("int"))
		{
			UINT64 data = readUint(addr, size ? size : getPtrSize());
			return py::cast(data);
		}
		else if (size)
		{
			char *buf = new char[size];
			read(addr, buf, size);
			py::bytes ret(buf, size);
			delete buf;
			return ret;
		}
		return None;
	}


	bool process_write(addr_t addr, pycref data, size_t size)
	{
		if (PY_IS_TYPE(data, PyFloat))
		{
			return write(addr, data.cast<float>());
		}
		else if (PY_IS_TYPE(data, PyBool))
		{
			return write(addr, data.cast<bool>());
		}
		else if (PY_IS_TYPE(data, PyLong))
		{
			writeUint(addr, data.cast<UINT64>(), size ? size : getPtrSize());
		}
		else if (PY_IS_TYPE(data, PyBytes))
		{
			if (size == 0)
				size = py::len(data);
			return write(addr, bytesGetBuff(data), size);
		}
		else if (PY_IS_TYPE(data, PyByteArray))
		{
			if (size == 0)
				size = py::len(data);
			return write(addr, PyByteArray_AsString(data.ptr()), size);
		}

		return false;
	}


	addr_t readLastAddr(addr_t addr, py::iterable &args)
	{
		wxArrayInt offsets = py::cast<wxArrayInt>(args);
		return ProcessHandler::readLastAddr(addr, offsets);
	}


	auto ptrRead(addr_t addr, u32 offset, pycref type, pycref size) {
		addr = readAddr(addr);
		if (addr)
		{
			return process_read(addr + offset, type, size.cast<size_t>());
		}
		return py::cast(false);
	}

	auto ptrWrite(addr_t addr, u32 offset, pycref data, pycref size) {
		addr = readAddr(addr);
		if (addr)
		{
			return process_write(addr + offset, data, size.cast<size_t>());
		}
		return false;
	}

	auto ptrsRead(addr_t addr, py::iterable &args, pycref type, pycref size) {
		addr = readLastAddr(addr, args);
		if (addr)
		{
			return process_read(addr, type, size.cast<size_t>());
		}
		return py::cast(false);
	}

	auto ptrsWrite(addr_t addr, py::iterable &args, pycref data, pycref size) {
		addr = readLastAddr(addr, args);
		if (addr)
		{
			return process_write(addr, data, size.cast<size_t>());
		}
		return false;
	}

	auto write_function(py::bytes buf) {
		char *buff;
		ssize_t size;
		PyBytes_AsStringAndSize(buf.ptr(), &buff, &size);
		return ProcessHandler::write_function(buff, size);
	}
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

	py::class_<ProcessHandler, PyProcessHandler>(emuhacker, "ProcessHandler")
		.def(py::init<>())
		.def("attach", &ProcessHandler::attach)
		.def("attachByWindowName", &ProcessHandler::attachByWindowName)
		.def("readUint", &ProcessHandler::readUint)
		.def("writeUint", &ProcessHandler::writeUint)
		.def("read8", &PyProcessHandler::read8)
		.def("read16", &PyProcessHandler::read16)
		.def("read32", &PyProcessHandler::read32)
		.def("read64", &PyProcessHandler::read64)
		.def("write8", &PyProcessHandler::write8)
		.def("write16", &PyProcessHandler::write16)
		.def("write32", &PyProcessHandler::write32)
		.def("write64", &PyProcessHandler::write64)
		.def("read", &PyProcessHandler::process_read, addr_a, type_a, "size"_a=0)
		.def("write", &PyProcessHandler::process_write, addr_a, data_a, "size"_a=0)
		.def("add", &ProcessHandler::add)
		.def("readAddr", &ProcessHandler::readAddr)
		.def("readFloat", &PyProcessHandler::readFloat)
		.def("writeFloat", &PyProcessHandler::writeFloat)
		.def("ptrRead", &PyProcessHandler::ptrRead, addr_a, offsets_a, type_a, "size"_a=4)
		.def("ptrWrite", &PyProcessHandler::ptrWrite, addr_a, offsets_a, data_a, "size"_a=4)
		.def("readLastAddr", &PyProcessHandler::readLastAddr, addr_a, offsets_a)
		.def("ptrsRead", &PyProcessHandler::ptrsRead, addr_a, offsets_a, type_a, "size"_a=4)
		.def("ptrsWrite", &PyProcessHandler::ptrsWrite, addr_a, offsets_a, data_a, "size"_a = 4)
		.def("get_module", &PyProcessHandler::getModuleHandle)
		.def("write_function", &PyProcessHandler::write_function)
		.def("alloc_memory", &ProcessHandler::alloc_memory, size_a)
		.def("free_memory", &ProcessHandler::free_memory)
		.def("remote_call", &ProcessHandler::remote_call, addr_a, "arg"_a)
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