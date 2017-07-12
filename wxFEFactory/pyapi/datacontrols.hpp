#pragma once
#include "layoutbase.hpp"
#include <wx/propgrid/propgrid.h>
#include <wx/listctrl.h>


class PropertyGrid: public Control
{
public:
	template <class... Args>
	PropertyGrid(pycref data, Args ...args):
		Control(args...), m_data(data.is_none() ? py::dict() : data)
	{
		bindElem(new wxPropertyGrid(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize()));

		auto &pg = m_ctrl();
		pg.SetExtraStyle(wxPG_EX_HELP_AS_TOOLTIPS);
		pg.SetCaptionBackgroundColour(0xeeeeee);
		pg.SetMarginColour(0xeeeeee);
		pg.Bind(wxEVT_PG_CHANGED, &PropertyGrid::OnChange, this);
	}

	void OnChange(wxPropertyGridEvent &event)
	{
		m_changed = true;
		if (m_twoway)
		{
			auto p = event.GetProperty();
			m_data[p->GetName()] = getValue(event.GetProperty());
		}
	}

	void Append(wxPGProperty* property, py::object &help)
	{
		m_ctrl().Append(property);
		if (!help.is_none())
		{
			property->SetHelpString(help.cast<wxString>());
		}
	}

	void addCategory(wxcstr title) {
		m_ctrl().Append(new wxPropertyCategory(title));
	}

	void addStringProperty(wxcstr title, wxcstr name, py::object help, py::object value) {
		Append(new wxStringProperty(title, name, pywxstr(value)), help);
	}

	void addIntProperty(wxcstr title, wxcstr name, py::object help, long value = 0) {
		Append(new wxIntProperty(title, name, value), help);
	}

	void addUIntProperty(wxcstr title, wxcstr name, py::object help, u32 value = 0) {
		Append(new wxUIntProperty(title, name, value), help);
	}

	void addHexProperty(wxcstr title, wxcstr name, py::object help, u32 value = 0) {
		wxPGProperty* property = new wxUIntProperty(title, name, value);
		property->SetAttribute(wxPG_UINT_BASE, wxPG_BASE_HEX);
		// property->SetAttribute(wxPG_UINT_PREFIX, wxPG_PREFIX_0x);
		Append(property, help);
	}

	void addFloatProperty(wxcstr title, wxcstr name, py::object help, double value = 0) {
		Append(new wxFloatProperty(title, name, value), help);
	}

	void addBoolProperty(wxcstr title, wxcstr name, py::object help, bool value = false) {
		Append(new wxBoolProperty(title, name, value), help);
	}

	void addEnumProperty(wxcstr title, wxcstr name, py::object help, py::iterable py_items, py::iterable py_values, int value = 0) {
		wxArrayString labels;
		wxArrayInt values;
		addAll(labels, py_items);
		addAll(values, py_values);
		Append(new wxEnumProperty(title, name, labels, values, value), help);
	}

	void addFlagsProperty(wxcstr title, wxcstr name, py::object help, py::iterable py_items, py::object py_values, int value = 0) {
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

	void addLongStringProperty(wxcstr title, wxcstr name, py::object help, py::object value) {
		Append(new wxLongStringProperty(title, name, pywxstr(value)), help);
	}

	void addArrayStringProperty(wxcstr title, wxcstr name, py::object help, py::iterable py_values) {
		wxArrayString values;
		addAll(values, py_values);
		Append(new wxArrayStringProperty(title, name, values), help);
	}

	py::object getValue(const wxPGProperty* p) {
		const wxVariant &&value = p->GetValue();
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

	py::object getValue(wxcstr name) {
		return getValue(m_ctrl().GetPropertyByName(name));
	}

	void setValue(const wxPGProperty* p, py::object pyval) {
		wxcstr type = p->GetValueType();

		if (pyval.is_none())
		{
			return;
		}

		auto &pg = m_ctrl();

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

	void setValue(wxcstr name, py::object value) {
		return setValue(m_ctrl().GetPropertyByName(name), value);
	}

	void getValues(py::object obj)
	{
		py::dict data = obj.is_none() ? m_data : obj;

		wxPropertyGridConstIterator it = m_ctrl().GetIterator();
		for (; !it.AtEnd(); it++)
		{
			const wxPGProperty* p = *it;
			data[p->GetName()] = getValue(p);
		}
	}

	void setValues(py::dict data)
	{
		wxPropertyGridIterator it = m_ctrl().GetIterator();
		for (; !it.AtEnd(); it++)
		{
			wxPGProperty* p = *it;
			setValue(p, data[p->GetName()]);
		}
	}

	void setReadonly(wxcstr name, bool readonly = true)
	{
		m_ctrl().GetPropertyByName(name)->SetFlagRecursively(wxPG_PROP_READONLY, readonly);
	}

	/**
	* °ó¶¨Êý¾Ý
	*/
	void bindData(py::object data)
	{
		m_data = data;
		setValues(data);
	}

	void setTwowayBinding(bool twoway) {
		m_twoway = twoway;
	}

	friend void initLayout(py::module &m);

protected:
	py::dict m_data;
	bool m_changed = false;
	bool m_twoway = false;

	wxPropertyGrid& m_ctrl()
	{
		return *(wxPropertyGrid*)m_elem;
	}
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
			m_ctrl().AppendColumn(pystrcpy(text, item));
		}
	}

	void insertItems(py::iterable rows, int pos = -1, bool create = true)
	{
		wxListItem info;
		auto &li = m_ctrl();
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

protected:
	wxListView& m_ctrl()
	{
		return *(wxListView*)m_elem;
	}
};