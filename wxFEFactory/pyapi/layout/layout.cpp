#include <wx/wx.h>
#include "../pyutils.h"
#include "../functions.h"
#include "layout.h"
#include "menu.h"
#include "bitmap.h"
#include "frames.h"
#include "containers.h"
#include "controls.h"
#include "datacontrols.h"
#include "aui.h"
#include "screen.h"
#include "bars.h"
#include "console.h"
#include "thread.h"

void setConsoleElem(TextInput &input, TextInput &output)
{
	pyConsole.setConsoleElem((wxTextCtrl*)input.ptr(), (wxTextCtrl*)output.ptr());
}


void init_layout(py::module &m)
{
	using namespace py::literals;

	py::module layout = m.def_submodule("layout");
	setattr(m, "ui", layout);

	// wx const
	ATTR_INT(layout.ptr(), HORIZONTAL, wx),
	ATTR_INT(layout.ptr(), VERTICAL, wx);

	// 为了方便，setConsoleElem 挂在外层模块，但在这里定义
	m.def("setConsoleElem", setConsoleElem, "input"_a, "output"_a);
	m.def("getScreenSize", &Screen::getScreenSize);

	py::class_<View>(layout, "View")
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
		.def_property_readonly("parent", &View::getParent);

	py::class_<Control, View>(layout, "Control");

	py::class_<Layout, View>(layout, "Layout")
		.def("__enter__", &Layout::__enter__)
		.def("__exit__", &Layout::__exit__)
		.def("styles", &Layout::setStyles)
		.def("removeChild", &Layout::removeChild)
		.def("reLayout", &Layout::reLayout)
		.def("findFocus", &Layout::findFocus)
		.def_readonly("children", &Layout::m_children);

	py::class_<PyThread>(layout, "Thread")
		.def(py::init<pyobj, DWORD>(), "fn"_a, "delay"_a=0)
		.def("Run", &PyThread::Run);


	// 按键事件
	py::class_<wxEvent>(layout, "Event")
		.def("Skip", &wxEvent::Skip, "skip"_a = true)
		.def_property("id", &wxEvent::GetId, &wxEvent::SetId);

	auto KeyEvent = py::class_<wxKeyEvent, wxEvent>(layout, "KeyEvent")
		.def("GetKeyCode", &wxKeyEvent::GetKeyCode)
		.def("GetModifiers", [](wxKeyEvent &event) {return event.GetModifiers(); event.ResumePropagation(1); })
		.def("getWXK", [](wxKeyEvent &event, wxChar *keystr) {
			int ch = keystr[0];
			if ('a' <= ch && ch <= 'z')
			{
				return ch - 32;
			}
			else if (33 <= ch && ch <= 126) {
				return ch;
			}
			return 0;
		}).ptr();


#define ATTR_ACCEL(name) ATTR_INT(KeyEvent, name, wxACCEL_)
	ATTR_ACCEL(NORMAL),
	ATTR_ACCEL(ALT),
	ATTR_ACCEL(CTRL),
	ATTR_ACCEL(SHIFT),
	ATTR_ACCEL(RAW_CTRL),
	ATTR_ACCEL(CMD);
#undef ATTR_ACCEL

#define ATTR_KEYCODE(name) ATTR_INT(KeyEvent, name, WXK_)
	ATTR_KEYCODE(BACK),
	ATTR_KEYCODE(TAB),
	ATTR_KEYCODE(RETURN),
	ATTR_KEYCODE(ESCAPE),
	ATTR_KEYCODE(SPACE),
	ATTR_INT(KeyEvent, _DELETE, WXK),
	ATTR_KEYCODE(LBUTTON),
	ATTR_KEYCODE(RBUTTON),
	ATTR_KEYCODE(MBUTTON),
	ATTR_KEYCODE(SHIFT),
	ATTR_KEYCODE(ALT),
	ATTR_KEYCODE(CONTROL),
	ATTR_KEYCODE(END),
	ATTR_KEYCODE(HOME),
	ATTR_KEYCODE(LEFT),
	ATTR_KEYCODE(UP),
	ATTR_KEYCODE(RIGHT),
	ATTR_KEYCODE(DOWN),
	ATTR_KEYCODE(PRINT),
	ATTR_KEYCODE(INSERT),
	ATTR_KEYCODE(NUMPAD0), ATTR_KEYCODE(NUMPAD1), ATTR_KEYCODE(NUMPAD2), ATTR_KEYCODE(NUMPAD3), ATTR_KEYCODE(NUMPAD4), ATTR_KEYCODE(NUMPAD5),
	ATTR_KEYCODE(NUMPAD6), ATTR_KEYCODE(NUMPAD7), ATTR_KEYCODE(NUMPAD8), ATTR_KEYCODE(NUMPAD9),
	ATTR_KEYCODE(MULTIPLY),
	ATTR_KEYCODE(ADD),
	ATTR_KEYCODE(SEPARATOR),
	ATTR_KEYCODE(SUBTRACT),
	ATTR_KEYCODE(DECIMAL),
	ATTR_KEYCODE(DIVIDE),
	ATTR_KEYCODE(F1), ATTR_KEYCODE(F2), ATTR_KEYCODE(F3), ATTR_KEYCODE(F4), ATTR_KEYCODE(F5), ATTR_KEYCODE(F6),
	ATTR_KEYCODE(F7), ATTR_KEYCODE(F8), ATTR_KEYCODE(F9), ATTR_KEYCODE(F10), ATTR_KEYCODE(F11), ATTR_KEYCODE(F12),
	ATTR_KEYCODE(NUMLOCK),
	ATTR_KEYCODE(PAGEUP),
	ATTR_KEYCODE(PAGEDOWN),
	ATTR_KEYCODE(NUMPAD_ENTER),
	ATTR_KEYCODE(NUMPAD_HOME),
	ATTR_KEYCODE(NUMPAD_LEFT),
	ATTR_KEYCODE(NUMPAD_UP),
	ATTR_KEYCODE(NUMPAD_RIGHT),
	ATTR_KEYCODE(NUMPAD_DOWN),
	ATTR_KEYCODE(NUMPAD_PAGEUP),
	ATTR_KEYCODE(NUMPAD_PAGEDOWN),
	ATTR_KEYCODE(NUMPAD_END),
	ATTR_KEYCODE(NUMPAD_BEGIN),
	ATTR_KEYCODE(NUMPAD_INSERT),
	ATTR_KEYCODE(NUMPAD_DELETE),
	ATTR_KEYCODE(NUMPAD_EQUAL),
	ATTR_KEYCODE(NUMPAD_MULTIPLY),
	ATTR_KEYCODE(NUMPAD_ADD),
	ATTR_KEYCODE(NUMPAD_SEPARATOR),
	ATTR_KEYCODE(NUMPAD_SUBTRACT),
	ATTR_KEYCODE(NUMPAD_DECIMAL),
	ATTR_KEYCODE(NUMPAD_DIVIDE),
	ATTR_KEYCODE(WINDOWS_LEFT),
	ATTR_KEYCODE(WINDOWS_RIGHT),
	ATTR_KEYCODE(WINDOWS_MENU);
#undef ATTR_KEYCODE

	init_frames(layout);
	init_menu(layout);
	init_containers(layout);
	init_controls(layout);
	init_aui(layout);
	init_bars(layout);
	init_datacontrols(layout);
	init_bitmap(layout);
}