#pragma once
#include "layoutbase.hpp"
#include <wx/button.h>
#include <wx/stattext.h>
#include <wx/spinctrl.h>
#include "wxpatch.hpp"


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

	void setLabel(wxcstr label)
	{
		m_ctrl().SetLabel(label);
	}

protected:
	wxButton& m_ctrl()
	{
		return *(wxButton*)m_elem;
	}
};


class CheckBox : public Control
{
public:
	template <class... Args>
	CheckBox(wxcstr label, bool checked, bool alignRight, pyobj &onchange, Args ...args) :
		Control(args...), m_listener(onchange)
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
		m_ctrl().SetValue(checked);
	}

	bool getChecked()
	{
		return m_ctrl().GetValue();
	}

	void setLabel(wxcstr label)
	{
		m_ctrl().SetLabel(label);
	}

	void onChange(wxCommandEvent & event)
	{
		if (!m_listener.is_none())
		{
			handlerEvent(m_listener, event);
		}
	}

	friend void initLayout(py::module &m);
protected:
	pyobj m_listener;

	wxCheckBox& m_ctrl()
	{
		return *(wxCheckBox*)m_elem;
	}
};


class Text : public Control
{
public:
	template <class... Args>
	Text(wxcstr label, Args ...args) : Control(args...)
	{
		bindElem(new wxStaticText(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize()));
	}

	void setText(wxcstr label)
	{
		m_ctrl().SetLabel(label);
	}

protected:
	wxStaticText& m_ctrl()
	{
		return *(wxStaticText*)m_elem;
	}
};


class TextInput : public Control
{
public:
	template <class... Args>
	TextInput(wxcstr value, wxcstr type, bool readonly, bool multiline, int extStyle, Args ...args) : Control(args...)
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
		if (extStyle)
		{
			style |= extStyle;
		}
		bindElem(new wxTextCtrl(*getActiveLayout(), wxID_ANY, value, wxDefaultPosition, getStyleSize(), style));
	}

	void setValue(wxcstr value)
	{
		m_ctrl().SetValue(value);
	}

	wxString getValue()
	{
		return m_ctrl().GetValue();
	}

protected:
	void applyStyle() override
	{
		View::applyStyle();

		pyobj style;

		style = getStyle(STYLE_TEXTALIGN);
		if (style != None)
		{
			wxcstr align = style.cast<wxString>();
			if (align != wxNoneString) {
				int style = m_ctrl().GetWindowStyle();
				if (align == wxT("center"))
				{
					style |= wxTE_CENTER;
				}
				else if (align == wxT("right"))
				{
					style |= wxTE_RIGHT;
				}
				else if (align == wxT("left"))
				{
					style |= wxTE_LEFT;
				}
				m_ctrl().SetWindowStyle(style);
			}
		}
	}

	wxTextCtrl& m_ctrl()
	{
		return *(wxTextCtrl*)m_elem;
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
		m_ctrl().SetValue(value);
	}

	int getValue() const
	{
		return m_ctrl().GetValue();
	}

	void setMin(int min)
	{
		m_ctrl().SetMin(min);
	}

	int getMin() const
	{
		return m_ctrl().GetMin();
	}

	void setMax(int max)
	{
		m_ctrl().SetMax(max);
	}

	int getMax()
	{
		return m_ctrl().GetMax();
	}
protected:
	wxSpinCtrl& m_ctrl() const
	{
		return *(wxSpinCtrl*)m_elem;
	}
};


class BaseControlWithItems : public Control
{
public:
	BaseControlWithItems(pycref listener, pycref key, pycref className, pycref style) :
		Control(key, className, style), m_listener(listener)
	{

	}

	void prepareOptions(wxArrayString &array, pyobj options, pycref values)
	{
		if (!options.is_none())
		{
			if (py::isinstance<py::function>(values))
			{
				py::list tmpOptions, tmpValues;
				for (auto &e : options)
				{
					py::tuple item = values(e);
					tmpOptions.append(item[0]);
					tmpValues.append(item[1]);
				}
				options = tmpOptions;
				m_values = tmpValues;
			}
			else
			{
				m_values = values;
			}
			addAll(array, options);
		}
		else
		{
			m_values = None;
		}
	}

