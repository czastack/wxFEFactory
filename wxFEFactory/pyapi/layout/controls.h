#pragma once
#include "layoutbase.h"
#include <wx/button.h>
#include <wx/tglbtn.h>
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
		setOnClick(onclick);
	}

	wxButton& ctrl() const
	{
		return *(wxButton*)m_elem;
	}

	void setOnClick(pyobj &fn, bool reset = true)
	{
		bindEvt(wxEVT_BUTTON, fn, reset);
	}
};


class ToggleButton : public Control
{
public:
	template <class... Args>
	ToggleButton(wxcstr label, bool checked, pyobj &onchange, Args ...args) :
		Control(args...)
	{

		bindElem(new wxToggleButton(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize()));
		if (checked)
		{
			setChecked(true);
		}
		setOnChange(onchange);
	}

	wxToggleButton& ctrl() const
	{
		return *(wxToggleButton*)m_elem;
	}

	void trigger()
	{
		setChecked(!getChecked());
		addPendingEvent(wxEVT_TOGGLEBUTTON);
	}

	void setChecked(bool checked)
	{
		ctrl().SetValue(checked);
	}

	bool getChecked()
	{
		return ctrl().GetValue();
	}

	void setOnChange(pyobj &fn, bool reset=true)
	{
		bindEvt(wxEVT_TOGGLEBUTTON, fn);
	}
};


class CheckBox : public Control
{
public:
	template <class... Args>
	CheckBox(wxcstr label, bool checked, bool alignRight, pyobj &onchange, Args ...args) :
		Control(args...)
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
		setOnChange(onchange);
	}

	wxCheckBox& ctrl() const
	{
		return *(wxCheckBox*)m_elem;
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

	void setOnChange(pyobj &fn, bool reset = true)
	{
		bindEvt(wxEVT_CHECKBOX, fn);
	}
};


class Text : public Control
{
public:
	template <class... Args>
	Text(wxcstr label, Args ...args) : Control(args...)
	{
		bindElem(new wxStaticText(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize(), getAlignStyle()));
	}

	wxStaticText& ctrl() const
	{
		return *(wxStaticText*)m_elem;
	}

	long getAlignStyle();
};


class TextInput : public Control
{
public:
	template <class... Args>
	TextInput(wxcstr value, wxcstr type, bool readonly, bool multiline, long wxstyle, Args ...args) : Control(args...)
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
		if (wxstyle)
		{
			style |= wxstyle;
		}
		style |= ((Text*)this)->getAlignStyle();
		bindElem(new wxTextCtrl(*getActiveLayout(), wxID_ANY, value, wxDefaultPosition, getStyleSize(), style));
	}

	wxTextCtrl& ctrl() const
	{
		return *(wxTextCtrl*)m_elem;
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

	void appendText(wxcstr text)
	{
		ctrl().AppendText(text);
	}

	void writeText(wxcstr text)
	{
		ctrl().WriteText(text);
	}

	void clear()
	{
		ctrl().Clear();
	}

	void getSelection()
	{
		py::tuple selection(2);
		long start, end;
		ctrl().GetSelection(&start, &end);
		selection[0] = start;
		selection[0] = end;
	}

	void setSelection(py::tuple &selection)
	{
		ctrl().SetSelection(selection[0].cast<long>(), selection[1].cast<long>());
	}

	void selectAll()
	{
		ctrl().SelectAll();
	}
};


class SearchCtrl: public Control
{
public:
	template <class... Args>
	SearchCtrl(wxcstr value, bool search_button, bool cancel_button, long wxstyle, Args ...args) : Control(args...)
	{
		bindElem(new wxSearchCtrl(*getActiveLayout(), wxID_ANY, value, wxDefaultPosition, getStyleSize(), wxstyle));
		
		if (!search_button)
		{
			ctrl().ShowSearchButton(false);
		}
		if (cancel_button)
		{
			ctrl().ShowCancelButton(true);
		}
	}

	wxSearchCtrl& ctrl() const
	{
		return *(wxSearchCtrl*)m_elem;
	}

