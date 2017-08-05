#pragma once
#include "layoutbase.h"
#include <wx/button.h>
#include <wx/stattext.h>
#include <wx/spinctrl.h>
#include <wx/srchctrl.h>
#include <wx/statline.h>
#include <wx/filepicker.h>
#include "wxpatch.h"


class Button : public Control
{
public:
	template <class... Args>
	Button(wxcstr label, pyobj &onclick, Args ...args) : Control(args...)
	{
		bindElem(new wxButton(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize()));
		setOnclick(onclick);
	}

	void setOnclick(pyobj &fn)
	{
		bindEvt(wxEVT_BUTTON, fn);
	}

	wxButton& ctrl()
	{
		return *(wxButton*)m_elem;
	}
};


class CheckBox : public Control
{
public:
	template <class... Args>
	CheckBox(wxcstr label, bool checked, bool alignRight, pyobj &onchange, Args ...args) :
		Control(args...), m_change(onchange)
	{
		long style = 0L;
		if (alignRight)
		{
			style |= wxALIGN_RIGHT;
		}

		bindElem(new wxCheckBox(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize(), style));
		if (checked)
		{
			setChecked(true);
		}
		m_elem->Bind(wxEVT_CHECKBOX, &CheckBox::onChange, this);
	}

	void trigger()
	{
		setChecked(!getChecked());
		addPendingEvent(wxEVT_CHECKBOX);
	}

	void setChecked(bool checked)
	{
		ctrl().SetValue(checked);
	}

	bool getChecked()
	{
		return ctrl().GetValue();
	}

	void onChange(wxCommandEvent & event)
	{
		if (!m_change.is_none())
		{
			handleEvent(m_change, event);
		}
	}

	wxCheckBox& ctrl()
	{
		return *(wxCheckBox*)m_elem;
	}

	friend void init_layout(py::module &m);

protected:
	pyobj m_change;
};


class Text : public Control
{
public:
	template <class... Args>
	Text(wxcstr label, Args ...args) : Control(args...)
	{
		bindElem(new wxStaticText(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize(), getAlignStyle()));
	}

	long getAlignStyle();

	wxStaticText& ctrl()
	{
		return *(wxStaticText*)m_elem;
	}
};


class TextInput : public Control
{
public:
	template <class... Args>
	TextInput(wxcstr value, wxcstr type, bool readonly, bool multiline, long exstyle, Args ...args) : Control(args...)
	{
		long style = 0L;
		if (readonly)
		{
			style |= wxTE_READONLY;
		}
		if (multiline)
		{
			style |= wxTE_MULTILINE;
		}
		if (type == wxT("password"))
		{
			style |= wxTE_PASSWORD;
		}
		else if (type == wxT("number"))
		{

		}
		if (exstyle)
		{
			style |= exstyle;
		}
		style |= ((Text*)this)->getAlignStyle();
		bindElem(new wxTextCtrl(*getActiveLayout(), wxID_ANY, value, wxDefaultPosition, getStyleSize(), style));
	}

	void setValue(wxcstr value)
	{
		ctrl().SetValue(value);
	}

	wxString getValue()
	{
		return ctrl().GetValue();
	}

	void setOnEnter(pycref fn)
	{
		bindEvt(wxEVT_TEXT_ENTER, fn);
	}

protected:

	wxTextCtrl& ctrl()
	{
		return *(wxTextCtrl*)m_elem;
	}
};


class SearchCtrl: public Control
{
public:
	template <class... Args>
	SearchCtrl(wxcstr value, bool search_button, bool cancel_button, long exstyle, Args ...args) : Control(args...)
	{
		bindElem(new wxSearchCtrl(*getActiveLayout(), wxID_ANY, value, wxDefaultPosition, getStyleSize(), exstyle));
		
		if (!search_button)
		{
			ctrl().ShowSearchButton(false);
		}
		if (cancel_button)
		{
			ctrl().ShowCancelButton(true);
		}
	}

