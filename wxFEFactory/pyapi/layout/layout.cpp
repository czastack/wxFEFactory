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
#include "bars.hpp"
#include "console.h"
#include "thread.h"

void setConsoleElem(TextInput &input, TextInput &output)
{
	pyConsole.setConsoleElem((wxTextCtrl*)input.ptr(), (wxTextCtrl*)output.ptr());
}


void init_layout(py::module &m)
{
	using namespace py::literals;

	auto className = "className"_a=None;
	auto style = "style"_a=None;
	auto styles = "styles"_a=None;
	auto label = "label"_a;
	auto type = "type"_a=wxEmptyString;
	auto wxstyle = "wxstyle"_a=0;
	auto n = "n"_a;
	auto onchange = "onchange"_a;
	auto evt_reset = "reset"_a = true;

	auto view_init = py::init<pyobj, pyobj>();
	auto layout_init = py::init<pyobj, pyobj, pyobj>();

	py::module layout = m.def_submodule("layout");
	init_menu(layout);
	init_bitmap(layout);
	setattr(m, "ui", layout);

	// wx const
	ATTR_INT(layout.ptr(), HORIZONTAL, wx),
	ATTR_INT(layout.ptr(), VERTICAL, wx);

	// 为了方便，setConsoleElem 挂在外层模块，但在这里定义
	m.def("setConsoleElem", setConsoleElem, "input"_a, "output"_a);

	py::class_<View>(layout, "View")
		.def("setContextMenu", &View::setContextMenu)
		.def("setOnKeyDown", &View::setOnKeyDown)
		.def("isShow", &View::isShow)
		.def("show", &View::show, "show"_a=true)
		.def("setToolTip", &View::setToolTip)
		.def("setOnFileDrop", &View::setOnFileDrop)
		.def("setOnTextDrop", &View::setOnTextDrop)
		.def("setOnClick", &View::setOnClick)
		.def("setOnDoubleClick", &View::setOnDoubleClick)
		.def("setOnDestroy", &View::setOnDestroy)
		.def("refresh", &View::refresh)
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

	py::class_t<BaseTopLevelWindow, Layout>(layout, "BaseTopLevelWindow")
		.def("close", &BaseTopLevelWindow::close)
		.def("setOnClose", &BaseTopLevelWindow::setOnClose)
		.def("setIcon", &BaseTopLevelWindow::setIcon)
		.def_property("title", &BaseTopLevelWindow::getTitle, &BaseTopLevelWindow::setTitle)
		.def_property("size", &BaseTopLevelWindow::getSize, &BaseTopLevelWindow::setSize)
		.def_property("position", &BaseTopLevelWindow::getPosition, &BaseTopLevelWindow::setPosition);


	auto base_frame_init = py::init<wxcstr, MenuBar*, long, pyobj, pyobj, pyobj>();
	auto base_frame_wxstyle_a = "wxstyle"_a = (long)(wxDEFAULT_FRAME_STYLE | wxTAB_TRAVERSAL);
	auto menubar_a = "menubar"_a = nullptr;
	py::class_t<BaseFrame, BaseTopLevelWindow>(layout, "BaseFrame")
		.def_property("keeptop", &Window::isKeepTop, &Window::keepTop)
		.def_property_readonly("menubar", &Window::getMenuBar)
		.def_property_readonly("statusbar", &Window::getStatusBar);

	py::class_t<Window, BaseFrame>(layout, "Window")
		.def_init(base_frame_init, label, menubar_a, base_frame_wxstyle_a, styles, className, style);

	py::class_t<MDIParentFrame, BaseFrame>(layout, "MDIParentFrame")
		.def_init(base_frame_init, label, menubar_a, base_frame_wxstyle_a, styles, className, style);

	py::class_t<MDIChildFrame, BaseFrame>(layout, "MDIChildFrame")
		.def_init(base_frame_init, label, menubar_a, base_frame_wxstyle_a, styles, className, style);

	py::class_t<AuiMDIParentFrame, BaseFrame>(layout, "AuiMDIParentFrame")
		.def_init(base_frame_init, label, menubar_a, base_frame_wxstyle_a, styles, className, style);

	py::class_t<AuiMDIChildFrame, BaseTopLevelWindow>(layout, "AuiMDIChildFrame")
		.def_init(py::init<wxcstr, long, pyobj, pyobj, pyobj>(), label, base_frame_wxstyle_a, styles, className, style);

	py::class_t<HotkeyWindow, Window>(layout, "HotkeyWindow")
		.def_init(base_frame_init, label, menubar_a, base_frame_wxstyle_a, styles, className, style)
		.def("RegisterHotKey", &HotkeyWindow::RegisterHotKey, "hotkeyId"_a, "mod"_a, "keycode"_a, "onhotkey"_a)
		.def("RegisterHotKeys", &HotkeyWindow::RegisterHotKeys, "items"_a)
		.def("UnregisterHotKey", &HotkeyWindow::UnregisterHotKey, "hotkeyId"_a, "force"_a=false)
		.def_property_readonly("hotkeys", &HotkeyWindow::getHotkeys);

	py::class_t<Dialog, BaseTopLevelWindow>(layout, "Dialog")
		.def_init(py::init<wxcstr, long, pyobj, pyobj, pyobj>(),
			label, "wxstyle"_a=(long)(wxDEFAULT_DIALOG_STYLE | wxMINIMIZE_BOX), styles, className, style)
		.def("showModal", &Dialog::showModal)
		.def("endModal", &Dialog::endModal);

	py::class_t<StdModalDialog, Dialog>(layout, "StdModalDialog")
		.def_init(py::init<wxcstr, long, pyobj, pyobj, pyobj>(),
			label, "wxstyle"_a=(long)(wxDEFAULT_DIALOG_STYLE | wxMINIMIZE_BOX), styles, className, style);

	py::class_t<Vertical, Layout>(layout, "Vertical")
		.def_init(layout_init, styles, className, style);

	py::class_t<Horizontal, Layout>(layout, "Horizontal")
		.def_init(layout_init, styles, className, style);

	py::class_t<GridLayout, Layout>(layout, "GridLayout")
		.def_init(py::init<int, int, int, int, pyobj, pyobj, pyobj>(),
			"rows"_a=0, "cols"_a=2, "vgap"_a=0, "hgap"_a=0,
			styles, className, style);

	py::class_t<FlexGridLayout, Layout>(layout, "FlexGridLayout")
		.def_init(py::init<int, int, int, int, pyobj, pyobj, pyobj>(),
			"rows"_a=0, "cols"_a=2, "vgap"_a=0, "hgap"_a=0,
			styles, className, style)
		.def("AddGrowableRow", &FlexGridLayout::AddGrowableRow, "index"_a, "flex"_a=0)
		.def("RemoveGrowableRow", &FlexGridLayout::RemoveGrowableRow, "index"_a)
		.def("AddGrowableCol", &FlexGridLayout::AddGrowableCol, "index"_a, "flex"_a=0)
		.def("RemoveGrowableCol", &FlexGridLayout::RemoveGrowableCol, "index"_a)
		.def_property("flexDirection", &FlexGridLayout::GetFlexibleDirection, &FlexGridLayout::SetFlexibleDirection);

	py::class_t<ScrollView, Layout>(layout, "ScrollView")
		.def_init(py::init<bool, pyobj, pyobj, pyobj>(),
			"horizontal"_a=false, styles, className, style);

	py::class_t<SplitterWindow, Layout>(layout, "SplitterWindow")
		.def_init(py::init<bool, int, pyobj, pyobj, pyobj>(),
			"horizontal"_a = false, "sashpos"_a = 0, styles, className, style);

	py::class_t<StaticBox, Layout>(layout, "StaticBox")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj>(),
			label, styles, className, style)
		.def("getLabel", &StaticBox::getLabel)
		.def("setLabel", &StaticBox::setLabel)
		.def_property("label", &StaticBox::getLabel, &StaticBox::setLabel);

	py::class_t<BookCtrlBase, Layout>(layout, "BookCtrlBase")
		.def("getPage", &BookCtrlBase::getPage, "n"_a=-1)
		.def("getPageCount", &BookCtrlBase::getPageCount)
		.def("setPageText", &BookCtrlBase::setPageText)
		.def("getPageText", &BookCtrlBase::getPageText)
		.def_property("index", &BookCtrlBase::getSelection, &BookCtrlBase::setSelection);

	py::class_t<Notebook, BookCtrlBase>(layout, "Notebook")
		.def_init(py::init<int, pyobj, pyobj, pyobj>(), wxstyle, styles, className, style);

	py::class_t<Listbook, BookCtrlBase>(layout, "Listbook")
		.def_init(py::init<int, pyobj, pyobj, pyobj>(), wxstyle, styles, className, style);


	// controls

	py::class_t<Button, Control>(layout, "Button")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj>(),
			label, "onclick"_a=None, className, style)
		.def("setOnClick", &Button::setOnClick, "onclick"_a, evt_reset)
		.def("getLabel", &Button::getLabel)
		.def("setLabel", &Button::setLabel)
		.def("click", &Button::click)
		.def_property("label", &Button::getLabel, &Button::setLabel);

	py::class_t<ToggleButton, Control>(layout, "ToggleButton")
		.def_init(py::init<wxcstr, bool, pyobj, pyobj, pyobj>(), 
			label, "checked"_a=false, "onchange"_a=None, className, style)
		.def("getLabel", &ToggleButton::getLabel)
		.def("setLabel", &ToggleButton::setLabel)
		.def("trigger", &ToggleButton::trigger)
		.def("setOnChange", &ToggleButton::setOnChange, "onchange"_a, evt_reset)
		.def_property("label", &ToggleButton::getLabel, &ToggleButton::setLabel)
		.def_property("checked", &ToggleButton::getChecked, &ToggleButton::setChecked);

	py::class_t<CheckBox, Control>(layout, "CheckBox")
		.def_init(py::init<wxcstr, bool, bool, pyobj, pyobj, pyobj>(), 
			label, "checked"_a=false, "alignRight"_a=false, "onchange"_a=None, className, style)
		.def("getLabel", &CheckBox::getLabel)
		.def("setLabel", &CheckBox::setLabel)
		.def("trigger", &CheckBox::trigger)
		.def_property("label", &CheckBox::getLabel, &CheckBox::setLabel)
		.def_property("checked", &CheckBox::getChecked, &CheckBox::setChecked);

	py::class_t<Text, Control>(layout, "Text")
		.def_init(py::init<wxcstr, pyobj, pyobj>(), label, className, style)
		.def("getLabel", &Text::getLabel)
		.def("setLabel", &Text::setLabel)
		.def_property("label", &Text::getLabel, &Text::setLabel);

	py::class_t<TextInput, Control>(layout, "TextInput")
		.def_init(py::init<wxcstr, wxcstr, bool, bool, long, pyobj, pyobj>(),
			"value"_a=wxEmptyString, type, "readonly"_a=false, "multiline"_a=false, wxstyle, className, style)
		.def("setOnEnter", &TextInput::setOnEnter)
		.def("appendText", &TextInput::appendText)
		.def("writeText", &TextInput::writeText)
		.def("selectAll", &TextInput::selectAll)
		.def("clear", &TextInput::clear)
		.def_property("value", &TextInput::getValue, &TextInput::setValue)
		.def_property("selection", &TextInput::getSelection, &TextInput::setSelection);

	py::class_t<SearchCtrl, Control>(layout, "SearchCtrl")
		.def_init(py::init<wxcstr, bool, bool, long, pyobj, pyobj>(),
			"value"_a=wxEmptyString, "search_button"_a=true, "cancel_button"_a=true, wxstyle, className, style)
		.def("setOnSubmit", &SearchCtrl::setOnSubmit)
		.def("setOnCancel", &SearchCtrl::setOnCancel)
		.def_property("value", &SearchCtrl::getValue, &SearchCtrl::setValue);

	py::class_t<SpinCtrl, Control>(layout, "SpinCtrl")
		.def_init(py::init<wxcstr, int, int, int, pyobj, pyobj>(),
			"value"_a=wxEmptyString, "min"_a, "max"_a, "initial"_a, className, style)
		.def_property("value", &SpinCtrl::getValue, &SpinCtrl::setValue)
		.def_property("min", &SpinCtrl::getMin, &SpinCtrl::setMin)
		.def_property("max", &SpinCtrl::getMax, &SpinCtrl::setMax);

	py::class_t<ColorPicker, Control>(layout, "ColorPicker")
		.def_init(py::init<uint, pyobj, pyobj, pyobj>(),
			"color"_a=0, "onchange"_a=None, className, style)
		.def_property("color", &ColorPicker::getColor, &ColorPicker::setColor);

	auto choices = "choices"_a=None,
		onselect = "onselect"_a=None;

	py::class_<BaseControlWithItems, Control>(layout, "BaseControlWithItems")
		.def("getText", &BaseControlWithItems::getText, "pos"_a=-1)
		.def("getTexts", &BaseControlWithItems::getTexts)
		.def("setText", &BaseControlWithItems::setText, "text"_a, "pos"_a=-1)
		.def("getSelection", &BaseControlWithItems::getSelection)
		.def("setSelection", &BaseControlWithItems::setSelection, "pos"_a, "handle"_a=false)
		.def("getCount", &BaseControlWithItems::getCount)
		.def("__getitem__", &BaseControlWithItems::__getitem__)
		.def("__setitem__", &BaseControlWithItems::__setitem__)
		.def("__len__", &BaseControlWithItems::getCount)
		.def("prev", &BaseControlWithItems::prev, "handle"_a=true)
		.def("next", &BaseControlWithItems::next, "handle"_a=true)
		.def_property("text", &BaseControlWithItems::getText1, &BaseControlWithItems::setText1)
		.def_property("index", &BaseControlWithItems::getSelection, &BaseControlWithItems::doSetSelection)
		.def_property_readonly("count", &BaseControlWithItems::getCount);

	py::class_<ControlWithItems, BaseControlWithItems>(layout, "ControlWithItems")
		.def("append", &ControlWithItems::append, "text"_a)
		.def("insert", &ControlWithItems::insert, "text"_a, "pos"_a)
		.def("appendItems", &ControlWithItems::appendItems, "choices"_a)
		.def("insertItems", &ControlWithItems::insertItems, "choices"_a, "pos"_a)
		.def("setItems", &ControlWithItems::setItems, "choices"_a)
		.def("__delitem__", &ControlWithItems::pop)
		.def("pop", &ControlWithItems::pop, "pos"_a)
		.def("clear", &ControlWithItems::clear);

	py::class_t<ListBox, ControlWithItems>(layout, "ListBox")
		.def_init(py::init<pyobj, pyobj, pyobj, pyobj>(),
			choices, onselect, className, style);

	py::class_t<CheckListBox, ListBox>(layout, "CheckListBox")
		.def_init(py::init<pyobj, pyobj, pyobj, pyobj>(),
			choices, onselect, className, style)
		.def("getCheckedItems", &CheckListBox::getCheckedItems)
		.def("setCheckedItems", &CheckListBox::setCheckedItems)
		.def("checkAll", &CheckListBox::checkAll, "checked"_a=true)
		.def("reverseCheck", &CheckListBox::reverseCheck);

	py::class_t<RearrangeList, CheckListBox>(layout, "RearrangeList")
		.def_init(py::init<pyobj, pyobj, pyobj, pyobj, pyobj>(),
			choices, "order"_a=py::list(), onselect, className, style)
		.def("moveUp", &RearrangeList::moveUp)
		.def("moveDown", &RearrangeList::moveDown);

	py::class_t<Choice, ControlWithItems>(layout, "Choice")
		.def_init(py::init<pyobj, pyobj, pyobj, pyobj>(),
			choices, onselect, className, style);

	py::class_t<ComboBox, ControlWithItems>(layout, "ComboBox")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj, pyobj>(),
			type, choices, onselect, className, style)
		.def("setOnEnter", &ComboBox::setOnEnter)
		.def_property("value", &ComboBox::getValue, &ComboBox::setValue);

	py::class_t<RadioBox, BaseControlWithItems>(layout, "RadioBox")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj, pyobj>(),
			label, choices, onselect, className, style);

	py::class_t<Hr, Control>(layout, "Hr")
		.def_init(py::init<bool, pyobj, pyobj>(),
			"vertical"_a=false, className, style);

	auto pyFilePickerCtrl = py::class_t<FilePickerCtrl, Control>(layout, "FilePickerCtrl")
		.def_init(py::init<wxcstr, wxcstr, wxcstr, long, pyobj, pyobj>(),
			"path"_a=wxEmptyString, "msg"_a=wxEmptyString, "wildcard"_a=(const char*)wxFileSelectorDefaultWildcardStr,
			"wxstyle"_a=(long)(wxFLP_DEFAULT_STYLE|wxFLP_SMALL), className, style)
		.def("setOnChange", &FilePickerCtrl::setOnChange)
		.def_property("path", &FilePickerCtrl::getPath, &FilePickerCtrl::setPath)
		.ptr();

	#define ATTR_FLP_STYLE(name) ATTR_INT(pyFilePickerCtrl, name, wxFLP_)
		ATTR_FLP_STYLE(FILE_MUST_EXIST),
		ATTR_FLP_STYLE(OPEN),
		ATTR_FLP_STYLE(OVERWRITE_PROMPT),
		ATTR_FLP_STYLE(SAVE),
		ATTR_FLP_STYLE(SMALL),
		ATTR_FLP_STYLE(USE_TEXTCTRL);
	#undef ATTR_FLP_STYLE

	auto pyDirPickerCtrl = py::class_t<DirPickerCtrl, Control>(layout, "DirPickerCtrl")
		.def_init(py::init<wxcstr, wxcstr, long, pyobj, pyobj>(),
			"path"_a=wxEmptyString, "msg"_a=wxEmptyString, "wxstyle"_a=(long)(wxDIRP_DEFAULT_STYLE|wxDIRP_SMALL), className, style)
		.def("setOnChange", &DirPickerCtrl::setOnChange)
		.def_property("path", &DirPickerCtrl::getPath, &DirPickerCtrl::setPath)
		.ptr();

	#define ATTR_DIRP_STYLE(name) ATTR_INT(pyDirPickerCtrl, name, wxDIRP_)
		ATTR_DIRP_STYLE(DIR_MUST_EXIST),
		ATTR_DIRP_STYLE(SMALL),
		ATTR_DIRP_STYLE(USE_TEXTCTRL);
	#undef ATTR_FLP_STYLE


	auto pyItem = py::class_t<Item>(layout, "Item")
		.def_init(py::init<View&, py::kwargs>(), "view"_a)
		.def("getView", &AuiItem::getView);


	// aui
	py::class_t<AuiManager, Layout>(layout, "AuiManager")
		.def(py::init<>())
		.def("showPane", &AuiManager::showPane, "name"_a, "show"_a=true)
		.def("hidePane", &AuiManager::hidePane)
		.def("togglePane", &AuiManager::togglePane);

	setattr(layout, "AuiItem", pyItem);

	py::class_t<AuiNotebook, Layout>(layout, "AuiNotebook")
		.def_init(layout_init, styles, className, style)
		.def("getPage", &AuiNotebook::getPage, "n"_a=-1)
		.def("closePage", &AuiNotebook::closePage, "n"_a=-1)
		.def("closeAllPage", &AuiNotebook::closeAllPage)
		.def_property("index", &AuiNotebook::getSelection, &AuiNotebook::setSelection)
		.def_property_readonly("index", &AuiNotebook::getPageCount);


	// bars

	py::class_t<ToolBar, Layout>(layout, "ToolBar")
		.def_init(py::init<long, pyobj, pyobj, pyobj>(), "wxstyle"_a=(long)wxHORIZONTAL|wxTB_TEXT, styles, className, style)
		.def("addTool", &ToolBar::addTool, 
			"label"_a, "shortHelp"_a=wxEmptyString, "bitmap"_a=None, "onclick"_a=None, "toolid"_a=-1, "kind"_a=wxEmptyString)
		.def("addControl", &ToolBar::addControl, "view"_a, "label"_a=wxNoneString, "onclick"_a=None)
		.def("addSeparator", &ToolBar::addSeparator)
		.def("realize", &ToolBar::realize)
		.def("getToolPos", &ToolBar::getToolPos)
		.def("setToolBitmapSize", &ToolBar::setToolBitmapSize);

	py::class_t<AuiToolBar, Layout>(layout, "AuiToolBar")
		.def_init(py::init<long, pyobj, pyobj, pyobj>(), "wxstyle"_a=(long)wxAUI_TB_HORIZONTAL|wxAUI_TB_TEXT, styles, className, style)
		.def("addTool", &AuiToolBar::addTool, 
			"label"_a, "shortHelp"_a=wxEmptyString, "bitmap"_a=None, "onclick"_a=None, "toolid"_a=-1, "kind"_a=wxEmptyString)
		.def("addControl", &AuiToolBar::addControl, "view"_a, "label"_a=wxNoneString, "onclick"_a=None)
		.def("addSeparator", &AuiToolBar::addSeparator)
		.def("realize", &AuiToolBar::realize)
		.def("getToolPos", &AuiToolBar::getToolPos)
		.def("setToolBitmapSize", &AuiToolBar::setToolBitmapSize);

	py::class_t<StatusBar, Control>(layout, "StatusBar")
		.def_init(view_init, className, style)
		.def("getText", &StatusBar::getText, n)
		.def("setText", &StatusBar::setText, "text"_a, n)
		.def("setFieldsCount", &StatusBar::setFieldsCount, "list"_a)
		.def("setItemWidths", &StatusBar::setItemWidths, "list"_a)
		.def("getStatusWidth", &StatusBar::getStatusWidth, n)
		.def("popStatusText", &StatusBar::popStatusText, n)
		.def("pushStatusText", &StatusBar::pushStatusText, "text"_a, n);


	// datacontrols

	auto &title_arg = "title"_a;
	auto &name_arg = "name"_a;
	auto &help_arg = "help"_a = None;
	auto &value_0 = "value"_a = 0;

	py::class_t<PropertyGrid, Control>(layout, "PropertyGrid")
		.def_init(py::init<pyobj, pyobj, pyobj>(),
			"data"_a=None, className, style)
		.def("addCategory", &PropertyGrid::addCategory, title_arg)
		.def("addStringProperty", &PropertyGrid::addStringProperty, title_arg, name_arg, help_arg, "value"_a=None)
		.def("addIntProperty", &PropertyGrid::addIntProperty, title_arg, name_arg, help_arg, value_0)
		.def("addUIntProperty", &PropertyGrid::addUIntProperty, title_arg, name_arg, help_arg, value_0)
		.def("addHexProperty", &PropertyGrid::addHexProperty, title_arg, name_arg, help_arg, value_0)
		.def("addFloatProperty", &PropertyGrid::addFloatProperty, title_arg, name_arg, help_arg, value_0)
		.def("addBoolProperty", &PropertyGrid::addBoolProperty, title_arg, name_arg, help_arg, "value"_a=false)
		.def("addEnumProperty", &PropertyGrid::addEnumProperty, title_arg, name_arg, help_arg, "labels"_a=None, "values"_a=None, value_0)
		.def("addFlagsProperty", &PropertyGrid::addFlagsProperty, title_arg, name_arg, help_arg, "labels"_a, "values"_a=None, value_0)
		.def("addLongStringProperty", &PropertyGrid::addLongStringProperty, title_arg, name_arg, help_arg, "value"_a=None)
		.def("addArrayStringProperty", &PropertyGrid::addArrayStringProperty, title_arg, name_arg, help_arg, "values"_a)
		.def("setEnumChoices", &PropertyGrid::setEnumChoices, "name"_a, "labels"_a, "values"_a=None)
		.def("getValues", &PropertyGrid::getValues, "data"_a=None)
		.def("setValues", &PropertyGrid::setValues, "data"_a, "all"_a=false)
		.def("setReadonly", &PropertyGrid::setReadonly)
		.def("bindData", &PropertyGrid::bindData)
		.def("setOnChange", &PropertyGrid::setOnChange)
		.def("setOnHighlight", &PropertyGrid::setOnHighlight)
		.def("setOnSelected", &PropertyGrid::setOnSelected)
		.def_readwrite("data", &PropertyGrid::m_data)
		.def_readwrite("autosave", &PropertyGrid::m_autosave)
		.def_readwrite("changed", &PropertyGrid::m_changed);

	py::class_t<ListView, Control>(layout, "ListView")
		.def_init(py::init<pyobj, pyobj>(), className, style)
		.def("appendColumns", &ListView::appendColumns)
		.def("insertItems", &ListView::insertItems, "data"_a, "pos"_a = -1, "create"_a = true);

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
			if ('0' <= ch && ch <= '9' || 'A' <= ch && ch <= 'Z') {
				// 0~9, A~Z
				return ch;
			}
			else if ('a' <= ch && ch <= 'z')
			{
				return ch - 32;
			}
			return 0;
		}).ptr();

/*
	py::detail::type_record rec;
	rec.name = "KEYCODE";
	rec.scope = layout;
	PyObject *KEYCODE = py::detail::make_new_python_type(rec);
	PyObject_SetAttrString(layout.ptr(), rec.name, KEYCODE);

	// PyObject_SetAttrString(layout.ptr(), "NORMAL", PyLong_FromLong(wxACCEL_NORMAL));
*/

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


	ATTR_INT(layout.ptr(), VERTICAL, wx),
	ATTR_INT(layout.ptr(), HORIZONTAL, wx);
}