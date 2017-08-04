#include <wx/wx.h>
#include "emuhacker.h"
#include "../pyutils.h"
#include "../functions.h"
#include "gba/VbaHandler.h"
#include "gba/NogbaHandler.h"
#include "nds/NogbaNdsHandler.h"
#include "nds/DeSmuMEHandler.h"
#include <windows.h>

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
		.def("read8", [](ProcessHandler& self, u32 addr) {
			return self.readUint(addr, sizeof(u8));
		})
		.def("read16", [](ProcessHandler& self, u32 addr) {
			return self.readUint(addr, sizeof(u16));
		})
		.def("read32", [](ProcessHandler& self, u32 addr) {
			return self.readUint(addr, sizeof(u32));
		})
		.def("read64", [](ProcessHandler& self, UINT64 addr) {
			return self.readUint(addr, sizeof(UINT64));
		})
		.def("write8", [](ProcessHandler& self, u32 addr, UINT64 data) {
			return self.writeUint(addr, sizeof(u8), data);
		})
		.def("write16", [](ProcessHandler& self, u32 addr, UINT64 data) {
			return self.writeUint(addr, sizeof(u8), data);
		})
		.def("write32", [](ProcessHandler& self, u32 addr, UINT64 data) {
			return self.writeUint(addr, sizeof(u32), data);
		})
		.def("write64", [](ProcessHandler& self, UINT64 addr, UINT64 data) {
			return self.writeUint(addr, sizeof(UINT64), data);
		})
		.def("read", [](ProcessHandler& self, u32 addr, size_t size) {
			char *buf = new char[size];
			self.read(addr, size, buf);
			py::bytes ret(buf, size);
			delete buf;
			return ret;
		}, addr_a, size_a)
		.def("write", [](ProcessHandler& self, u32 addr, size_t size, py::bytes &data) {
			return self.write(addr, size, bytesGetBuff(data));
		}, addr_a, size_a, data_a)
		.def("add", &ProcessHandler::add)
		.def("readFloat", [](ProcessHandler& self, u32 addr, float value) {
			return self.write(addr, value);
		})
		.def("readFloat", [](ProcessHandler& self, u32 addr) {
			return self.read<float>(addr);
		})
		.def("ptrsRead", [](ProcessHandler& self, u32 addr, py::iterable &args, pycref type) {
			const auto &builtin = py::module::import("builtins");
			wxArrayInt offsets = py::cast<wxArrayInt>(args);
			if (type == builtin.attr("float"))
			{
				return py::cast(self.ptrsRead<float>(addr, offsets));
			}
			else if (type == builtin.attr("bool"))
			{
				return py::cast(self.ptrsRead<bool>(addr, offsets));
			}
			else if (PY_IS_TYPE(type, PyLong))
			{
				UINT data = 0;
				if (self.ptrsRead(addr, offsets, py::cast<int>(type), &data))
				{
					return py::cast(data);
				}
			}
			return (pyobj&)(None);
		}, addr_a, offsets_a, type_a)
		.def("ptrsWrite", [](ProcessHandler& self, u32 addr, py::iterable &args, pycref data, pycref size) {
			const auto &builtin = py::module::import("builtins");
			wxArrayInt offsets = py::cast<wxArrayInt>(args);
			if (PY_IS_TYPE(data, PyFloat))
			{
				return self.ptrsWrite(addr, offsets, data.cast<float>());
			}
			else if (PY_IS_TYPE(data, PyBool))
			{
				return self.ptrsWrite(addr, offsets, data.cast<bool>());
			}
			else if (PY_IS_TYPE(data, PyLong))
			{
				UINT tmp = data.cast<UINT64>();
				self.ptrsWrite(addr, offsets, py::cast<int>(size), &tmp);
			}
			return false;
		}, addr_a, offsets_a, data_a, "size"_a=4);

	py::class_<VbaHandler, ProcessHandler>(emuhacker, "VbaHandler")
		.def(py::init<>());
	py::class_<NogbaHandler, ProcessHandler>(emuhacker, "NogbaHandler")
		.def(py::init<>());
	py::class_<NogbaNdsHandler, ProcessHandler>(emuhacker, "NogbaNdsHandler")
		.def(py::init<>());
	py::class_<DeSmuMEHandler, ProcessHandler>(emuhacker, "DeSmuMEHandler")
		.def(py::init<>());
}