	void setValue(wxcstr value)
	{
		ctrl().SetValue(value);
	}

	wxString getValue()
	{
		return ctrl().GetValue();
	}

	void setOnsubmit(pycref fn)
	{
		bindEvt(wxEVT_SEARCHCTRL_SEARCH_BTN, fn);
	}

	void setOncancel(pycref fn)
	{
		bindEvt(wxEVT_SEARCHCTRL_CANCEL_BTN, fn);
	}

	wxSearchCtrl& ctrl()
	{
		return *(wxSearchCtrl*)m_elem;
	}
};


class SpinCtrl: public Control
{
public:
	template <class... Args>
	SpinCtrl(wxcstr value, int min, int max, int initial, Args ...args) : Control(args...)
	{
		bindElem(new wxSpinCtrl(*getActiveLayout(), wxID_ANY, value, wxDefaultPosition, getStyleSize(), 
			wxSP_ARROW_KEYS | wxALIGN_RIGHT, min, max, initial));
	}

	void setValue(int value)
	{
		ctrl().SetValue(value);
	}

	int getValue() const
	{
		return ctrl().GetValue();
	}

	void setMin(int min)
	{
		ctrl().SetMin(min);
	}

	int getMin() const
	{
		return ctrl().GetMin();
	}

	void setMax(int max)
	{
		ctrl().SetMax(max);
	}

	int getMax()
	{
		return ctrl().GetMax();
	}
	wxSpinCtrl& ctrl() const
	{
		return *(wxSpinCtrl*)m_elem;
	}
};


class BaseControlWithItems : public Control
{
public:
	BaseControlWithItems(pycref onselect, pycref key, pycref className, pycref style) :
		Control(key, className, style), m_onselect(onselect)
	{

	}

	void onSelect(wxCommandEvent & event)
	{
		if (!m_onselect.is_none())
		{
			handleEvent(m_onselect, event);
		}
	}

	virtual int getSelection()
	{
		return ctrl().GetSelection();
	}

	virtual void doSetSelection(int n)
	{
		ctrl().SetSelection(n);
	}

	virtual void triggerSelectEvent()
	{

	}

	/**
	* handle 是否触发事件处理
	*/
	auto setSelection(int n, bool handle = false)
	{
		doSetSelection(n);
		if (handle)
		{
			triggerSelectEvent();
		}
		return this;
	}

	virtual int getCount()
	{
		return ctrl().GetCount();
	}

	virtual wxString doGetText(int pos)
	{
		return ctrl().GetString(pos);
	}

	virtual void doSetText(int pos, wxcstr text)
	{
		ctrl().SetString(pos, text);
	}

	wxString getText(int pos=-1)
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

	void setText(wxcstr text, int pos=-1)
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

	auto getText1()
	{
		return getText();
	}

	void setText1(wxcstr text)
	{
		setText(text);
	}

	pyobj getTexts()
	{
		const wxArrayString &textArray = ctrl().GetStrings();
		py::list list;
		for (wxcstr text : textArray)
		{
			list.append(text);
		}
		return list;
	}

	wxString __getitem__(int i)
	{
		return getText(i);
	}

	void __setitem__(int i, wxcstr text)
	{
		return setText(text, i);
	}

	wxControlWithItems& ctrl()
	{
		return *(wxControlWithItems*)m_elem;
	}

	friend void init_layout(py::module &m);

protected:
	pyobj m_onselect;
};


class ControlWithItems : public BaseControlWithItems
{
public:
	using BaseControlWithItems::BaseControlWithItems;

	void insert(pycref text, int pos)
	{
		ctrl().Insert(py::cast<wxString>(text), pos);
	}

	void append(pycref text)
	{
		insert(text, getCount());
	}

	void insertItems(pycref choices, int pos)
	{
		ctrl().Insert(py::cast<wxArrayString>(choices), pos);
	}

