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

	auto view = py::class_<View>(ui, "View")
		.def("isShow", &View::isShow)
		.def("show", &View::show, "show"_a=true)
		.def("destroy", &View::destroy)
		.def("refresh", &View::refresh)
		.def("setToolTip", &View::setToolTip)
		.def("setContextMenu", &View::setContextMenu)
		.def("setOnKeyDown", &View::setOnKeyDown)
		.def("setOnFileDrop", &View::setOnFileDrop)
		.def("setOnTextDrop", &View::setOnTextDrop)
		.def("setOnClick", &View::setOnClick)
		.def("setOnDoubleClick", &View::setOnDoubleClick)
		.def("setOnDestroy", &View::setOnDestroy)
		.def_static("get_active_layout", &View::getActiveLayout)
		.def_readwrite("style", &View::m_style)
		.def_readwrite("className", &View::m_class)
		.def_property("enabled", &View::getEnabaled, &View::setEnabaled)
		.def_property("background", &View::getBackground, &View::setBackground)
		.def_property("color", &View::getForeground, &View::setForeground)
		.def_property("id",
			[](View &self) { return self.ptr()->GetId(); },
			[](View &self, int id) { self.ptr()->SetId(id); }
		)
		.def_property_readonly("parent", &View::getParent);

	py::class_<Control, View>(ui, "Control");

	py::class_<Layout, View>(ui, "Layout")
		.def("__enter__", &Layout::__enter__)
		.def("__exit__", &Layout::__exit__)
		.def("styles", &Layout::setStyles)
		.def("removeChild", &Layout::removeChild)
		.def("clearChildren", &Layout::clearChildren)
		.def("reLayout", &Layout::reLayout)
		.def("findFocus", &Layout::findFocus)
		.def_readonly("children", &Layout::m_children);

	py::class_<PyThread>(ui, "Thread")
		.def(py::init<pyobj, DWORD>(), "fn"_a, "delay"_a=0)
		.def("Run", &PyThread::Run);


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