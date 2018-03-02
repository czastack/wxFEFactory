#include <wx/wx.h>
#include "controls.h"

long Text::getAlignStyle()
{
	pyobj style = getStyle(STYLE_TEXTALIGN);
	long wxstyle = 0;
	if (!style.is(None))
	{
		wxcstr align = style.cast<wxString>();
		if (align != wxNoneString) {
			if (align == wxT("center"))
			{
				wxstyle |= wxALIGN_CENTER_HORIZONTAL;
			}
			else if (align == wxT("right"))
			{
				wxstyle |= wxALIGN_RIGHT;
			}
			else if (align == wxT("left"))
			{
				wxstyle |= wxALIGN_LEFT;
			}
		}
	}
	return wxstyle;
}

void RadioBox::applyStyle()
{
	View::applyStyle();

	pyobj style;

	style = getStyle(STYLE_FLEXDIRECTION);
	if (!style.is(None))
	{
		wxcstr dir = style.cast<wxString>();
		if (dir != wxNoneString) {
			long style = ctrl().GetWindowStyle();
			if (dir == wxT("row"))
			{
				style |= wxRA_SPECIFY_ROWS;
			}
			else if (dir == wxT("column"))
			{
				style |= wxRA_SPECIFY_COLS;
			}
			ctrl().SetWindowStyle(style);
		}
	}
}

