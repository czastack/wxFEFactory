#pragma once
#include "layoutbase.h"
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

	void OnChange(wxPropertyGridEvent &event);

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

	void setOnChange(pycref onchang)
	{
		m_onchange = onchang;
	}

	void setOnHighlight(pycref fn)
	{
		bindEvt(wxEVT_PG_HIGHLIGHTED, fn);
	}

	void setOnSelected(pycref fn)
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

	void addFlagsProperty(wxcstr title, wxcstr name, pycref help, pycref py_items, pycref py_values, int value = 0);

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

	pyobj getValue(const wxVariant& value);

	pyobj getValue(const wxPGProperty* p) {
		return getValue(p->GetValue());
	}

	pyobj getValue(wxcstr name) {
		return getValue(ctrl().GetPropertyByName(name));
	}

	void setValue(const wxPGProperty* p, pycref pyval);

	void setValue(wxcstr name, pycref value) {
		return setValue(ctrl().GetPropertyByName(name), value);
	}

	pyobj getValues(pycref obj);

	void setValues(pycref data, bool all = false);

	void setReadonly(wxcstr name, bool readonly = true)
	{
		ctrl().GetPropertyByName(name)->SetFlagRecursively(wxPG_PROP_READONLY, readonly);
	}

	/**
	* ������
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

	void insertItems(const py::iterable &rows, int pos = -1, bool create = true);

	wxListView& ctrl()
	{
		return *(wxListView*)m_elem;
	}
};