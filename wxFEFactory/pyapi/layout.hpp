#include "menu.hpp"
#include "layouts.hpp"
#include "controls.hpp"
#include "datacontrols.hpp"
#include "aui.hpp"
#include "bars.hpp"

void initLayout(py::module &m)
{
	using namespace py::literals;

	auto key = "key"_a=None;
	auto className = "className"_a=None;
	auto style = "style"_a=None;
	auto styles = "styles"_a=None;
	auto label = "label"_a;
	auto type = "type"_a=wxEmptyString;
	auto extStyle = "extStyle"_a=0;

	auto view_init = py::init<pyobj, pyobj, pyobj>();
	auto layout_init = py::init<pyobj, pyobj, pyobj, pyobj>();

	py::module layout = m.def_submodule("layout");
	initMenu(layout);

	py::class_<View>(layout, "View")
		.def("setContextMenu", &View::setContextMenu)
		.def_readwrite("style", &View::m_style)
		.def_readwrite("key", &View::m_key)
		.def_readwrite("className", &View::m_class)
		.def_static("confirm", &confirm_dialog)
		.def_property("enabled", &View::getEnabaled, &View::setEnabaled);

	py::class_<Control, View>(layout, "Control");

	py::class_<Layout, View>(layout, "Layout")
		.def("__enter__", &Layout::__enter__)
		.def("__exit__", &Layout::__exit__)
		.def("__getattr__", &Layout::__getattr__)
		.def("styles", &Layout::setStyles)
		.def("removeChild", &Layout::removeChild)
		.def_readonly("children", &Layout::m_children)
		.def_readonly("named_children", &Layout::m_named_children);

	py::class_t<BaseFrame, Layout>(layout, "BaseFrame")
		.def("close", &BaseFrame::close)
		.def_property("title", &BaseFrame::getTitle, &BaseFrame::setTitle);

	py::class_t<Window, BaseFrame>(layout, "Window")
		.def_init(py::init<wxcstr, MenuBar*, pyobj, pyobj, pyobj, pyobj>(),
			label, "menuBar"_a=nullptr, styles, key, className, style)
		.def_property_readonly("menubar", &Window::getMenuBar)
		.def_property_readonly("statusbar", &Window::getStatusBar);

	py::class_t<Dialog, BaseFrame>(layout, "Dialog")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj, pyobj>(),
			label, styles, key, className, style);

	py::class_t<Vertical, Layout>(layout, "Vertical")
		.def_init(layout_init, styles, key, className, style);

	py::class_t<Horizontal, Layout>(layout, "Horizontal")
		.def_init(layout_init, styles, key, className, style);

	py::class_t<GridLayout, Layout>(layout, "GridLayout")
		.def_init(py::init<int, int, int, int, pyobj, pyobj, pyobj, pyobj>(),
			"rows"_a=0, "cols"_a=2, "vgap"_a=0, "hgap"_a=0,
			styles, key, className, style);

	py::class_t<FlexGridLayout, Layout>(layout, "FlexGridLayout")
		.def_init(py::init<int, int, int, int, pyobj, pyobj, pyobj, pyobj>(),
			"rows"_a=0, "cols"_a=2, "vgap"_a=0, "hgap"_a=0,
			styles, key, className, style);

	py::class_t<ScrollView, Layout>(layout, "ScrollView")
		.def_init(py::init<bool, pyobj, pyobj, pyobj, pyobj>(),
			"horizontal"_a=false, styles, key, className, style);

	py::class_t<SplitterWindow, Layout>(layout, "SplitterWindow")
		.def_init(py::init<bool, int, pyobj, pyobj, pyobj, pyobj>(),
			"horizontal"_a=false, "sashpos"_a=0, styles, key, className, style);

	py::class_t<Button, Control>(layout, "Button")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj, pyobj>(),
			label, "onclick"_a=None, key, className, style)
		.def("setOnclick", &Button::setOnclick)
		.def("setLabel", &Button::setLabel);

	py::class_t<CheckBox, Control>(layout, "CheckBox")
		.def_init(py::init<wxcstr, bool, bool, pyobj, pyobj, pyobj, pyobj>(), 
			label, "checked"_a=false, "alignRight"_a=false, "onchange"_a = None, key, className, style)
		.def("setLabel", &CheckBox::setLabel)
		.def("trigger", &CheckBox::trigger)
		.def_property("checked", &CheckBox::getChecked, &CheckBox::setChecked)
		.def_readwrite("onchange", &CheckBox::m_listener);

	py::class_t<Text, Control>(layout, "Text")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj>(), label, key, className, style)
		.def("setText", &Text::setText);

	py::class_t<TextInput, Control>(layout, "TextInput")
		.def_init(py::init<wxcstr, wxcstr, bool, bool, int, pyobj, pyobj, pyobj>(),
			"value"_a=wxEmptyString, type, "readonly"_a=false, "multiline"_a=false, extStyle, key, className, style)
		.def_property("value", &TextInput::getValue, &TextInput::setValue);

	py::class_<BaseControlWithItems, Control>(layout, "BaseControlWithItems")
		.def("getSelectedText", &BaseControlWithItems::getSelectedText)
		.def("getValue", &BaseControlWithItems::getValue, "i"_a=None)
		.def("setValue", &BaseControlWithItems::setValue)
		.def("getSelection", &BaseControlWithItems::getSelection)
		.def("setSelection", &BaseControlWithItems::setSelection)
		.def_readwrite("onselect", &BaseControlWithItems::m_listener);

	py::class_<ControlWithItems, BaseControlWithItems>(layout, "ControlWithItems")
		.def("setItems", &ControlWithItems::setItems, "options"_a, "values"_a=None)
		.def("append", &ControlWithItems::append, "options"_a, "values"_a=None)
		.def("insert", &ControlWithItems::insert, "options"_a, "values"_a=None, "pos"_a)
		.def("remove", &ControlWithItems::remove, "pos"_a)
		.def("clear", &ControlWithItems::clear);

	py::class_t<ListBox, ControlWithItems>(layout, "ListBox")
		.def_init(py::init<pyobj, pyobj, pyobj, pyobj, pyobj, pyobj>(),
			"options"_a=None, "values"_a=None, "onselect"_a=None, key, className, style);

	py::class_t<ComboBox, ControlWithItems>(layout, "ComboBox")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj, pyobj, pyobj, pyobj>(),
			type, "options"_a=None, "values"_a=None, "onselect"_a=None, key, className, style);

	py::class_t<RadioBox, BaseControlWithItems>(layout, "RadioBox")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj, pyobj, pyobj, pyobj>(),
			label, "options"_a=None, "values"_a=None, "onselect"_a=None, key, className, style);

	py::class_t<AuiManager, Layout>(layout, "AuiManager")
		.def(py::init<pyobj>(), key)
		.def("showPane", &AuiManager::showPane)
		.def("hidePane", &AuiManager::hidePane)
		.def("togglePane", &AuiManager::togglePane);

	py::class_t<AuiItem>(layout, "AuiItem")
		.def_init(py::init<View&, py::kwargs>(), "view"_a)
		.def("getView", &AuiItem::operator View&);

	py::class_t<AuiNotebook, Layout>(layout, "AuiNotebook")
		.def_init(layout_init, styles, key, className, style);

	auto n = "n"_a;

	py::class_t<ToolBar, Control>(layout, "ToolBar")
		.def_init(view_init, key, className, style)
		.def("addTool", &ToolBar::addTool, 
			"label"_a, "shortHelp"_a=wxEmptyString, "bitmap"_a=wxEmptyString, "onclick"_a, "toolid"_a=-1, "kind"_a=wxEmptyString)
		.def("addSeparator", &ToolBar::addSeparator)
		.def("realize", &ToolBar::realize);

	py::class_t<StatusBar, Control>(layout, "StatusBar")
		.def_init(view_init, key, className, style)
		.def("getText", &StatusBar::getText, n)
		.def("setText", &StatusBar::setText, "text"_a, n)
		.def("setFieldsCount", &StatusBar::setFieldsCount, "list"_a)
		.def("setItemWidths", &StatusBar::setItemWidths, "list"_a)
		.def("getStatusWidth", &StatusBar::getStatusWidth, n)
		.def("popStatusText", &StatusBar::popStatusText, n)
		.def("pushStatusText", &StatusBar::pushStatusText, "text"_a, n);


	auto &title_arg = "title"_a;
	auto &name_arg = "name"_a;
	auto &help_arg = "help"_a = None;
	auto &value_0 = "value"_a = 0;

	py::class_t<PropertyGrid, Control>(layout, "PropertyGrid")
		.def_init(py::init<pyobj, pyobj, pyobj, pyobj>(),
			"data"_a=None, key, className, style)
		.def("addCategory", &PropertyGrid::addCategory, title_arg)
		.def("addStringProperty", &PropertyGrid::addStringProperty, title_arg, name_arg, help_arg, "value"_a = None)
		.def("addIntProperty", &PropertyGrid::addIntProperty, title_arg, name_arg, help_arg, value_0)
		.def("addUIntProperty", &PropertyGrid::addUIntProperty, title_arg, name_arg, help_arg, value_0)
		.def("addHexProperty", &PropertyGrid::addHexProperty, title_arg, name_arg, help_arg, value_0)
		.def("addFloatProperty", &PropertyGrid::addFloatProperty, title_arg, name_arg, help_arg, value_0)
		.def("addBoolProperty", &PropertyGrid::addBoolProperty, title_arg, name_arg, help_arg, "value"_a = false)
		.def("addEnumProperty", &PropertyGrid::addEnumProperty, title_arg, name_arg, help_arg, "items"_a, "values"_a, value_0)
		.def("addFlagsProperty", &PropertyGrid::addFlagsProperty, title_arg, name_arg, help_arg, "items"_a, "values"_a = None, value_0)
		.def("addLongStringProperty", &PropertyGrid::addLongStringProperty, title_arg, name_arg, help_arg, "value"_a = None)
		.def("addArrayStringProperty", &PropertyGrid::addArrayStringProperty, title_arg, name_arg, help_arg, "values"_a)
		.def("getValues", &PropertyGrid::getValues, "data"_a = None)
		.def("setValues", &PropertyGrid::setValues)
		.def("setReadonly", &PropertyGrid::setReadonly)
		.def("bindData", &PropertyGrid::bindData)
		.def("setTwowayBinding", &PropertyGrid::setTwowayBinding, "twoway"_a = true)
		.def_readwrite("data", &PropertyGrid::m_data);

	py::class_t<ListView, Control>(layout, "ListView")
		.def_init(py::init<pyobj, pyobj, pyobj>(), key, className, style)
		.def("appendColumns", &ListView::appendColumns)
		.def("insertItems", &ListView::insertItems, "data"_a, "pos"_a = -1, "create"_a = true);