void init_controls(py::module & m)
{
	using namespace py::literals;

	auto className = "className"_a = None;
	auto style = "style"_a = None;
	auto label = "label"_a;
	auto type = "type"_a = wxEmptyString;
	auto wxstyle = "wxstyle"_a = 0;
	auto evt_fn = "fn"_a;
	auto evt_reset = "reset"_a = true;

	py::class_t<Button, Control>(m, "Button")
		.def(py::init<wxcstr, pyobj, pyobj, pyobj>(),
			label, "onclick"_a = None, className, style)
		.def("setOnClick", &Button::setOnClick, "onclick"_a, evt_reset)
		.def("getLabel", &Button::getLabel)
		.def("setLabel", &Button::setLabel)
		.def("click", &Button::click)
		.def_property("label", &Button::getLabel, &Button::setLabel);

	py::class_t<ToggleButton, Control>(m, "ToggleButton")
		.def(py::init<wxcstr, bool, pyobj, pyobj, pyobj>(),
			label, "checked"_a = false, "onchange"_a = None, className, style)
		.def("getLabel", &ToggleButton::getLabel)
		.def("setLabel", &ToggleButton::setLabel)
		.def("trigger", &ToggleButton::trigger)
		.def("setOnChange", &ToggleButton::setOnChange, "onchange"_a, evt_reset)
		.def_property("label", &ToggleButton::getLabel, &ToggleButton::setLabel)
		.def_property("checked", &ToggleButton::getChecked, &ToggleButton::setChecked);

	py::class_t<CheckBox, Control>(m, "CheckBox")
		.def(py::init<wxcstr, bool, bool, pyobj, pyobj, pyobj>(),
			label, "checked"_a = false, "alignRight"_a = false, "onchange"_a = None, className, style)
		.def("getLabel", &CheckBox::getLabel)
		.def("setLabel", &CheckBox::setLabel)
		.def("trigger", &CheckBox::trigger)
		.def_property("label", &CheckBox::getLabel, &CheckBox::setLabel)
		.def_property("checked", &CheckBox::getChecked, &CheckBox::setChecked);

	py::class_t<Text, Control>(m, "Text")
		.def(py::init<wxcstr, pyobj, pyobj>(), label, className, style)
		.def("getLabel", &Text::getLabel)
		.def("setLabel", &Text::setLabel)
		.def_property("label", &Text::getLabel, &Text::setLabel);

	py::class_t<TextInput, Control>(m, "TextInput")
		.def(py::init<wxcstr, wxcstr, bool, bool, long, pyobj, pyobj>(),
			"value"_a = wxEmptyString, type, "readonly"_a = false, "multiline"_a = false, wxstyle, className, style)
		.def("setOnEnter", &TextInput::setOnEnter, evt_fn, evt_reset)
		.def("setOnChar", &TextInput::setOnChar, evt_fn, evt_reset)
		.def("appendText", &TextInput::appendText)
		.def("writeText", &TextInput::writeText)
		.def("selectAll", &TextInput::selectAll)
		.def("clear", &TextInput::clear)
		.def_property("value", &TextInput::getValue, &TextInput::setValue)
		.def_property("selection", &TextInput::getSelection, &TextInput::setSelection);

	py::class_t<SearchCtrl, Control>(m, "SearchCtrl")
		.def(py::init<wxcstr, bool, bool, long, pyobj, pyobj>(),
			"value"_a = wxEmptyString, "search_button"_a = true, "cancel_button"_a = true, wxstyle, className, style)
		.def("setOnSubmit", &SearchCtrl::setOnSubmit, evt_fn, evt_reset)
		.def("setOnCancel", &SearchCtrl::setOnCancel, evt_fn, evt_reset)
		.def_property("value", &SearchCtrl::getValue, &SearchCtrl::setValue);

	py::class_t<SpinCtrl, Control>(m, "SpinCtrl")
		.def(py::init<wxcstr, int, int, int, pyobj, pyobj>(),
			"value"_a = wxEmptyString, "min"_a=0, "max"_a=100, "initial"_a=0, className, style)
		.def_property("value", &SpinCtrl::getValue, &SpinCtrl::setValue)
		.def_property("min", &SpinCtrl::getMin, &SpinCtrl::setMin)
		.def_property("max", &SpinCtrl::getMax, &SpinCtrl::setMax);

	py::class_t<ColorPicker, Control>(m, "ColorPicker")
		.def(py::init<uint, pyobj, pyobj, pyobj>(),
			"color"_a = 0, "onchange"_a = None, className, style)
		.def_property("color", &ColorPicker::getColor, &ColorPicker::setColor);

	auto choices = "choices"_a = None,
		onselect = "onselect"_a = None;

	py::class_<BaseControlWithItems, Control>(m, "BaseControlWithItems")
		.def("getText", &BaseControlWithItems::getText, "pos"_a = -1)
		.def("getTexts", &BaseControlWithItems::getTexts)
		.def("setText", &BaseControlWithItems::setText, "text"_a, "pos"_a = -1)
		.def("getSelection", &BaseControlWithItems::getSelection)
		.def("setSelection", &BaseControlWithItems::setSelection, "pos"_a, "handle"_a = false)
		.def("getCount", &BaseControlWithItems::getCount)
		.def("__getitem__", &BaseControlWithItems::__getitem__)
		.def("__setitem__", &BaseControlWithItems::__setitem__)
		.def("__len__", &BaseControlWithItems::getCount)
		.def("prev", &BaseControlWithItems::prev, "handle"_a = true)
		.def("next", &BaseControlWithItems::next, "handle"_a = true)
		.def_property("text", &BaseControlWithItems::getText1, &BaseControlWithItems::setText1)
		.def_property("index", &BaseControlWithItems::getSelection, &BaseControlWithItems::doSetSelection)
		.def_property_readonly("count", &BaseControlWithItems::getCount);

	py::class_<ControlWithItems, BaseControlWithItems>(m, "ControlWithItems")
		.def("append", &ControlWithItems::append, "text"_a)
		.def("insert", &ControlWithItems::insert, "text"_a, "pos"_a)
		.def("appendItems", &ControlWithItems::appendItems, "choices"_a)
		.def("insertItems", &ControlWithItems::insertItems, "choices"_a, "pos"_a)
		.def("setItems", &ControlWithItems::setItems, "choices"_a)
		.def("__delitem__", &ControlWithItems::pop)
		.def("pop", &ControlWithItems::pop, "pos"_a)
		.def("clear", &ControlWithItems::clear);

	py::class_t<ListBox, ControlWithItems>(m, "ListBox")
		.def(py::init<pyobj, pyobj, pyobj, pyobj>(),
			choices, onselect, className, style);

	py::class_t<CheckListBox, ListBox>(m, "CheckListBox")
		.def(py::init<pyobj, pyobj, pyobj, pyobj>(),
			choices, onselect, className, style)
		.def("getCheckedItems", &CheckListBox::getCheckedItems)
		.def("setCheckedItems", &CheckListBox::setCheckedItems)
		.def("checkAll", &CheckListBox::checkAll, "checked"_a = true)
		.def("reverseCheck", &CheckListBox::reverseCheck);

	py::class_t<RearrangeList, CheckListBox>(m, "RearrangeList")
		.def(py::init<pyobj, pyobj, pyobj, pyobj, pyobj>(),
			choices, "order"_a = py::list(), onselect, className, style)
		.def("moveUp", &RearrangeList::moveUp)
		.def("moveDown", &RearrangeList::moveDown);

	py::class_t<Choice, ControlWithItems>(m, "Choice")
		.def(py::init<pyobj, pyobj, pyobj, pyobj>(),
			choices, onselect, className, style);

	py::class_t<ComboBox, ControlWithItems>(m, "ComboBox")
		.def(py::init<wxcstr, pyobj, pyobj, pyobj, pyobj>(),
			type, choices, onselect, className, style)
		.def("setOnEnter", &ComboBox::setOnEnter, evt_fn, evt_reset)
		.def("autoComplete", &ComboBox::autoComplete)
		.def_property("value", &ComboBox::getValue, &ComboBox::setValue);

	py::class_t<RadioBox, BaseControlWithItems>(m, "RadioBox")
		.def(py::init<wxcstr, pyobj, pyobj, pyobj, pyobj>(),
			label, choices, onselect, className, style);

	py::class_t<Hr, Control>(m, "Hr")
		.def(py::init<bool, pyobj, pyobj>(),
			"vertical"_a = false, className, style);

	auto pyFilePickerCtrl = py::class_t<FilePickerCtrl, Control>(m, "FilePickerCtrl")
		.def(py::init<wxcstr, wxcstr, wxcstr, long, pyobj, pyobj>(),
			"path"_a = wxEmptyString, "msg"_a = wxEmptyString, "wildcard"_a = (const char*)wxFileSelectorDefaultWildcardStr,
			"wxstyle"_a = (long)(wxFLP_DEFAULT_STYLE | wxFLP_SMALL), className, style)
		.def("setOnChange", &FilePickerCtrl::setOnChange, evt_fn, evt_reset)
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

	auto pyDirPickerCtrl = py::class_t<DirPickerCtrl, Control>(m, "DirPickerCtrl")
		.def(py::init<wxcstr, wxcstr, long, pyobj, pyobj>(),
			"path"_a = wxEmptyString, "msg"_a = wxEmptyString, "wxstyle"_a = (long)(wxDIRP_DEFAULT_STYLE | wxDIRP_SMALL), className, style)
		.def("setOnChange", &DirPickerCtrl::setOnChange, evt_fn, evt_reset)
		.def_property("path", &DirPickerCtrl::getPath, &DirPickerCtrl::setPath)
		.ptr();

#define ATTR_DIRP_STYLE(name) ATTR_INT(pyDirPickerCtrl, name, wxDIRP_)
	ATTR_DIRP_STYLE(DIR_MUST_EXIST),
		ATTR_DIRP_STYLE(SMALL),
		ATTR_DIRP_STYLE(USE_TEXTCTRL);
#undef ATTR_FLP_STYLE
}
