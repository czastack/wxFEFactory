#include <wx/wx.h>
#include <wx/propgrid/propgrid.h>
#include <wx/listctrl.h>
#include "ui.h"


void UiModule::init_datacontrols()
{
	using namespace py::literals;

	py::class_<NODELETE(wxPGProperty)>(ui, "PGProperty")
		.def("GetName", &wxPGProperty::GetName)
		.def("GetLabel", &wxPGProperty::GetLabel)
		.def("GetValue", &wxPGProperty::GetValue)
		.def("SetHelpString", &wxPGProperty::SetHelpString)
		.def("SetAttribute", &wxPGProperty::SetAttribute, name, value)
		.def("SetFlagRecursively", &wxPGProperty::SetFlagRecursively, "flag"_a, "set"_a);

	py::class_<NODELETE(wxPropertyCategory), wxPGProperty>(ui, "PropertyCategory")
		.def(py::init<const wxString&, const wxString&>(), label, name = wxPG_LABEL);

	py::class_<NODELETE(wxStringProperty), wxPGProperty>(ui, "StringProperty")
		.def(py::init<const wxString&, const wxString&, const wxString&>(),
			label = wxPG_LABEL, name = wxPG_LABEL, value = wxEmptyString);

	py::class_<NODELETE(wxIntProperty), wxPGProperty>(ui, "IntProperty")
		.def(py::init<const wxString&, const wxString&, long>(),
			label = wxPG_LABEL, name = wxPG_LABEL, value = 0L);

	py::class_<NODELETE(wxUIntProperty), wxPGProperty>(ui, "UIntProperty")
		.def(py::init<const wxString&, const wxString&, unsigned long>(),
			label = wxPG_LABEL, name = wxPG_LABEL, value = 0L);

	py::class_<NODELETE(wxFloatProperty), wxPGProperty>(ui, "FloatProperty")
		.def(py::init<const wxString&, const wxString&, double>(),
			label = wxPG_LABEL, name = wxPG_LABEL, value = 0.0);

	py::class_<NODELETE(wxBoolProperty), wxPGProperty>(ui, "BoolProperty")
		.def(py::init<const wxString&, const wxString&, bool>(),
			label = wxPG_LABEL, name = wxPG_LABEL, value = false);

	py::class_<NODELETE(wxEnumProperty), wxPGProperty>(ui, "EnumProperty")
		.def(py::init<const wxString&, const wxString&, const wxArrayString&, const wxArrayInt&, int>(),
			label, name, "labels"_a, "values"_a = wxArrayInt(), value = 0);

	py::class_<NODELETE(wxFlagsProperty), wxPGProperty>(ui, "FlagsProperty")
		.def(py::init<const wxString&, const wxString&, const wxArrayString&, const wxArrayInt&, int>(),
			label=wxPG_LABEL, name=wxPG_LABEL, "labels"_a, "values"_a, value = 0);

	py::class_<NODELETE(wxLongStringProperty), wxPGProperty>(ui, "LongStringProperty")
		.def(py::init<const wxString&, const wxString&, const wxString&>(),
			label = wxPG_LABEL, name = wxPG_LABEL, value = wxEmptyString);

	py::class_<NODELETE(wxArrayStringProperty), wxPGProperty>(ui, "ArrayStringProperty")
		.def(py::init<const wxString&, const wxString&, const wxArrayString&>(),
			label = wxPG_LABEL, name = wxPG_LABEL, value);


	py::class_<wxPGPropertyFlags>(ui, "PGPropertyFlags");

	py::class_<wxVariant>(ui, "Variant")
		.def(py::init<long, const wxString&>(), value, name_v)
		.def(py::init<bool, const wxString&>(), value, name_v)
		.def(py::init<double, const wxString&>(), value, name_v)
		.def(py::init<const wxString&, const wxString&>(), value, name_v)
		.def(py::init<const wxArrayString&, const wxString&>(), value, name_v)
		.def("GetType", &wxVariant::GetType)
		.def("GetLong", &wxVariant::GetLong)
		.def("GetBool", &wxVariant::GetBool)
		.def("GetDouble", &wxVariant::GetDouble)
		.def("GetString", &wxVariant::GetString)
		.def("GetArrayString", &wxVariant::GetArrayString);


	py::class_<wxPropertyGridIterator>(ui, "PropertyGridIterator")
		.def("Get", &wxPropertyGridIterator::operator*)
		.def("AtEnd", &wxPropertyGridIterator::AtEnd);


	py::class_<NODELETE(wxPropertyGrid), wxControl>(ui, "PropertyGrid")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, pos_v, size_v, style = (long)wxTB_DEFAULT_STYLE, name = (const char*)wxToolBarNameStr)
		.def("GetSelection", &wxPropertyGrid::GetSelection)
		.def("GetIterator", py::overload_cast<int, wxPGProperty*>(&wxPropertyGrid::GetIterator),
			"flags"_a=(int)wxPG_ITERATE_DEFAULT, "first"_a=(wxPGProperty*)nullptr, py::return_value_policy::reference)
		.def("SetPropVal", &wxPropertyGrid::SetPropVal)
		.def("SetExtraStyle", &wxPropertyGrid::SetExtraStyle, "exStyle"_a)
		.def("SetCaptionBackgroundColour", &wxPropertyGrid::SetCaptionBackgroundColour, "col"_a)
		.def("SetMarginColour", &wxPropertyGrid::SetMarginColour, "col"_a)
		.def("Append", &wxPropertyGrid::Append)
		.def("GetPropertyByName", (wxPGProperty * (wxPropertyGrid::*)(const wxString & name) const) & wxPropertyGrid::GetPropertyByName);

	py::enum_<wxListColumnFormat>(ui, "ListColumnFormat")
		.ENUM_VAL(LIST_FORMAT_LEFT)
		.ENUM_VAL(LIST_FORMAT_RIGHT)
		.ENUM_VAL(LIST_FORMAT_CENTRE)
		.export_values();

	// ListView
	py::class_<NODELETE(wxListView), wxControl>(ui, "ListView")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),
			parent, id, pos_v, size_v, style = wxLC_REPORT, validator_v, name = (const char*)wxListCtrlNameStr)
		.def("AppendColumn", &wxListView::AppendColumn,
			"heading"_a, "format"_a=wxLIST_FORMAT_LEFT, "width"_a = -1)
		.def("GetItemCount", &wxListView::GetItemCount)
		.def("InsertItem", (long (wxListView::*)(const wxListItem & info)) & wxListView::InsertItem, "info"_a)
		.def("InsertItem", (long (wxListView::*)(long index, const wxString & label_v, int imageIndex)) & wxListView::InsertItem,
			"index"_a, label, "imageId"_a = -1)
		.def("SetItem", (bool (wxListView::*)(wxListItem & info)) & wxListView::SetItem)
		.def("SetItem", (bool (wxListView::*)(long, int, const wxString&, int)) & wxListView::SetItem,
			"index"_a, "col"_a, label, "imageId"_a = -1)
		.def("GetFirstSelected", &wxListView::GetFirstSelected)
		.def("GetNextSelected", &wxListView::GetNextSelected)
		.def("GetItemCount", &wxListView::GetItemCount)
		.def("GetColumnCount", &wxListView::GetColumnCount)
		.def("EnableCheckBoxes", &wxListView::EnableCheckBoxes, "enable"_a=true)
		.def("IsItemChecked", &wxListView::IsItemChecked, item)
		.def("IsSelected", &wxListView::IsSelected, item)
		.def("CheckItem", &wxListView::CheckItem, item, "check"_a)
		.def("Select", &wxListView::Select, item, "select"_a)
		.def("GetFocusedItem", &wxListView::GetFocusedItem)
		.def("Focus", &wxListView::Focus, "index"_a)
		;

	py::class_<wxListItem>(ui, "ListItem")
		.def(py::init<>())
		.def_readwrite("m_mask", &wxListItem::m_mask)
		.def_readwrite("m_itemId", &wxListItem::m_itemId)
		.def_readwrite("m_col", &wxListItem::m_col)
		.def_readwrite("m_text", &wxListItem::m_text)
		.def_readwrite("m_itemId", &wxListItem::m_itemId);
}