	void onSelect(wxCommandEvent & event)
	{
		if (!m_listener.is_none())
		{
			/*int index = event.GetSelection();
			if (!m_values.is_none())
			{
				(void)pyCall(m_listener, m_values[py::int_(index)], index);
			}
			else {
				(void)pyCall(m_listener, index);
			}*/
			handlerEvent(m_listener, event);
		}
	}

	pyobj getValue(pyobj i)
	{
		if (i == None)
		{
			i = py::cast(getSelection());
		}
		if (m_values.is_none())
		{
			return i;
		}
		return m_values[i];
	}

	void setValue(pyobj value)
	{
		if (m_values.is_none())
		{
			setSelection(value.cast<int>());
		}
		else
		{
			pyobj ret = pyCall(m_values.attr("find"), value);
			if (!ret.is_none())
			{
				setSelection(ret.cast<int>());
			}
		}
	}

	pyobj getTexts()
	{
		const wxArrayString &textArray = m_ctrl().GetStrings();
		py::list list;
		for (wxcstr text: textArray)
		{
			list.append(text);
		}
		return list;
	}

	virtual int getCount()
	{
		return m_ctrl().GetCount();
	}

	virtual wxString doGetText(int pos)
	{
		return m_ctrl().GetString(pos);
	}

	virtual void doSetText(int pos, wxcstr text)
	{
		m_ctrl().SetString(pos, text);
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

	virtual int getSelection()
	{
		return m_ctrl().GetSelection();
	}

	virtual void doSetSelection(int n)
	{
		m_ctrl().SetSelection(n);
	}

	virtual void triggerSelectEvent()
	{

	}

	/**
	 * handle 是否触发事件处理
	 */
	void setSelection(int n, bool handle=false)
	{
		doSetSelection(n);
		if (handle)
		{
			triggerSelectEvent();
		}
	}

	friend void initLayout(py::module &m);

protected:
	pyobj m_listener;
	pyobj m_values;

	wxControlWithItems& m_ctrl()
	{
		return *(wxControlWithItems*)m_elem;
	}
};


class ControlWithItems : public BaseControlWithItems
{
public:
	using BaseControlWithItems::BaseControlWithItems;

	void insert(pycref options, pycref values, int pos)
	{
		wxArrayString choices;
		prepareOptions(choices, options, values);
		m_ctrl().Insert(choices, pos);
	}

	void append(pycref options, pycref values)
	{
		insert(options, values, getCount());
	}

	void remove(int pos)
	{
		m_ctrl().Delete(pos);
	}

	void setItems(pycref options, pycref values) {
		clear();
		insert(options, values, 0);
	}

	void clear()
	{
		m_ctrl().Clear();
	}
};


class ListBox : public ControlWithItems
{
public:
	using ControlWithItems::ControlWithItems;

	template <class... Args>
	ListBox(pycref options, pycref values, pycref listener, Args ...args) :
		ControlWithItems(listener, args...)
	{
		wxArrayString choices;
		prepareOptions(choices, options, values);
		bindElem(new wxListBox(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), choices));
		m_elem->Bind(wxEVT_LISTBOX, &ListBox::onSelect, this);
	}

	void triggerSelectEvent() override
	{
		addPendingEvent(wxEVT_LISTBOX);
	}

protected:
	wxListBox& m_ctrl()
	{
		return *(wxListBox*)m_elem;
	}
};


class CheckListBox : public ListBox
{
public:
	using ListBox::ListBox;
	template <class... Args>
	CheckListBox(pycref options, pycref values, pycref listener, Args ...args) :
		ListBox(listener, args...)
	{
		wxArrayString choices;
		prepareOptions(choices, options, values);
		bindElem(new wxCheckListBox(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), choices));
		m_elem->Bind(wxEVT_LISTBOX, &ListBox::onSelect, this);
	}

	pyobj getCheckedItems()
	{
		wxArrayInt items;
		m_ctrl().GetCheckedItems(items);
		py::list list;
		for (int idx : items)
		{
			list.append(idx);
		}
		return list;
	}

