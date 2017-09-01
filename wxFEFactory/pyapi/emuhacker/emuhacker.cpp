#ifdef __WXMSW__

#include <wx/wx.h>
#include "emuhacker.h"
#include "../pyutils.h"
#include "../functions.h"
#include "gba/VbaHandler.h"
#include "gba/NogbaHandler.h"
#include "nds/NogbaNdsHandler.h"
#include "nds/DeSmuMEHandler.h"
#include <windows.h>


pyobj process_read(ProcessHandler& self, addr_t addr, size_t size, pycref type)
{
	const auto &builtin = py::module::import("builtins");
	if (type == builtin.attr("float"))
	{
		return py::cast(self.read<float>(addr));
	}
	else if (type == builtin.attr("bool"))
	{
		return py::cast(self.read<bool>(addr));
	}
	else if (type == builtin.attr("int"))
	{
		UINT data = 0;
		if (self.read(addr, size, &data))
		{
			return py::cast(data);
		}
		return py::cast(0);
	}
	else
	{
		char *buf = new char[size];
		self.read(addr, size, buf);
		py::bytes ret(buf, size);
		delete buf;
		return ret;
	}
}


bool process_write(ProcessHandler& self, addr_t addr, size_t size, pycref data)
{
	if (PY_IS_TYPE(data, PyFloat))
	{
		return self.write(addr, data.cast<float>());
	}
	else if (PY_IS_TYPE(data, PyBool))
	{
		return self.write(addr, data.cast<bool>());
	}
	else if (PY_IS_TYPE(data, PyLong))
	{
		UINT tmp = data.cast<UINT64>();
		return self.write(addr, size, &tmp);
	}
	else if (PY_IS_TYPE(data, PyBytes))
	{
		if (size == 0)
			size = py::len(data);
		return self.write(addr, size, bytesGetBuff(data));
	}

	return false;
}


addr_t readLastAddr(ProcessHandler& self, addr_t addr, py::iterable &args)
{
	wxArrayInt offsets = py::cast<wxArrayInt>(args);
	return self.readLastAddr(addr, offsets);
}


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
		.def("readUint", &ProcessHandler::readUint)
		.def("writeUint", &ProcessHandler::writeUint)
		.def("read8", [](ProcessHandler& self, addr_t addr) {
			return self.readUint(addr, sizeof(u8));
		})
		.def("read16", [](ProcessHandler& self, addr_t addr) {
			return self.readUint(addr, sizeof(u16));
		})
		.def("read32", [](ProcessHandler& self, addr_t addr) {
			return self.readUint(addr, sizeof(u32));
		})
		.def("read64", [](ProcessHandler& self, UINT64 addr) {
			return self.readUint(addr, sizeof(UINT64));
		})
		.def("write8", [](ProcessHandler& self, addr_t addr, UINT64 data) {
			return self.writeUint(addr, sizeof(u8), data);
		})
		.def("write16", [](ProcessHandler& self, addr_t addr, UINT64 data) {
			return self.writeUint(addr, sizeof(u16), data);
		})
		.def("write32", [](ProcessHandler& self, addr_t addr, UINT64 data) {
			return self.writeUint(addr, sizeof(u32), data);
		})
		.def("write64", [](ProcessHandler& self, UINT64 addr, UINT64 data) {
			return self.writeUint(addr, sizeof(UINT64), data);
		})
		.def("read", process_read, addr_a, size_a, type_a)
		.def("write", process_write, addr_a, size_a, data_a)
		.def("add", &ProcessHandler::add)
		.def("readAddr", &ProcessHandler::readAddr)
		.def("readFloat", [](ProcessHandler& self, addr_t addr) {
			return self.read<float>(addr);
		})
		.def("writeFloat", [](ProcessHandler& self, addr_t addr, float value) {
			return self.write(addr, value);
		})
		.def("ptrRead", [](ProcessHandler& self, addr_t addr, u32 offset, pycref type, pycref size) {
			addr = self.readAddr(addr);
			if (addr)
			{
				return process_read(self, addr + offset, size.cast<size_t>(), type);
			}
			return py::cast(false);
		}, addr_a, offsets_a, type_a, "size"_a = 4)
		.def("ptrWrite", [](ProcessHandler& self, addr_t addr, u32 offset, pycref data, pycref size) {
			addr = self.readAddr(addr);
			if (addr)
			{
				return process_write(self, addr + offset, size.cast<size_t>(), data);
			}
			return false;
		}, addr_a, offsets_a, data_a, "size"_a=4)
		.def("readLastAddr", readLastAddr, addr_a, offsets_a)
		.def("ptrsRead", [](ProcessHandler& self, addr_t addr, py::iterable &args, pycref type, pycref size) {
			addr = readLastAddr(self, addr, args);
			if (addr)
			{
				return process_read(self, addr, size.cast<size_t>(), type);
			}
			return py::cast(false);
		}, addr_a, offsets_a, type_a, "size"_a = 4)
		.def("ptrsWrite", [](ProcessHandler& self, addr_t addr, py::iterable &args, pycref data, pycref size) {
			addr = readLastAddr(self, addr, args);
			if (addr)
			{
				return process_write(self, addr, size.cast<size_t>(), data);
			}
			return false;
		}, addr_a, offsets_a, data_a, "size"_a=4)
		.def_readwrite("addr_is32", &ProcessHandler::m_addr_is32);

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