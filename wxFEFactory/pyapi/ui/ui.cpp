#include <wx/wx.h>
#include "../pyutils.h"
#include "../functions.h"
#include "ui.h"
#include "screen.h"
#include "thread.h"
#include "console.h"
#include "utils/HistorySet.hpp"


void Console__bind_elem(ConsoleHandler* self, View *input, View *output)
{
	self->bindElem((wxComboBox*)input->ptr(), (wxTextCtrl*)output->ptr());
}


auto Console__get_history(ConsoleHandler* self)
{
	return asPyList(*(wxArrayString*)self->getHistory());
}


void init_ui(py::module &m)
{
	using namespace py::literals;

	py::module ui = m.def_submodule("ui");

	py::class_<ConsoleHandler>(ui, "Console")
		.def("bind_elem", Console__bind_elem)
		.def("get_history", Console__get_history);

	py::class_<PyThread>(ui, "Thread")
		.def(py::init<pyobj, DWORD>(), "fn"_a, "delay"_a=0)
		.def("Run", &PyThread::Run);

	m.def("getScreenSize", &Screen::getScreenSize)
		.def("getDpi", &Screen::getDpi);

	setattr(m, "console", py::cast(&pyConsole));


	init_uibase(ui);
	init_events(ui);
	init_frames(ui);
	init_menu(ui);
	init_containers(ui);
	init_controls(ui);
	init_aui(ui);
	init_bars(ui);
	init_datacontrols(ui);
	init_bitmap(ui);
}