#pragma once
#include "layoutbase.hpp"
#include <wx/propgrid/propgrid.h>
#include <wx/listctrl.h>


class PropertyGrid: public Control
{
public:
	template <class... Args>
	PropertyGrid(pycref data, Args ...args):
		Control(args...), m_data(data.is_none() ? py::dict() : data), m_onchange(None)
	{
		bindElem(new wxPropertyGrid(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize()));

		auto &pg = ctrl();
		pg.SetExtraStyle(wxPG_EX_HELP_AS_TOOLTIPS);
		pg.SetCaptionBackgroundColour(0xeeeeee);
		pg.SetMarginColour(0xeeeeee);
		pg.Bind(wxEVT_PG_CHANGING, &PropertyGrid::OnChange, this);
	}

	void OnChange(wxPropertyGridEvent &event)
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

	template <typename EventTag>
	void bindEvt(const EventTag& eventType, pycref fn)
	{
		if (!fn.is_none())
		{
			fn.inc_ref();
			((wxEvtHandler*)m_elem)->Bind(eventType, [fn, this](auto &event) {
				handleEvent(fn, event);
			});
		}
	}

	void handleEvent(pycref fn, wxPropertyGridEvent &event)
	{
		pycref ret = pyCall(fn, this, event.GetPropertyName());
		if (!PyObject_IsTrue(ret.ptr()))
		{
			event.Skip();
		}
	}

	void setOnchange(pycref onchang)
	{
		m_onchange = onchang;
	}

	void setOnhighlight(pycref fn)
	{
		bindEvt(wxEVT_PG_HIGHLIGHTED, fn);
	}

	void setOnselected(pycref fn)
	{
		bindEvt(wxEVT_PG_SELECTED, fn);
	}

	void Append(wxPGProperty* property, pycref help)
	{
		ctrl().Append(property);
		if (!help.is_none())
		{
			property->SetHelpString(help.cast<wxString>());
		}
	}

	void addCategory(wxcstr title) {
		ctrl().Append(new wxPropertyCategory(title));
	}

	void addStringProperty(wxcstr title, wxcstr name, pycref help, pycref value) {
		Append(new wxStringProperty(title, name, pywxstr(value)), help);
	}

	void addIntProperty(wxcstr title, wxcstr name, pycref help, long value = 0) {
		Append(new wxIntProperty(title, name, value), help);
	}

	void addUIntProperty(wxcstr title, wxcstr name, pycref help, u32 value = 0) {
		Append(new wxUIntProperty(title, name, value), help);
	}

	void addHexProperty(wxcstr title, wxcstr name, pycref help, u32 value = 0) {
		wxPGProperty* property = new wxUIntProperty(title, name, value);
		property->SetAttribute(wxPG_UINT_BASE, wxPG_BASE_HEX);
		// property->SetAttribute(wxPG_UINT_PREFIX, wxPG_PREFIX_0x);
		Append(property, help);
	}

	void addFloatProperty(wxcstr title, wxcstr name, pycref help, double value = 0) {
		Append(new wxFloatProperty(title, name, value), help);
	}

	void addBoolProperty(wxcstr title, wxcstr name, pycref help, bool value = false) {
		Append(new wxBoolProperty(title, name, value), help);
	}

	void addEnumProperty(wxcstr title, wxcstr name, pycref help, pyobj labels, pyobj values, int value = 0) {
		prepareOptions(labels, values, true);
		Append(new wxEnumProperty(title, name, py::cast<wxArrayString>(labels), py::cast<wxArrayInt>(values), value), help);
	}

	void addFlagsProperty(wxcstr title, wxcstr name, pycref help, pycref py_items, pycref py_values, int value = 0) {
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

	void addLongStringProperty(wxcstr title, wxcstr name, pycref help, pycref value) {
		Append(new wxLongStringProperty(title, name, pywxstr(value)), help);
	}

	void addArrayStringProperty(wxcstr title, wxcstr name, pycref help, const py::iterable &py_values) {
		wxArrayString values;
		addAll(values, py_values);
		Append(new wxArrayStringProperty(title, name, values), help);
	}

	void setEnumChoices(wxcstr name, pyobj labels, pyobj values)
	{
		wxPGProperty *p = ctrl().GetPropertyByName(name);
		if (wxIsKindOf(p, wxEnumProperty))
		{
			prepareOptions(labels, values, true);
			wxPGChoices choices(py::cast<wxArrayString>(labels), py::cast<wxArrayInt>(values));
			((wxEnumProperty*)p)->SetChoices(choices);
		}
	}

	pyobj getValue(const wxVariant& value) {
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

	pyobj getValue(const wxPGProperty* p) {
		return getValue(p->GetValue());
	}

	pyobj getValue(wxcstr name) {
		return getValue(ctrl().GetPropertyByName(name));
	}

	void setValue(const wxPGProperty* p, pycref pyval) {
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

	void setValue(wxcstr name, pycref value) {
		return setValue(ctrl().GetPropertyByName(name), value);
	}

	pyobj getValues(pycref obj)
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

	void setValues(pycref data, bool all=false)
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

	void setReadonly(wxcstr name, bool readonly = true)
	{
		ctrl().GetPropertyByName(name)->SetFlagRecursively(wxPG_PROP_READONLY, readonly);
	}

	/**
	* 绑定数据
	*/
	void bindData(pycref data)
	{
		m_data = data;
		setValues(data, true);
	}

	wxString getSelectedName()
	{
		wxPGProperty* p = ctrl().GetSelection();
		if (p)
		{
			return p->GetName();
		}
		return wxNoneString;
	}

	wxPropertyGrid& ctrl()
	{
		return *(wxPropertyGrid*)m_elem;
	}

	friend void init_layout(py::module &m);

protected:
	pyobj m_data; // py::dict
	pyobj m_onchange;
	bool m_changed = false;
	bool m_autosave = false;
};


class ListView : public Control
{
public:
	template <class... Args>
	ListView(Args ...args) :
		Control(args...)
	{
		bindElem(new wxListView(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize()));
	}

	void appendColumns(py::iterable columns)
	{
		wxString text;
		for (auto &item : columns) {
			ctrl().AppendColumn(pystrcpy(text, item));
		}
	}

	void insertItems(const py::iterable &rows, int pos = -1, bool create = true)
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
			for (auto &item : py::reinterpret_steal<py::iterable>(cols)) {
				pystrcpy(info.m_text, item);
				li.SetItem(info);
				++info.m_col;
			}
			++info.m_itemId;
		}
	}

	wxListView& ctrl()
	{
		return *(wxListView*)m_elem;
	}
};