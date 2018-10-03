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


/**
 * handle 是否触发事件处理
 */

auto ItemContainer::setSelection(int n, bool handle)
{
	doSetSelection(n);
	if (handle)
	{
		triggerSelectEvent();
	}
	return this;
}

wxString ItemContainer::getText(int pos)
{
	if (pos == -1)
	{
		pos = getSelection();
	}
	if (pos != -1)
	{
		return doGetText(pos);
	}
	return wxNoneString;
}

void ItemContainer::setText(wxcstr text, int pos)
{
	if (pos == -1)
	{
		pos = getSelection();
	}
	if (pos != -1)
	{
		doSetText(pos, text);
	}
}

pyobj ItemContainer::getTexts()
{
	const wxArrayString &textArray = ctnr().GetStrings();
	py::list list;
	for (wxcstr text : textArray)
	{
		list.append(text);
	}
	return list;
}

void ItemContainer::prev(bool handle)
{
	if (!getCount())
	{
		return;
	}

	int pos = getSelection();
	if (pos == 0)
	{
		pos = getCount();
	}

	setSelection(pos - 1, handle);
}

void ItemContainer::next(bool handle)
{
	if (!getCount())
	{
		return;
	}

	int pos = getSelection();
	if (pos == getCount() - 1)
	{
		pos = -1;
	}

	setSelection(pos + 1, handle);
}


pyobj CheckListBox::getCheckedItems()
{
	wxArrayInt items;
	ctrl().GetCheckedItems(items);
	return asPyList(items);
}

void CheckListBox::setCheckedItems(pyobj list)
{
	auto &el = ctrl();
	for (uint i = 0; i < el.GetCount(); ++i)
	{
		el.Check(i, false);
	}
	for (auto &item : list) {
		el.Check(item.cast<int>(), true);
	}
}

void CheckListBox::checkAll(bool checked)
{
	auto &el = ctrl();
	for (uint i = 0; i < el.GetCount(); ++i)
	{
		el.Check(i, checked);
	}
}

