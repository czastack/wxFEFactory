#include <wx/wx.h>
#include <wx/button.h>
#include <wx/tglbtn.h>
#include <wx/stattext.h>
#include <wx/spinctrl.h>
#include <wx/srchctrl.h>
#include <wx/statline.h>
#include <wx/radiobox.h>
#include <wx/rearrangectrl.h>
#include <wx/filepicker.h>
#include <wx/clrpicker.h>
#include <wx/treectrl.h>
#include <unordered_map>
#include "ui.h"


class PyTreeItemData : public wxTreeItemData
{
public:
	PyTreeItemData(pycref obj) : m_data(obj) {}
	pyobj m_data;
};


void UiModule::init_controls()
{
	using namespace py::literals;

	py::class_<NODELETE(wxControl), wxWindow>(ui, "Control");

	py::class_<NODELETE(wxButton), wxControl>(ui, "Button")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, label_v, pos_v, size_v, style_0, validator_v, name = (const char*)wxButtonNameStr);

	py::class_<NODELETE(wxBitmapButton), wxButton>(ui, "BitmapButton")
		.def(py::init<wxWindow*, wxWindowID, const wxBitmap&, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, label_v, pos_v, size_v, style_0, validator_v, name = (const char*)wxButtonNameStr);

	py::class_<NODELETE(wxToggleButton), wxControl>(ui, "ToggleButton")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, label_v, pos_v, size_v, style_0, validator_v, name = (const char*)wxCheckBoxNameStr)
		.def("GetValue", &wxToggleButton::GetValue)
		.def("SetValue", &wxToggleButton::SetValue, value);

	py::class_<NODELETE(wxCheckBox), wxControl>(ui, "CheckBox")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, label_v, pos_v, size_v, style_0, validator_v, name = (const char*)wxCheckBoxNameStr)
		.def("GetValue", &wxCheckBox::GetValue)
		.def("SetValue", &wxCheckBox::SetValue, value);

	py::class_<NODELETE(wxStaticBitmap), wxControl>(ui, "StaticBitmap")
		.def(py::init<wxWindow*, wxWindowID, const wxGDIImage&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, label_v, pos_v, size_v, style_0, name = (const char*)wxStaticBitmapNameStr);

	py::class_<NODELETE(wxStaticText), wxControl>(ui, "StaticText")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, label_v, pos_v, size_v, style_0, name = (const char*)wxStaticTextNameStr);

	py::class_<NODELETE(wxStaticLine), wxControl>(ui, "StaticLine")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, pos_v, size_v, style_0, name = (const char*)wxStaticLineNameStr);

	// py::class_<wxTextEntry>(ui, "TextEntry");

	py::class_<NODELETE(wxTextCtrl), wxControl>(ui, "TextCtrl")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, value = wxEmptyString, pos_v, size_v, style_0, validator_v, name = (const char*)wxTextCtrlNameStr)
		.def("GetValue", &wxTextCtrl::GetValue)
		.def("SetValue", &wxTextCtrl::SetValue, value)
		.def("AppendText", &wxTextCtrl::AppendText, text)
		.def("WriteText", &wxTextCtrl::WriteText, text)
		.def("Clear", &wxTextCtrl::Clear)
		.def("SelectAll", &wxTextCtrl::SelectAll)
		.def("GetSelection", [](wxTextCtrl* self) {
		long from, to;
		py::tuple result(2);
		self->GetSelection(&from, &to);
		result[0] = from;
		result[1] = to;
		return result;
			})
		.def("SetSelection", &wxTextCtrl::SetSelection)
				;

	py::class_<NODELETE(wxSearchCtrl), wxControl>(ui, "SearchCtrl")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, value = wxEmptyString, pos_v, size_v, style_0, validator_v, name = (const char*)wxSearchCtrlNameStr)
		.def("ShowSearchButton", &wxSearchCtrl::ShowSearchButton, show = true)
		.def("ShowCancelButton", &wxSearchCtrl::ShowCancelButton, show = true)
		.def("GetValue", &wxSearchCtrl::GetValue)
		.def("SetValue", &wxSearchCtrl::SetValue, value)
		;

	py::class_<NODELETE(wxSpinCtrl), wxControl>(ui, "SpinCtrl")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, int, int, int, const wxString&>(),
			parent, id_v, value = wxEmptyString, pos_v, size_v, style = wxSP_ARROW_KEYS, "min"_a = 0, "max"_a = 100, "initial"_a = 0, name = wxT("wxSpinCtrl"))
		;

	py::class_<NODELETE(wxColourPickerCtrl), wxControl>(ui, "ColourPickerCtrl")
		.def(py::init<wxWindow*, wxWindowID, const wxColour&, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, "col"_a = *wxBLACK, pos_v, size_v, style = wxCLRP_DEFAULT_STYLE, validator_v, name = (const char*)wxColourPickerCtrlNameStr)
		.def("GetColour", &wxColourPickerCtrl::GetColour)
		.def("SetColour", (void (wxColourPickerCtrl::*)(const wxColour & col)) & wxColourPickerCtrl::SetColour, "col"_a)
		;

	py::class_<NODELETE(wxItemContainerImmutable)>(ui, "ItemContainerImmutable")
		.def("GetSelection", &wxItemContainerImmutable::GetSelection)
		.def("SetSelection", &wxItemContainerImmutable::SetSelection, "n"_a)
		.def("GetCount", &wxItemContainerImmutable::GetCount)
		.def("GetString", &wxItemContainerImmutable::GetString, "n"_a)
		.def("SetString", &wxItemContainerImmutable::SetString, "n"_a, "s"_a)
		;

	py::class_<NODELETE(wxItemContainer), wxItemContainerImmutable>(ui, "ItemContainer")
		.def("Append", (int (wxItemContainer::*)(const wxString & item)) & wxItemContainer::Append, item)
		.def("Append", (int (wxItemContainer::*)(const wxArrayString & item)) & wxItemContainer::Append, items)
		.def("Insert", (int (wxItemContainer::*)(const wxString & item, unsigned int pos)) & wxItemContainer::Insert, item, pos)
		.def("Insert", (int (wxItemContainer::*)(const wxArrayString & items, unsigned int pos)) & wxItemContainer::Insert, item, pos)
		.def("Set", (void (wxItemContainer::*)(const wxArrayString & items)) & wxItemContainer::Set, item)
		.def("Clear", &wxItemContainer::Clear)
		.def("Delete", &wxItemContainer::Delete)
		;

	py::class_<NODELETE(wxControlWithItems), wxControl, wxItemContainer>(ui, "ControlWithItems")
		;

	py::class_<wxListBox, wxControlWithItems>(ui, "ListBox")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, const wxArrayString&, long, const wxValidator&, const wxString&>(),
			parent, id, pos_v, size_v, choices, style_0, validator_v, name = (const char*)wxListBoxNameStr)
		;

	py::class_<NODELETE(wxCheckListBox), wxListBox>(ui, "CheckListBox")
		.def("IsChecked", &wxCheckListBox::IsChecked, item)
		.def("Check", &wxCheckListBox::Check, item, "check"_a = true)
		.def("GetCheckedItems", &wxCheckListBox::GetCheckedItems)
		;

	py::class_<NODELETE(wxRearrangeList), wxCheckListBox>(ui, "RearrangeList")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, const wxArrayInt&, const wxArrayString&, long, const wxValidator&, const wxString&>(),
			parent, id, pos_v, size_v, "order"_a, items, style_0, validator_v, name = (const char*)wxRearrangeListNameStr)
		;

	py::class_<NODELETE(wxChoice), wxControlWithItems>(ui, "Choice")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, const wxArrayString&, long, const wxValidator&, const wxString&>(),
			parent, id, pos_v, size_v, choices, style_0, validator_v, name = (const char*)wxChoiceNameStr)
		;

	py::class_<NODELETE(wxComboBox), wxControlWithItems>(ui, "ComboBox")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, const wxArrayString&, long, const wxValidator&, const wxString&>(),
			parent, id, value, pos_v, size_v, choices=py::tuple(), style_0, validator_v, name = (const char*)wxComboBoxNameStr)
		.def("GetValue", &wxComboBox::GetValue)
		.def("SetValue", &wxComboBox::SetValue, value)
		.def("AutoComplete", (bool (wxComboBox::*)(const wxArrayString & choices)) & wxComboBox::AutoComplete, choices)
		;

	py::class_<NODELETE(wxRadioBox), wxControl, wxItemContainerImmutable>(ui, "RadioBox")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, const wxArrayString&, int, long, const wxValidator&, const wxString&>(),
			parent, id, title, pos_v, size_v, choices, "majorDim"_a = 0, style_0, validator_v, name = (const char*)wxRadioBoxNameStr)
		;

	py::class_<NODELETE(wxFilePickerCtrl), wxControl>(ui, "FilePickerCtrl")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxString&, const wxString&, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, "path"_a = wxEmptyString, "message"_a = (const char*)wxFileSelectorPromptStr, "wildcard"_a = (const char*)wxFileSelectorDefaultWildcardStr,
			pos_v, size_v, style = wxFLP_DEFAULT_STYLE, validator_v, name = (const char*)wxFilePickerCtrlNameStr)
		.def("GetPath", &wxFilePickerCtrl::GetPath)
		.def("SetPath", &wxFilePickerCtrl::SetPath, "path"_a)
		;

	py::class_<NODELETE(wxDirPickerCtrl), wxControl>(ui, "DirPickerCtrl")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxString&, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, "path"_a = wxEmptyString, "message"_a = (const char*)wxFileSelectorPromptStr, pos_v, size_v, style = wxDIRP_DEFAULT_STYLE,
			validator_v, name = (const char*)wxDirPickerCtrlNameStr)
		.def("GetPath", &wxDirPickerCtrl::GetPath)
		.def("SetPath", &wxDirPickerCtrl::SetPath, "path"_a)
		;

	py::class_<wxTreeItemId>(ui, "TreeItemId")
		.def(py::init<>())
		.def("GetID", &wxTreeItemId::GetID)
		;

	py::class_<NODELETE(wxTreeItemData)>(ui, "TreeItemData")
		.def(py::init<>())
		.def("GetId", &wxTreeItemData::GetId, py::return_value_policy::reference)
		.def("SetId", &wxTreeItemData::SetId)
		;

	py::class_<NODELETE(PyTreeItemData), wxTreeItemData>(ui, "PyTreeItemData")
		.def(py::init<pycref>(), data)
		.def_readwrite("data", &PyTreeItemData::m_data)
		;

	py::class_<NODELETE(wxTreeCtrl), wxControl>(ui, "TreeCtrl")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, pos_v, size_v, style = wxTR_DEFAULT_STYLE, validator_v, name = (const char*)wxTreeCtrlNameStr)
		.def("AssignImageList", &wxTreeCtrl::AssignImageList)
		.def("AddRoot", &wxTreeCtrl::AddRoot, text, "image"_a = -1, "selectedImage"_a = -1, data = (wxTreeItemData*)nullptr)
		.def("InsertItem", (wxTreeItemId(wxTreeCtrl::*)(const wxTreeItemId&, size_t, const wxString&, int, int, wxTreeItemData*))
			& wxTreeCtrl::InsertItem, parent, pos=(size_t)-1, text, "image"_a = -1, "selectedImage"_a = -1, data = (wxTreeItemData*)nullptr)
		.def("GetItemData", &wxTreeCtrl::GetItemData, item, py::return_value_policy::reference)
		.def("Delete", &wxTreeCtrl::Delete, item)
		.def("DeleteChildren", &wxTreeCtrl::DeleteChildren, item)
		.def("DeleteAllItems", &wxTreeCtrl::DeleteAllItems)
		.def("Expand", &wxTreeCtrl::Expand, item)
		.def("ExpandAllChildren", &wxTreeCtrl::ExpandAllChildren, item)
		.def("ExpandAll", &wxTreeCtrl::ExpandAll)
		.def("Collapse", &wxTreeCtrl::Collapse, item)
		.def("CollapseAllChildren", &wxTreeCtrl::CollapseAllChildren, item)
		.def("CollapseAll", &wxTreeCtrl::CollapseAll)
		.def("CollapseAndReset", &wxTreeCtrl::CollapseAndReset, item)
		.def("Toggle", &wxTreeCtrl::Toggle, item)
		.def("Unselect", &wxTreeCtrl::Unselect)
		.def("UnselectAll", &wxTreeCtrl::UnselectAll)
		.def("SelectItem", &wxTreeCtrl::SelectItem, item, "select"_a = true)
		.def("SelectChildren", &wxTreeCtrl::SelectChildren, parent)
		.def("ToggleItemSelection", &wxTreeCtrl::ToggleItemSelection, item)
		.def("GetCount", &wxTreeCtrl::GetCount)
		.def("GetIndent", &wxTreeCtrl::GetIndent)
		.def("SetIndent", &wxTreeCtrl::SetIndent)
		.def("GetSpacing", &wxTreeCtrl::GetSpacing)
		.def("SetSpacing", &wxTreeCtrl::SetSpacing)
		;


	py::class_<NODELETE(wxToolBarToolBase)>(ui, "ToolBarToolBase")
		.def("GetId", &wxToolBarToolBase::GetId)
		.def("GetControl", &wxToolBarToolBase::GetControl)
		.def("GetStyle", &wxToolBarToolBase::GetStyle);


	py::class_<NODELETE(wxToolBar), wxControl>(ui, "ToolBar")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, pos_v, size_v, style = (long)wxTB_DEFAULT_STYLE, name = (const char*)wxToolBarNameStr)
		.def("AddTool", (wxToolBarToolBase* (wxToolBar::*)(int, const wxString&, const wxBitmap&, const wxString&, wxItemKind))
			& wxToolBar::AddTool, "toolid"_a, label, "bitmap"_a, "shortHelp"_a = wxEmptyString, "kind"_a = wxITEM_NORMAL, py::return_value_policy::reference)
		.def("AddControl", &wxToolBar::AddControl, "control"_a, label_v, py::return_value_policy::reference)
		.def("InsertControl", &wxToolBar::InsertControl, pos, "control"_a, label_v, py::return_value_policy::reference)
		.def("AddSeparator", &wxToolBar::AddSeparator, py::return_value_policy::reference)
		.def("Realize", &wxToolBar::Realize)
		.def("ClearTools", &wxToolBar::ClearTools)
		.def("FindById", &wxToolBar::FindById)
		.def("GetToolPos", &wxToolBar::GetToolPos)
		.def("SetToolBitmapSize", &wxToolBar::SetToolBitmapSize)
		;

	py::class_<NODELETE(wxStatusBar), wxControl>(ui, "StatusBar")
		.def(py::init<wxWindow*, wxWindowID, long, const wxString&>(),
			parent, id, style = wxSTB_DEFAULT_STYLE, name = (const char*)wxStatusBarNameStr)
		.def("GetStatusText", &wxStatusBar::GetStatusText, "number"_a = 0)
		.def("SetStatusText", &wxStatusBar::SetStatusText, text, "number"_a = 0)
		.def("SetFieldsCount", &wxStatusBar::SetFieldsCount, "number"_a = 1, "widths"_a)
		.def("SetStatusWidths", &wxStatusBar::SetStatusWidths, "number"_a = 1, "widths"_a)
		.def("GetStatusWidth", &wxStatusBar::GetStatusWidth, "n"_a)
		.def("PopStatusText", &wxStatusBar::PopStatusText, "number"_a = 0)
		.def("PushStatusText", &wxStatusBar::PushStatusText, text, "number"_a = 0)
		;
}