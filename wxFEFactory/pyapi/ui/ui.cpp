#include <wx/wx.h>
#include "../pyutils.h"
#include "../functions.h"
#include "ui.h"
#include "screen.h"
#include "thread.h"
#include "console.h"


void setConsoleElem(View *input, View *output)
{
	pyConsole.setConsoleElem((wxTextCtrl*)input->ptr(), (wxTextCtrl*)output->ptr());
}


void init_ui(py::module &m)
{
	using namespace py::literals;

	py::module ui = m.def_submodule("ui");

	// wx const
	ATTR_INT(ui.ptr(), HORIZONTAL, wx),
	ATTR_INT(ui.ptr(), VERTICAL, wx);

	// 为了方便，setConsoleElem 挂在外层模块，但在这里定义
	m.def("setConsoleElem", setConsoleElem, "input"_a, "output"_a)
		.def("getScreenSize", &Screen::getScreenSize)
		.def("getDpi", &Screen::getDpi);

	py::class_<PyThread>(ui, "Thread")
		.def(py::init<pyobj, DWORD>(), "fn"_a, "delay"_a=0)
		.def("Run", &PyThread::Run);


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


	ATTR_INT(ui.ptr(), ID_OK, wx),
	ATTR_INT(ui.ptr(), ID_CANCEL, wx);
}