/*
	py::detail::type_record rec;
	rec.name = "KEYCODE";
	rec.scope = layout;
	PyObject *KEYCODE = py::detail::make_new_python_type(rec);
	PyObject_SetAttrString(layout.ptr(), rec.name, KEYCODE);

	// PyObject_SetAttrString(layout.ptr(), "NORMAL", PyLong_FromLong(wxACCEL_NORMAL));

#define ATTR_INT(obj, name, pre) PyObject_SetAttrString(obj, #name, PyLong_FromLong(pre##name))

#define ATTR_ACCEL(name) ATTR_INT(layout.ptr(), name, wxACCEL_)
	ATTR_ACCEL(NORMAL),
	ATTR_ACCEL(ALT),
	ATTR_ACCEL(CTRL),
	ATTR_ACCEL(SHIFT),
	ATTR_ACCEL(RAW_CTRL),
	ATTR_ACCEL(CMD);
#undef ATTR_ACCEL

#define ATTR_KEYCODE(name) ATTR_INT(KEYCODE, name, WXK_)
	ATTR_KEYCODE(CONTROL_A), ATTR_KEYCODE(CONTROL_B), ATTR_KEYCODE(CONTROL_C), ATTR_KEYCODE(CONTROL_D), ATTR_KEYCODE(CONTROL_E), ATTR_KEYCODE(CONTROL_F), ATTR_KEYCODE(CONTROL_G),
	ATTR_KEYCODE(CONTROL_H), ATTR_KEYCODE(CONTROL_I), ATTR_KEYCODE(CONTROL_J), ATTR_KEYCODE(CONTROL_K), ATTR_KEYCODE(CONTROL_L), ATTR_KEYCODE(CONTROL_M), ATTR_KEYCODE(CONTROL_N),
	ATTR_KEYCODE(CONTROL_O), ATTR_KEYCODE(CONTROL_P), ATTR_KEYCODE(CONTROL_Q), ATTR_KEYCODE(CONTROL_R), ATTR_KEYCODE(CONTROL_S), ATTR_KEYCODE(CONTROL_T),
	ATTR_KEYCODE(CONTROL_U), ATTR_KEYCODE(CONTROL_V), ATTR_KEYCODE(CONTROL_W), ATTR_KEYCODE(CONTROL_X), ATTR_KEYCODE(CONTROL_Y), ATTR_KEYCODE(CONTROL_Z),
	ATTR_KEYCODE(BACK),
	ATTR_KEYCODE(TAB),
	ATTR_KEYCODE(RETURN),
	ATTR_KEYCODE(ESCAPE),
	ATTR_KEYCODE(SPACE),
	ATTR_INT(KEYCODE, _DELETE, WXK),
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

#undef ATTR_INT*/
}