	void appendItems(pycref choices)
	{
		insertItems(choices, getCount());
	}

	void pop(int pos)
	{
		ctrl().Delete(pos);
	}

	void setItems(pycref choices) {
		clear();
		insertItems(choices, 0);
	}

	void clear()
	{
		ctrl().Clear();
	}
};


class ListBox : public ControlWithItems
{
public:
	using ControlWithItems::ControlWithItems;

	template <class... Args>
	ListBox(pycref choices, pycref onselect, Args ...args) :
		ControlWithItems(onselect, args...)
	{
		bindElem(new wxListBox(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), py::cast<wxArrayString>(choices)));
		m_elem->Bind(wxEVT_LISTBOX, &ListBox::onSelect, this);
	}

	void triggerSelectEvent() override
	{
		addPendingEvent(wxEVT_LISTBOX);
	}
	wxListBox& ctrl()
	{
		return *(wxListBox*)m_elem;
	}
};


class CheckListBox : public ListBox
{
public:
	using ListBox::ListBox;
	template <class... Args>
	CheckListBox(pycref choices, pycref onselect, Args ...args) :
		ListBox(onselect, args...)
	{
		bindElem(new wxCheckListBox(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), py::cast<wxArrayString>(choices)));
		m_elem->Bind(wxEVT_LISTBOX, &ListBox::onSelect, this);
	}

	pyobj getCheckedItems()
	{
		wxArrayInt items;
		ctrl().GetCheckedItems(items);
		return asPyList(items);
	}

	void setCheckedItems(pyobj list)
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

	void checkAll(bool checked=true)
	{
		auto &el = ctrl();
		for (uint i = 0; i < el.GetCount(); ++i)
		{
			el.Check(i, checked);
		}
	}

	void reverseCheck()
	{
		auto &el = ctrl();
		for (uint i = 0; i < el.GetCount(); ++i)
		{
			el.Check(i, !el.IsChecked(i));
		}
	}

	wxCheckListBox& ctrl()
	{
		return *(wxCheckListBox*)m_elem;
	}
};


class RearrangeList : public CheckListBox
{
public:
	template <class... Args>
	RearrangeList(pycref choices, pycref order, pycref onselect, Args ...args) :
		CheckListBox(onselect, args...)
	{
		bindElem(new wxRearrangeListPatched(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(),
			py::cast<wxArrayInt>(order), py::cast<wxArrayString>(choices)));
		m_elem->Bind(wxEVT_LISTBOX, &ListBox::onSelect, this);
	}

	void moveUp()
	{
		ctrl().MoveCurrentUp();
	}

	void moveDown()
	{
		ctrl().MoveCurrentDown();
	}
	wxRearrangeList& ctrl()
	{
		return *(wxRearrangeList*)m_elem;
	}
};

class Choice : public ControlWithItems
{
public:
	template <class... Args>
	Choice(pycref choices, pycref onselect, Args ...args) :
		ControlWithItems(onselect, args...)
	{
		bindElem(new wxChoice(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), py::cast<wxArrayString>(choices)));
		m_elem->Bind(wxEVT_CHOICE, &Choice::onSelect, this);
	}

	void triggerSelectEvent() override
	{
		addPendingEvent(wxEVT_CHOICE);
	}
};


class ComboBox : public ControlWithItems
{
public:
	template <class... Args>
	ComboBox(wxcstr type, pycref choices, pycref onselect, Args ...args) :
		ControlWithItems(onselect, args...)
	{
		long style = 0L;
		if (type == wxT("simple"))
		{
			style |= wxCB_SIMPLE | wxTE_PROCESS_ENTER;
		}
		else if (type == wxT("dropdown"))
		{
			style |= wxCB_DROPDOWN;
		}
		else if (type == wxT("readonly"))
		{
			style |= wxCB_READONLY;
		}
		bindElem(new wxComboBox(*getActiveLayout(), wxID_ANY, wxNoneString, wxDefaultPosition, getStyleSize(), py::cast<wxArrayString>(choices), style));
		m_elem->Bind(wxEVT_COMBOBOX, &ComboBox::onSelect, this);

		if (!(style & wxCB_READONLY))
		{
			ctrl().AutoComplete(ctrl().GetStrings());
		}
	}