protected:
	wxCheckListBox& m_ctrl()
	{
		return *(wxCheckListBox*)m_elem;
	}
};


class RearrangeList : public CheckListBox
{
public:
	template <class... Args>
	RearrangeList(pycref options, pycref values, pycref listener, Args ...args) :
		CheckListBox(listener, args...)
	{
		wxArrayString choices;
		wxArrayInt order;
		prepareOptions(choices, options, values);
		bindElem(new wxRearrangeListPatched(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), order, choices));
		m_elem->Bind(wxEVT_LISTBOX, &ListBox::onSelect, this);
	}

	void moveUp()
	{
		m_ctrl().MoveCurrentUp();
	}

	void moveDown()
	{
		m_ctrl().MoveCurrentDown();
	}

protected:
	wxRearrangeList& m_ctrl()
	{
		return *(wxRearrangeList*)m_elem;
	}
};


class ComboBox : public ControlWithItems
{
public:
	template <class... Args>
	ComboBox(wxcstr type, pycref options, pycref values, pycref listener, Args ...args) :
		ControlWithItems(listener, args...)
	{
		long style = 0L;
		if (type == wxT("simple"))
		{
			style |= wxCB_SIMPLE;
		}
		else if (type == wxT("dropdown"))
		{
			style |= wxCB_DROPDOWN;
		}
		else if (type == wxT("readonly"))
		{
			style |= wxCB_READONLY;
		}

		wxArrayString choices;
		prepareOptions(choices, options, values);
		bindElem(new wxComboBox(*getActiveLayout(), wxID_ANY, wxNoneString, wxDefaultPosition, getStyleSize(), choices, style));
		m_elem->Bind(wxEVT_COMBOBOX, &ComboBox::onSelect, this);
	}

	void triggerSelectEvent() override
	{
		addPendingEvent(wxEVT_COMBOBOX);
	}

protected:

	wxComboBox& m_ctrl()
	{
		return *(wxComboBox*)m_elem;
	}
};


class RadioBox : public BaseControlWithItems
{
public:
	template <class... Args>
	RadioBox(wxcstr label, pycref options, pycref values, pycref listener, Args ...args) :
		BaseControlWithItems(listener, args...)
	{
		wxArrayString choices;
		prepareOptions(choices, options, values);

		bindElem(new wxRadioBox(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize(), choices));
		m_elem->Bind(wxEVT_RADIOBOX, &ComboBox::onSelect, this);
	}

	int getCount() override
	{
		return m_ctrl().GetCount();
	}

	wxString doGetText(int pos) override
	{
		return m_ctrl().GetString(pos);
	}

	void doSetText(int pos, wxcstr text) override
	{
		m_ctrl().SetString(pos, text);
	}

	int getSelection() override
	{
		return m_ctrl().GetSelection();
	}

	void doSetSelection(int n) override
	{
		m_ctrl().SetSelection(n);
	}

	void triggerSelectEvent() override
	{
		addPendingEvent(wxEVT_RADIOBOX);
	}

protected:

	void applyStyle() override
	{
		View::applyStyle();

		pyobj style;

		style = getStyle(STYLE_FLEXDIRECTION);
		if (style != None)
		{
			wxcstr dir = style.cast<wxString>();
			if (dir != wxNoneString) {
				int style = m_ctrl().GetWindowStyle();
				if (dir == wxT("row"))
				{
					style |= wxRA_SPECIFY_ROWS;
				}
				else if (dir == wxT("column"))
				{
					style |= wxRA_SPECIFY_COLS;
				}
				m_ctrl().SetWindowStyle(style);
			}
		}
	}

	wxRadioBox& m_ctrl()
	{
		return *(wxRadioBox*)m_elem;
	}
};