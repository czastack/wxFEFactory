#include <wx/wx.h>
#include "bars.h"

void init_bars(py::module & m)
{
	using namespace py::literals;

	auto className = "className"_a = None;
	auto style = "style"_a = None;
	auto styles = "styles"_a = None;
	auto n = "n"_a;

	py::class_t<ToolBar, Layout>(m, "ToolBar")
		.def(py::init<long, pyobj, pyobj, pyobj>(), "wxstyle"_a = (long)wxHORIZONTAL | wxTB_TEXT, styles, className, style)
		.def("addTool", &ToolBar::addTool,
			"label"_a, "shortHelp"_a = wxEmptyString, "bitmap"_a = None, "onclick"_a = None, "toolid"_a = -1, "kind"_a = wxEmptyString)
		.def("addControl", &ToolBar::addControl, "view"_a, "label"_a = wxNoneString, "onclick"_a = None)
		.def("addSeparator", &ToolBar::addSeparator)
		.def("realize", &ToolBar::realize)
		.def("getToolPos", &ToolBar::getToolPos)
		.def("setToolBitmapSize", &ToolBar::setToolBitmapSize);

	py::class_t<AuiToolBar, Layout>(m, "AuiToolBar")
		.def(py::init<long, pyobj, pyobj, pyobj>(), "wxstyle"_a = (long)wxAUI_TB_HORIZONTAL | wxAUI_TB_TEXT, styles, className, style)
		.def("addTool", &AuiToolBar::addTool,
			"label"_a, "shortHelp"_a = wxEmptyString, "bitmap"_a = None, "onclick"_a = None, "toolid"_a = -1, "kind"_a = wxEmptyString)
		.def("addControl", &AuiToolBar::addControl, "view"_a, "label"_a = wxNoneString, "onclick"_a = None)
		.def("addSeparator", &AuiToolBar::addSeparator)
		.def("realize", &AuiToolBar::realize)
		.def("getToolPos", &AuiToolBar::getToolPos)
		.def("setToolBitmapSize", &AuiToolBar::setToolBitmapSize);

	py::class_t<StatusBar, Control>(m, "StatusBar")
		.def(py::init<pyobj, pyobj>(), className, style)
		.def("getText", &StatusBar::getText, n)
		.def("setText", &StatusBar::setText, "text"_a, n)
		.def("setFieldsCount", &StatusBar::setFieldsCount, "list"_a)
		.def("setItemWidths", &StatusBar::setItemWidths, "list"_a)
		.def("getStatusWidth", &StatusBar::getStatusWidth, n)
		.def("popStatusText", &StatusBar::popStatusText, n)
		.def("pushStatusText", &StatusBar::pushStatusText, "text"_a, n);
}