void CheckListBox::reverseCheck()
{
	auto &el = ctrl();
	for (uint i = 0; i < el.GetCount(); ++i)
	{
		el.Check(i, !el.IsChecked(i));
	}
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
		.def("click", &Button::click);

	auto pyBitmapButton = py::class_t<BitmapButton, Button>(m, "BitmapButton")
		.def(py::init<pycref, pyobj, pyobj, pyobj>(),
			"src"_a, "onclick"_a = None, className, style);

	py::setattr(m, "ImageButton", pyBitmapButton);

	py::class_t<ToggleButton, Control>(m, "ToggleButton")
		.def(py::init<wxcstr, bool, pyobj, pyobj, pyobj>(),
			label, "checked"_a = false, "onchange"_a = None, className, style)
		.def("toggle", &ToggleButton::toggle)
		.def("setOnChange", &ToggleButton::setOnChange, "onchange"_a, evt_reset)
		.def_property("checked", &ToggleButton::getChecked, &ToggleButton::setChecked);

	py::class_t<CheckBox, Control>(m, "CheckBox")
		.def(py::init<wxcstr, bool, bool, pyobj, pyobj, pyobj>(),
			label, "checked"_a = false, "alignRight"_a = false, "onchange"_a = None, className, style)
		.def("toggle", &CheckBox::toggle)
		.def_property("checked", &CheckBox::getChecked, &CheckBox::setChecked);

	py::class_t<Img, Control>(m, "Img")
		.def(py::init<pycref, pyobj, pyobj>(), "src"_a, className, style)
		.def_property("scalemode",
			[](Img *self) { return (int)self->ctrl().GetScaleMode(); },
			[](Img *self, int value) { return self->ctrl().SetScaleMode((wxStaticBitmap::ScaleMode)value); });

	py::class_t<Text, Control>(m, "Text")
		.def(py::init<wxcstr, pyobj, pyobj>(), label, className, style);

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
		.def(py::init<wxcstr, int, int, int, long, pyobj, pyobj>(),
			"value"_a = wxEmptyString, "min"_a=0, "max"_a=100, "initial"_a=0, wxstyle, className, style)
		.def("setOnChange", &SpinCtrl::setOnChange, evt_fn, evt_reset)
		.def("setOnEnter", &SpinCtrl::setOnEnter, evt_fn, evt_reset)
		.def_property("value", 
			[](SpinCtrl *self) { return self->ctrl().GetValue(); },
			[](SpinCtrl *self, int value) { return self->ctrl().SetValue(value); })
		.def_property("min",
			[](SpinCtrl *self) { return self->ctrl().GetMin(); },
			[](SpinCtrl *self, int value) { return self->ctrl().SetMin(value); })
		.def_property("max",
			[](SpinCtrl *self) { return self->ctrl().GetMax(); },
			[](SpinCtrl *self, int value) { return self->ctrl().SetMax(value); });

	py::class_t<ColorPicker, Control>(m, "ColorPicker")
		.def(py::init<uint, pyobj, pyobj, pyobj>(),
			"color"_a = 0, "onchange"_a = None, className, style)
		.def_property("color", &ColorPicker::getColor, &ColorPicker::setColor);

	auto choices = "choices"_a = None,
		onselect = "onselect"_a = None;

	py::class_<ItemContainer, Control>(m, "ItemContainer")
		.def("getText", &ItemContainer::getText, "pos"_a = -1)
		.def("getTexts", &ItemContainer::getTexts)
		.def("setText", &ItemContainer::setText, "text"_a, "pos"_a = -1)
		.def("getSelection", &ItemContainer::getSelection)
		.def("setSelection", &ItemContainer::setSelection, "pos"_a, "handle"_a = false)
		.def("getCount", &ItemContainer::getCount)
		.def("__getitem__", &ItemContainer::__getitem__)
		.def("__setitem__", &ItemContainer::__setitem__)
		.def("__len__", &ItemContainer::getCount)
		.def("prev", &ItemContainer::prev, "handle"_a = true)
		.def("next", &ItemContainer::next, "handle"_a = true)
		.def_property("text", &ItemContainer::getText1, &ItemContainer::setText1)
		.def_property("index", &ItemContainer::getSelection, &ItemContainer::doSetSelection)
		.def_property_readonly("count", &ItemContainer::getCount);

	py::class_<ControlWithItems, ItemContainer>(m, "ControlWithItems")
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
		.def(py::init<long, pyobj, pyobj, pyobj, pyobj>(),
			"wxstyle"_a=(long)wxCB_READONLY, choices, onselect, className, style)
		.def("setOnEnter", &ComboBox::setOnEnter, evt_fn, evt_reset)
		.def("auto_complete", &ComboBox::auto_complete)
		.def("popup", [](ComboBox *self) { self->ctrl().Popup(); })
		.def("dismiss", [](ComboBox *self) { self->ctrl().Dismiss(); })
		.def_property("value", &ComboBox::getValue, &ComboBox::setValue);

	py::class_t<RadioBox, ItemContainer>(m, "RadioBox")
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

	auto pyDirPickerCtrl = py::class_t<DirPickerCtrl, Control>(m, "DirPickerCtrl")
		.def(py::init<wxcstr, wxcstr, long, pyobj, pyobj>(),
			"path"_a = wxEmptyString, "msg"_a = wxEmptyString, "wxstyle"_a = (long)(wxDIRP_DEFAULT_STYLE | wxDIRP_SMALL), className, style)
		.def("setOnChange", &DirPickerCtrl::setOnChange, evt_fn, evt_reset)
		.def_property("path", &DirPickerCtrl::getPath, &DirPickerCtrl::setPath)
		.ptr();

	auto text = "text"_a;
	auto image = "image"_a = -1,
		selectedImage = "selectedImage"_a = -1,
		data = "data"_a = None,
		pos = "pos"_a = -1;

	py::class_t<TreeCtrl, Control>(m, "TreeCtrl")
		.def(py::init<long, pyobj, pyobj>(),
			"wxstyle"_a=0, className, style)
		.def("AssignImageList", [](TreeCtrl *self, wxImageList *imageList) {
			self->ctrl().AssignImageList(imageList);
		})
		.def("AddRoot", [](TreeCtrl *self, wxcstr text, int image, int selectedImage, pycref data) {
			return self->ctrl().AddRoot(text, image, selectedImage, data.is_none() ? NULL: new PyTreeItemData(data));
		}, text, image, selectedImage, data)
		.def("InsertItem", [](TreeCtrl *self, const wxTreeItemId& parent, wxcstr text, int image, int selectedImage, pycref data, int pos) {
			return self->ctrl().InsertItem(parent, pos, text, image, selectedImage, data.is_none() ? NULL : new PyTreeItemData(data));
		}, "parent"_a, text, image, selectedImage, data, pos)

		.def("GetItemData", [](TreeCtrl *self, const wxTreeItemId& item) { 
			PyTreeItemData *data = (PyTreeItemData*)self->ctrl().GetItemData(item);
			return data ? data->GetData(): None;
		})

		.def("Delete", [](TreeCtrl *self, const wxTreeItemId& item) { self->ctrl().Delete(item); })
		.def("DeleteChildren", [](TreeCtrl *self, const wxTreeItemId& item) { self->ctrl().DeleteChildren(item); })
		.def("DeleteAllItems", [](TreeCtrl *self) { self->ctrl().DeleteAllItems(); })

		.def("Expand", [](TreeCtrl *self, const wxTreeItemId& item) { self->ctrl().Expand(item); })
		.def("ExpandAllChildren", [](TreeCtrl *self, const wxTreeItemId& item) { self->ctrl().ExpandAllChildren(item); })
		.def("ExpandAll", [](TreeCtrl *self) { self->ctrl().ExpandAll(); })
		.def("Collapse", [](TreeCtrl *self, const wxTreeItemId& item) { self->ctrl().Collapse(item); })
		.def("CollapseAllChildren", [](TreeCtrl *self, const wxTreeItemId& item) { self->ctrl().CollapseAllChildren(item); })
		.def("CollapseAll", [](TreeCtrl *self) { self->ctrl().CollapseAll(); })
		.def("CollapseAndReset", [](TreeCtrl *self, const wxTreeItemId& item) { self->ctrl().CollapseAndReset(item); })
		.def("Toggle", [](TreeCtrl *self, const wxTreeItemId& item) { self->ctrl().Toggle(item); })

		.def("Unselect", [](TreeCtrl *self) { self->ctrl().Unselect(); })
		.def("UnselectAll", [](TreeCtrl *self) { self->ctrl().UnselectAll(); })
		.def("SelectItem", [](TreeCtrl *self, const wxTreeItemId& item, bool select = true) { self->ctrl().SelectItem(item, select); }, "item"_a, "select"_a=true)
		.def("SelectChildren", [](TreeCtrl *self, const wxTreeItemId& parent) { self->ctrl().SelectChildren(parent); })
		.def("ToggleItemSelection", [](TreeCtrl *self, const wxTreeItemId& item) { self->ctrl().ToggleItemSelection(item); })
		.def("setOnItemActivated", &TreeCtrl::setOnItemActivated, evt_fn, evt_reset)

		/*.def("GetCount", [](TreeCtrl *self) { return self->ctrl().GetCount(); })
		.def("GetIndent", [](TreeCtrl *self) { return self->ctrl().GetIndent(); })
		.def("SetIndent", [](TreeCtrl *self, unsigned int indent) { self->ctrl().SetIndent(indent); })
		.def("GetSpacing", [](TreeCtrl *self) { return self->ctrl().GetSpacing(); })
		.def("SetSpacing", [](TreeCtrl *self, unsigned int spacing) { self->ctrl().SetSpacing(spacing); })*/
		
		.def_property_readonly("count", [](TreeCtrl *self) { return self->ctrl().GetCount(); })
		.def_property("indent", 
			[](TreeCtrl *self) { return self->ctrl().GetIndent(); },
			[](TreeCtrl *self, unsigned int indent) { self->ctrl().SetIndent(indent); }
		)
		.def_property("spacing",
			[](TreeCtrl *self) { return self->ctrl().GetSpacing(); },
			[](TreeCtrl *self, unsigned int spacing) { self->ctrl().SetSpacing(spacing); }
		);

		py::class_<wxTreeEvent, wxEvent>(m, "TreeEvent")
			.def_property_readonly("item", &wxTreeEvent::GetItem);
}