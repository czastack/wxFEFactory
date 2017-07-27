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

	py::class_<ProcessHandler>(emuhacker, "ProcessHandler")
		.def("attach", &ProcessHandler::attach)
		.def("read8", [](ProcessHandler& self, u32 addr) {
			return self.read<u8>(addr);
		})
		.def("read16", [](ProcessHandler& self, u32 addr) {
			return self.read<u16>(addr);
		})
		.def("read32", [](ProcessHandler& self, u32 addr) {
			return self.read<u32>(addr);
		})
		.def("write8", [](ProcessHandler& self, u32 addr, u8 data) {
			return self.write(addr, data);
		})
		.def("write16", [](ProcessHandler& self, u32 addr, u16 data) {
			return self.write(addr, data);
		})
		.def("write32", [](ProcessHandler& self, u32 addr, u32 data) {
			return self.write(addr, data);
		})
		.def("read", [](ProcessHandler& self, u32 addr, size_t size, char* buf) {
			return self.read(addr, size, buf);
		})
		.def("write", [](ProcessHandler& self, u32 addr, size_t size, char* buf) {
			return self.write(addr, size, buf);
		})
		.def("add", &ProcessHandler::add);

	py::class_<VbaHandler, ProcessHandler>(emuhacker, "VbaHandler")
		.def(py::init<>());
	py::class_<NogbaHandler, ProcessHandler>(emuhacker, "NogbaHandler")
		.def(py::init<>());
	py::class_<NogbaNdsHandler, ProcessHandler>(emuhacker, "NogbaNdsHandler")
		.def(py::init<>());
	py::class_<DeSmuMEHandler, ProcessHandler>(emuhacker, "DeSmuMEHandler")
		.def(py::init<>());
}
