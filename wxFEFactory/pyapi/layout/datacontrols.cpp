#include <wx/wx.h>
#include "datacontrols.h"

void PropertyGrid::OnChange(wxPropertyGridEvent & event)
{
	m_changed = true;
	if (m_autosave)
	{
		auto p = event.GetProperty();
		pycref name = py::cast(p->GetName());
		pycref value = getValue(event.GetValue());
		if (m_onchange != None)
		{
			pycref ret = pyCall(m_onchange, this, name, value);
			if (ret.ptr() == Py_False)
			{
				// 返回False忽略当前改动
				event.Veto();
				return;
			}
			else if (ret.ptr() != Py_True)
			{
				event.Skip();
			}
		}
		m_data[name] = value;
	}
	else {
		event.Skip();
	}
}

void PropertyGrid::addFlagsProperty(wxcstr title, wxcstr name, pycref help, pycref py_items, pycref py_values, int value) {
	wxArrayString labels;
	wxArrayInt values;
	addAll(labels, py_items);
	if (!py_values.is_none())
	{
		addAll(values, py::iterable(py_values));
	}
	else
	{
		for (uint i = 0; i < labels.size(); ++i)
		{
			values.Add(1 << i);
		}
	}
	wxPGProperty* property = new wxFlagsProperty(title, name, labels, values, value);
	property->SetAttribute(wxPG_BOOL_USE_CHECKBOX, true);
	Append(property, help);
}

pyobj PropertyGrid::getValue(const wxVariant & value) {
	wxcstr type = value.GetType();
	if (type == "long")
		return py::cast(value.GetLong());
	else if (type == "string")
		return py::cast(value.GetString());
	else if (type == "bool")
		return py::cast(value.GetBool());
	else if (type == "arrstring") {
		const wxArrayString &&list = value.GetArrayString();
		py::list pylist(list.size());
		int i = 0;
		for (auto &e : list)
		{
			pylist[i++] = e;
		}
		return pylist;
	}
	return None;
}

void PropertyGrid::setValue(const wxPGProperty * p, pycref pyval) {
	/*
	The built-in types are:
	"bool"
	"char"
	"datetime"
	"double"
	"list"
	"long"
	"longlong"
	"string"
	"ulonglong"
	"arrstring"
	"void*"
	If the variant is null, the value type returned is the string "null" (not the empty string).
	*/

	wxcstr type = p->GetValueType();
	auto &pg = ctrl();

	if (pyval.is_none())
	{
		pg.SetPropertyValue(p, wxNoneString);
		return;
	}

	if (type != "null")
	{
		if (type == "long")
			pg.SetPropertyValue(p, pyval.cast<long>());
		else if (type == "string")
			pg.SetPropertyValue(p, pyval.cast<wxString>());
		else if (type == "bool")
			pg.SetPropertyValue(p, pyval.cast<bool>());
		else if (type == "arrstring") {
			py::list pylist(pyval);
			wxArrayString list;
			list.SetCount(pylist.size());
			int i = 0;
			for (auto &e : pylist)
			{
				list[i++] = pyval.cast<wxString>();
			}
			pg.SetPropertyValue(p, list);
		}
	}
	else
	{
		if (wxIsKindOf(p, wxUIntProperty) || wxIsKindOf(p, wxIntProperty))
			pg.SetPropertyValue(p, pyval.cast<long>());
		else if (wxIsKindOf(p, wxStringProperty) || wxIsKindOf(p, wxLongStringProperty))
			pg.SetPropertyValue(p, pyval.cast<wxString>());
		else if (wxIsKindOf(p, wxBoolProperty))
			pg.SetPropertyValue(p, pyval.cast<bool>());
		else if (wxIsKindOf(p, wxArrayStringProperty)) {
			py::list pylist(pyval);
			wxArrayString list;
			list.SetCount(pylist.size());
			int i = 0;
			for (auto &e : pylist)
			{
				list[i++] = pyval.cast<wxString>();
			}
			pg.SetPropertyValue(p, list);
		}
	}
}

pyobj PropertyGrid::getValues(pycref obj)
{
	pycref data = obj.is_none() ? m_data : obj;

	wxPropertyGridConstIterator it = ctrl().GetIterator();
	for (; !it.AtEnd(); ++it)
	{
		const wxPGProperty* p = *it;
		data[p->GetName()] = getValue(p);
	}
	return data;
}

void PropertyGrid::setValues(pycref data, bool all)
{
	wxString text;

	if (all)
	{
		wxPropertyGridIterator it = ctrl().GetIterator();
		for (; !it.AtEnd(); ++it)
		{
			wxPGProperty* p = *it;
			setValue(p, pyDictGet(data, p->GetName()));
		}
	}
	else
	{
		for (auto &item : data) {
			pystrcpy(text, item);
			wxPGProperty* p = ctrl().GetPropertyByName(text);
			if (p)
			{
				setValue(p, data[item]);
			}
		}
	}
}

void ListView::appendColumns(py::iterable columns, pycref widths)
{
	wxString text;
	int width_len = widths.is_none() ? 0 : py::len(widths);
	const py::sequence &width_list = width_len ? py::reinterpret_borrow<py::sequence>(widths) : None;
	int i = 0;
	for (auto &item : columns) {
		ctrl().AppendColumn(pystrcpy(text, item), wxLIST_FORMAT_LEFT, i < width_len ? width_list[i].cast<int>(): -1);
		i++;
	}
}