	void setValue(wxcstr value)
	{
		ctrl().SetValue(value);
	}

	wxString getValue()
	{
		return ctrl().GetValue();
	}

	void setOnSubmit(pycref fn)
	{
		bindEvt(wxEVT_SEARCHCTRL_SEARCH_BTN, fn);
	}

	void setOnCancel(pycref fn)
	{
		bindEvt(wxEVT_SEARCHCTRL_CANCEL_BTN, fn);
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

	wxSpinCtrl& ctrl() const
	{
		return *(wxSpinCtrl*)m_elem;
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
};


class BaseControlWithItems : public Control
{
public:
	BaseControlWithItems(pycref onselect, pycref className, pycref style) :
		Control(className, style)
	{

	}

	wxControlWithItems& ctrl() const
	{
		return *(wxControlWithItems*)m_elem;
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

	void prev(bool handle = true)
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

	void next(bool handle = true)
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
		bindEvt(wxEVT_LISTBOX, onselect);
	}

	wxListBox& ctrl() const
	{
		return *(wxListBox*)m_elem;
	}

	void triggerSelectEvent() override
	{
		addPendingEvent(wxEVT_LISTBOX);
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
		bindEvt(wxEVT_LISTBOX, onselect);
	}

	wxCheckListBox& ctrl() const
	{
		return *(wxCheckListBox*)m_elem;
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
		bindEvt(wxEVT_LISTBOX, onselect);
	}

	wxRearrangeList& ctrl() const
	{
		return *(wxRearrangeList*)m_elem;
	}

	void moveUp()
	{
		ctrl().MoveCurrentUp();
	}

	void moveDown()
	{
		ctrl().MoveCurrentDown();
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
		bindEvt(wxEVT_CHOICE, onselect);
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
		bindEvt(wxEVT_COMBOBOX, onselect);

		if (!(style & wxCB_READONLY))
		{
			ctrl().AutoComplete(ctrl().GetStrings());
		}
	}

	wxComboBox& ctrl() const
	{
		return *(wxComboBox*)m_elem;
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
};


class RadioBox : public BaseControlWithItems
{
public:
	template <class... Args>
	RadioBox(wxcstr label, pycref choices, pycref onselect, Args ...args) :
		BaseControlWithItems(onselect, args...)
	{
		bindElem(new wxRadioBox(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize(), py::cast<wxArrayString>(choices)));
		bindEvt(wxEVT_RADIOBOX, onselect);
	}

	wxRadioBox& ctrl() const
	{
		return *(wxRadioBox*)m_elem;
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
	FilePickerCtrl(wxcstr path, wxcstr msg, wxcstr wildcard, long wxstyle, Args ...args) : Control(args...)
	{
		bindElem(new wxFilePickerCtrl(*getActiveLayout(), wxID_ANY, path, msg, wildcard, wxDefaultPosition, getStyleSize(), wxstyle));
	}

	wxFilePickerCtrl& ctrl() const
	{
		return *(wxFilePickerCtrl*)m_elem;
	}

	wxString getPath()
	{
		return ctrl().GetPath();
	}

	void setPath(wxcstr path)
	{
		ctrl().SetPath(path);
	}

	void setOnChange(pycref fn)
	{
		bindEvt(wxEVT_FILEPICKER_CHANGED, fn);
	}
};


class DirPickerCtrl : public Control 
{
public:
	template <class... Args>
	DirPickerCtrl(wxcstr path, wxcstr msg, long wxstyle, Args ...args) : Control(args...)
	{
		bindElem(new wxDirPickerCtrl(*getActiveLayout(), wxID_ANY, path, msg, wxDefaultPosition, getStyleSize(), wxstyle));
	}

	wxDirPickerCtrl& ctrl() const
	{
		return *(wxDirPickerCtrl*)m_elem;
	}

	wxString getPath()
	{
		return ctrl().GetPath();
	}

	void setPath(wxcstr path)
	{
		ctrl().SetPath(path);
	}

	void setOnChange(pycref fn)
	{
		bindEvt(wxEVT_DIRPICKER_CHANGED, fn);
	}
};