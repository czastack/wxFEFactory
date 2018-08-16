#pragma once
#include "uibase.h"
#include <wx/button.h>
#include <wx/tglbtn.h>
#include <wx/stattext.h>
#include <wx/spinctrl.h>
#include <wx/srchctrl.h>
#include <wx/statline.h>
#include <wx/filepicker.h>
#include <wx/clrpicker.h>
#include <wx/treectrl.h>
#include "wxpatch.h"


class Button : public Control
{
protected:
	using Control::Control;
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

	void click()
	{
		addPendingEvent(wxEVT_BUTTON);
	}
};


class BitmapButton : public Button
{
public:
	template <class... Args>
	BitmapButton(pycref src, pyobj &onclick, Args ...args) : Button(args...)
	{
		wxBitmap bp;
		bindElem(new wxBitmapButton(*getActiveLayout(), wxID_ANY, castBitmap(src, bp), wxDefaultPosition, getStyleSize()));
		setOnClick(onclick);
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
		bindEvt(wxEVT_TOGGLEBUTTON, fn, reset);
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
		bindEvt(wxEVT_CHECKBOX, fn, reset);
	}
};


class Img : public Control 
{
public:
	template <class... Args>
	Img(pycref src, Args ...args) : Control(args...)
	{
		wxBitmap bp;
		bindElem(new wxStaticBitmap(*getActiveLayout(), wxID_ANY, castBitmap(src, bp), wxDefaultPosition, getStyleSize()));
	}

	wxStaticBitmap& ctrl() const
	{
		return *(wxStaticBitmap*)m_elem;
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

	void setOnEnter(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_TEXT_ENTER, fn, reset);
	}

	void setOnChar(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_CHAR, fn, reset, true);
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

	py::tuple getSelection()
	{
		py::tuple selection(2);
		long start, end;
		ctrl().GetSelection(&start, &end);
		selection[0] = start;
		selection[0] = end;
		return selection;
	}

	void setSelection(py::sequence &selection)
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

	void setOnSubmit(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_SEARCHCTRL_SEARCH_BTN, fn, reset);
	}

	void setOnCancel(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_SEARCHCTRL_CANCEL_BTN, fn, reset);
	}
};


class SpinCtrl: public Control
{
public:
	template <class... Args>
	SpinCtrl(wxcstr value, int min, int max, int initial, long wxstyle, Args ...args) : Control(args...)
	{
		bindElem(new wxSpinCtrl(*getActiveLayout(), wxID_ANY, value, wxDefaultPosition, getStyleSize(), 
			wxstyle ? wxstyle: (wxSP_ARROW_KEYS | wxALIGN_RIGHT), min, max, initial));
	}

	wxSpinCtrl& ctrl() const
	{
		return *(wxSpinCtrl*)m_elem;
	}

	void setOnChange(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_SPINCTRL, fn, reset);
	}

	void setOnEnter(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_TEXT_ENTER, fn, reset);
	}
};


class ColorPicker : public Control
{
public:
	template <class... Args>
	ColorPicker(uint color, pyobj &onchange, Args ...args) :
		Control(args...)
	{

		bindElem(new wxColourPickerCtrl(*getActiveLayout(), wxID_ANY, wxColor(color), wxDefaultPosition, getStyleSize()));
		setOnChange(onchange);
	}

	wxColourPickerCtrl& ctrl() const
	{
		return *(wxColourPickerCtrl*)m_elem;
	}

	void setOnChange(pyobj &fn, bool reset = true)
	{
		bindEvt(wxEVT_COLOURPICKER_CHANGED, fn, reset);
	}

	void setColor(uint rgb)
	{
		ctrl().SetColour(wxColor(rgb));
	}

	uint getColor()
	{
		return ctrl().GetColour().GetRGB();
	}
};


class ItemContainer : public Control
{
public:
	using Control::Control;

	virtual wxItemContainerImmutable& ctnr() const = 0;

	int getSelection()
	{
		return ctnr().GetSelection();
	}

	void doSetSelection(int n)
	{
		ctnr().SetSelection(n);
	}

	virtual void triggerSelectEvent()
	{

	}

	/**
	* handle 是否触发事件处理
	*/
	auto setSelection(int n, bool handle = false);

	int getCount()
	{
		return ctnr().GetCount();
	}

	wxString doGetText(int pos)
	{
		return ctnr().GetString(pos);
	}

	void doSetText(int pos, wxcstr text)
	{
		ctnr().SetString(pos, text);
	}

	wxString getText(int pos = -1);

	void setText(wxcstr text, int pos = -1);

	auto getText1()
	{
		return getText();
	}