	void triggerSelectEvent() override
	{
		addPendingEvent(wxEVT_COMBOBOX);
	}

	wxString getValue()
	{
		return ctrl().GetValue();
	}

	void setValue(wxcstr value)
	{
		ctrl().SetValue(value);
	}

	void setOnEnter(pycref fn)
	{
		bindEvt(wxEVT_TEXT_ENTER, fn);
	}

/*
	void setOnTextChange(pycref fn)
	{
		bindEvt(wxEVT_TEXT, fn);
	}*/

	wxComboBox& ctrl()
	{
		return *(wxComboBox*)m_elem;
	}
};


class RadioBox : public BaseControlWithItems
{
public:
	template <class... Args>
	RadioBox(wxcstr label, pycref choices, pycref onselect, Args ...args) :
		BaseControlWithItems(onselect, args...)
	{
		bindElem(new wxRadioBox(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize(), py::cast<wxArrayString>(choices)));
		m_elem->Bind(wxEVT_RADIOBOX, &ComboBox::onSelect, this);
	}

	int getCount() override
	{
		return ctrl().GetCount();
	}

	wxString doGetText(int pos) override
	{
		return ctrl().GetString(pos);
	}

	void doSetText(int pos, wxcstr text) override
	{
		ctrl().SetString(pos, text);
	}

	int getSelection() override
	{
		return ctrl().GetSelection();
	}

	void doSetSelection(int n) override
	{
		ctrl().SetSelection(n);
	}

	void triggerSelectEvent() override
	{
		addPendingEvent(wxEVT_RADIOBOX);
	}

	wxRadioBox& ctrl()
	{
		return *(wxRadioBox*)m_elem;
	}

protected:

	void applyStyle() override;
};


class Hr : public Control
{
public:
	template <class... Args>
	Hr(bool vertical, Args ...args) : Control(args...)
	{
		bindElem(new wxStaticLine(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(),
			vertical ? wxLI_VERTICAL: wxLI_HORIZONTAL));
	}
};


class FilePickerCtrl : public Control 
{
public:
	template <class... Args>
	FilePickerCtrl(wxcstr path, wxcstr msg, wxcstr wildcard, long exstyle, Args ...args) : Control(args...)
	{
		bindElem(new wxFilePickerCtrl(*getActiveLayout(), wxID_ANY, path, msg, wildcard, wxDefaultPosition, getStyleSize(), exstyle));
	}

	wxString getPath()
	{
		return ctrl().GetPath();
	}

	void setPath(wxcstr path)
	{
		ctrl().SetPath(path);
	}

	void setOnchange(pycref fn)
	{
		bindEvt(wxEVT_FILEPICKER_CHANGED, fn);
	}

	wxFilePickerCtrl& ctrl()
	{
		return *(wxFilePickerCtrl*)m_elem;
	}
};


class DirPickerCtrl : public Control 
{
public:
	template <class... Args>
	DirPickerCtrl(wxcstr path, wxcstr msg, long exstyle, Args ...args) : Control(args...)
	{
		bindElem(new wxDirPickerCtrl(*getActiveLayout(), wxID_ANY, path, msg, wxDefaultPosition, getStyleSize(), exstyle));
	}

	wxString getPath()
	{
		return ctrl().GetPath();
	}

	void setPath(wxcstr path)
	{
		ctrl().SetPath(path);
	}

	void setOnchange(pycref fn)
	{
		bindEvt(wxEVT_DIRPICKER_CHANGED, fn);
	}

	wxDirPickerCtrl& ctrl()
	{
		return *(wxDirPickerCtrl*)m_elem;
	}
};