auto &ListView::appendColumn(wxString &text, int align, int width)
{
	ctrl().AppendColumn(text, (wxListColumnFormat)align, width);
	return *this;
}

void ListView::insertItems(const py::iterable & rows, int pos, bool create)
{
	wxListItem info;
	auto &li = ctrl();
	info.m_mask = wxLIST_MASK_TEXT;
	info.m_itemId = pos != -1 ? pos : li.GetItemCount();
	if (!create && pos == -1)
		create = true;

	for (auto &cols : rows) {
		info.m_col = 0;
		if (create)
			li.InsertItem(info);
		for (auto &item : cols) {
			pystrcpy(info.m_text, item);
			li.SetItem(info);
			++info.m_col;
		}
		++info.m_itemId;
	}
}

void init_datacontrols(py::module &m)
{
	using namespace py::literals;

	auto className = "className"_a = None;
	auto style = "style"_a = None;

	auto &title_arg = "title"_a;
	auto &name_arg = "name"_a;
	auto &help_arg = "help"_a = None;
	auto &value_0 = "value"_a = 0;
	auto evt_reset = "reset"_a = true;

	py::class_t<PropertyGrid, Control>(m, "PropertyGrid")
		.def_init(py::init<pyobj, pyobj, pyobj>(),
			"data"_a = None, className, style)
		.def("addCategory", &PropertyGrid::addCategory, title_arg)
		.def("addStringProperty", &PropertyGrid::addStringProperty, title_arg, name_arg, help_arg, "value"_a = None)
		.def("addIntProperty", &PropertyGrid::addIntProperty, title_arg, name_arg, help_arg, value_0)
		.def("addUIntProperty", &PropertyGrid::addUIntProperty, title_arg, name_arg, help_arg, value_0)
		.def("addHexProperty", &PropertyGrid::addHexProperty, title_arg, name_arg, help_arg, value_0)
		.def("addFloatProperty", &PropertyGrid::addFloatProperty, title_arg, name_arg, help_arg, value_0)
		.def("addBoolProperty", &PropertyGrid::addBoolProperty, title_arg, name_arg, help_arg, "value"_a = false)
		.def("addEnumProperty", &PropertyGrid::addEnumProperty, title_arg, name_arg, help_arg, "labels"_a = None, "values"_a = None, value_0)
		.def("addFlagsProperty", &PropertyGrid::addFlagsProperty, title_arg, name_arg, help_arg, "labels"_a, "values"_a = None, value_0)
		.def("addLongStringProperty", &PropertyGrid::addLongStringProperty, title_arg, name_arg, help_arg, "value"_a = None)
		.def("addArrayStringProperty", &PropertyGrid::addArrayStringProperty, title_arg, name_arg, help_arg, "values"_a)
		.def("setEnumChoices", &PropertyGrid::setEnumChoices, "name"_a, "labels"_a, "values"_a = None)
		.def("getValues", &PropertyGrid::getValues, "data"_a = None)
		.def("setValues", &PropertyGrid::setValues, "data"_a, "all"_a = false)
		.def("setReadonly", &PropertyGrid::setReadonly)
		.def("bindData", &PropertyGrid::bindData)
		.def("setOnChange", &PropertyGrid::setOnChange)
		.def("setOnHighlight", &PropertyGrid::setOnHighlight)
		.def("setOnSelected", &PropertyGrid::setOnSelected)
		.def_readwrite("data", &PropertyGrid::m_data)
		.def_readwrite("autosave", &PropertyGrid::m_autosave)
		.def_readwrite("changed", &PropertyGrid::m_changed);

	auto pyListView = py::class_t<ListView, Control>(m, "ListView")
		.def_init(py::init<pyobj, pyobj>(), className, style)
		.def("appendColumns", &ListView::appendColumns, "columns"_a, "widths"_a=None)
		.def("appendColumn", &ListView::appendColumn, "text"_a, "align"_a=(int)wxLIST_FORMAT_LEFT, "width"_a=-1)
		.def("insertItems", &ListView::insertItems, "data"_a, "pos"_a=-1, "create"_a=true)
		.def("enableCheckboxes", &ListView::enableCheckboxes, "enabled"_a=true)
		.def("isItemChecked", &ListView::isItemChecked, "item"_a)
		.def("checkItem", &ListView::checkItem, "item"_a, "checked"_a=true)
		.def("setOnItemSelected", &ListView::setOnItemSelected, "onselect"_a, evt_reset)
		.def("setOnItemDeselected", &ListView::setOnItemDeselected, "ondeselect"_a, evt_reset)
		.def("setOnItemChecked", &ListView::setOnItemChecked, "oncheck"_a, evt_reset)
		.def("setOnItemUnchecked", &ListView::setOnItemUnchecked, "onuncheck"_a, evt_reset);
	
	ATTR_INT(pyListView.ptr(), LEFT, wxLIST_FORMAT_),
	ATTR_INT(pyListView.ptr(), RIGHT, wxLIST_FORMAT_),
	ATTR_INT(pyListView.ptr(), CENTER, wxLIST_FORMAT_);

	py::class_<wxListEvent, wxEvent>(m, "ListEvent")
		.def_property_readonly("keycode", &wxListEvent::GetKeyCode)
		.def_property_readonly("index", &wxListEvent::GetIndex)
		.def_property_readonly("column", &wxListEvent::GetColumn);
}