	void setText1(wxcstr text)
	{
		setText(text);
	}

	pyobj getTexts();

	wxString __getitem__(int i)
	{
		return getText(i);
	}

	void __setitem__(int i, wxcstr text)
	{
		return setText(text, i);
	}

	void prev(bool handle = true);

	void next(bool handle = true);
};


class ControlWithItems : public ItemContainer
{
public:
	using ItemContainer::ItemContainer;

	wxItemContainerImmutable& ctnr() const override
	{
		return *(wxItemContainerImmutable*)(wxControlWithItems*)m_elem;
	}

	wxControlWithItems& ctrl() const
	{
		return *(wxControlWithItems*)m_elem;
	}

	void insert(wxcstr text, int pos)
	{
		ctrl().Insert(text, pos);
	}

	void append(wxcstr text)
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
		ControlWithItems(args...)
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
		ListBox(args...)
	{
		bindElem(new wxCheckListBox(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), py::cast<wxArrayString>(choices)));
		bindEvt(wxEVT_LISTBOX, onselect);
	}

	wxCheckListBox& ctrl() const
	{
		return *(wxCheckListBox*)m_elem;
	}

	pyobj getCheckedItems();

	void setCheckedItems(pyobj list);

	void checkAll(bool checked = true);

	void reverseCheck();
};


class RearrangeList : public CheckListBox
{
public:
	template <class... Args>
	RearrangeList(pycref choices, pycref order, pycref onselect, Args ...args) :
		CheckListBox(args...)
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
		ControlWithItems(args...)
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
		ControlWithItems(args...)
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
		else if (type == wxT("processenter"))
		{
			style |= wxTE_PROCESS_ENTER;
		}
		else if (type == wxT("readonly")) {
			style |= wxCB_READONLY;
		}
		bindElem(new wxComboBox(*getActiveLayout(), wxID_ANY, wxNoneString, wxDefaultPosition, getStyleSize(), py::cast<wxArrayString>(choices), style));
		bindEvt(wxEVT_COMBOBOX, onselect);
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

	void setOnEnter(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_TEXT_ENTER, fn, reset);
	}

	void auto_complete()
	{
		if (!has_wxstyle(wxCB_READONLY))
		{
			ctrl().AutoComplete(ctrl().GetStrings());
		}
	}

/*
	void setOnTextChange(pycref fn)
	{
		bindEvt(wxEVT_TEXT, fn);
	}*/
};


class RadioBox : public ItemContainer
{
public:
	template <class... Args>
	RadioBox(wxcstr label, pycref choices, pycref onselect, Args ...args) :
		ItemContainer(args...)
	{
		bindElem(new wxRadioBox(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize(), py::cast<wxArrayString>(choices)));
		bindEvt(wxEVT_RADIOBOX, onselect);
	}

	wxItemContainerImmutable& ctnr() const override
	{
		return *(wxItemContainerImmutable*)(wxRadioBox*)m_elem;
	}

	wxRadioBox& ctrl() const
	{
		return *(wxRadioBox*)m_elem;
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

	void setOnChange(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_FILEPICKER_CHANGED, fn, reset);
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

	void setOnChange(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_DIRPICKER_CHANGED, fn, reset);
	}
};


class TreeCtrl : public Control
{
public:
	template <class... Args>
	TreeCtrl(long wxstyle, Args ...args) : Control(args...)
	{
		bindElem(new wxTreeCtrl(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(),
			wxstyle ? wxstyle: (wxTR_HAS_BUTTONS | wxTR_SINGLE)));
	}

	wxTreeCtrl& ctrl() const
	{
		return *(wxTreeCtrl*)ptr();
	}

	void setOnItemActivated(pycref fn, bool reset = true)
	{
		bindEvt(wxEVT_TREE_ITEM_ACTIVATED, fn, reset, true);
	}
};


class PyTreeItemData : public wxTreeItemData
{
public:
	PyTreeItemData(pycref obj) : m_data(obj) { }
	pycref GetData() const { return m_data; }
private:
	pyobj m_data;
};

namespace pybind11 {
	namespace detail {
		template <> class type_caster<wxTreeItemId> {
		public:
			bool load(handle src, bool) {
				value.m_pItem = (void*)(size_t)src.cast<pybind11::int_>();
				return true;
			}

			static handle cast(const wxTreeItemId &src, return_value_policy /* policy */, handle /* parent */) {
				return PyLong_FromUnsignedLongLong((size_t)src.GetID());
			}

			PYBIND11_TYPE_CASTER(wxTreeItemId, (_)("wxTreeItemId"));
		protected:
			bool success = false;
		};
	};
};
