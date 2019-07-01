#include <wx/wx.h>
#include <wx/aui/aui.h>
#include <wx/aui/tabmdi.h>
#include "ui.h"


void UiModule::init_aui()
{
	using namespace py::literals;
	py::class_<wxAuiManager>(ui, "AuiManager")
		.def(py::init<wxWindow*, unsigned int>(),
			"managedWnd"_a = NULL, "flags"_a = (long)wxAUI_MGR_DEFAULT)
		.def("UnInit", &wxAuiManager::UnInit)
		.def("Update", &wxAuiManager::Update)
		.def("AddPane", (bool (wxAuiManager::*)(wxWindow*, const wxAuiPaneInfo&)) & wxAuiManager::AddPane, window, "paneInfo"_a)
		.def("AddPane", (bool (wxAuiManager::*)(wxWindow*, int, const wxString&))
			& wxAuiManager::AddPane, window, "direction"_a = wxLEFT, "caption"_a = wxEmptyString)
		.def("GetPane", (wxAuiPaneInfo & (wxAuiManager::*)(wxWindow*)) & wxAuiManager::GetPane, window)
		.def("GetPane", (wxAuiPaneInfo & (wxAuiManager::*)(const wxString&)) & wxAuiManager::GetPane, name)
		;

	py::class_<wxAuiPaneInfo>(ui, "AuiPaneInfo")
		.def(py::init<>())
		.def("Name", &wxAuiPaneInfo::Name)
		.def("Top", &wxAuiPaneInfo::Top)
		.def("Right", &wxAuiPaneInfo::Right)
		.def("Bottom", &wxAuiPaneInfo::Bottom)
		.def("Left", &wxAuiPaneInfo::Left)
		.def("Center", &wxAuiPaneInfo::Center)
		.def("Caption", &wxAuiPaneInfo::Caption)
		.def("CloseButton", &wxAuiPaneInfo::CloseButton)
		.def("MaximizeButton", &wxAuiPaneInfo::MaximizeButton)
		.def("MinimizeButton", &wxAuiPaneInfo::MinimizeButton)
		.def("CaptionVisible", &wxAuiPaneInfo::CaptionVisible)
		.def("Row", &wxAuiPaneInfo::Row)
		.def("Hide", &wxAuiPaneInfo::Hide)
		.def_readwrite("dock_direction", &wxAuiPaneInfo::dock_direction)
		/* .def_readwrite("name", &wxAuiPaneInfo::name)
		.def_readwrite("caption", &wxAuiPaneInfo::caption)
		.def_readwrite("icon", &wxAuiPaneInfo::icon)
		.def_readwrite("state", &wxAuiPaneInfo::state)
		.def_readwrite("dock_direction", &wxAuiPaneInfo::dock_direction)
		.def_readwrite("dock_layer", &wxAuiPaneInfo::dock_layer)
		.def_readwrite("dock_row", &wxAuiPaneInfo::dock_row)
		.def_readwrite("dock_pos", &wxAuiPaneInfo::dock_pos)
		.def_readwrite("dock_proportion", &wxAuiPaneInfo::dock_proportion) */
		;

	py::class_<wxAuiMDIParentFrame, wxFrame>(ui, "AuiMDIParentFrame")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, title, pos_v, size_v, style = wxDEFAULT_FRAME_STYLE | wxVSCROLL | wxHSCROLL, name = (const char*)wxFrameNameStr)
		.def("GetNotebook", &wxAuiMDIParentFrame::GetNotebook)
		;

	py::class_<wxAuiMDIChildFrame, wxFrame>(ui, "AuiMDIChildFrame")
		.def(py::init<wxAuiMDIParentFrame*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, title, pos_v, size_v, style = wxDEFAULT_FRAME_STYLE, name = (const char*)wxFrameNameStr)
		;


	py::class_<wxAuiNotebook, wxControl>(ui, "AuiNotebook")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long>(),
			parent, id, pos_v, size_v, style = (long)wxAUI_NB_DEFAULT_STYLE)
		.def("GetSelection", &wxAuiNotebook::GetSelection)
		.def("SetSelection", &wxAuiNotebook::SetSelection)
		.def("GetPageCount", &wxAuiNotebook::GetPageCount)
		.def("GetPage", &wxAuiNotebook::GetPage)
		.def("DeletePage", &wxAuiNotebook::DeletePage)
		.def("AddPage", (bool (wxAuiNotebook::*)(wxWindow*, const wxString&, bool, const wxBitmap&)) & wxAuiNotebook::AddPage,
			"page"_a, "caption"_a, "select"_a = false, "bitmap"_a = wxNullBitmap)
		;


	py::class_<wxAuiToolBarItem>(ui, "AuiToolBarItem")
		.def("GetId", &wxAuiToolBarItem::GetId)
		.def("SetId", &wxAuiToolBarItem::SetId);


	py::class_<wxAuiToolBar, wxControl>(ui, "AuiToolBar")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long>(),
			parent, id, pos_v, size_v, style = (long)wxAUI_TB_DEFAULT_STYLE)
		.def("AddTool", (wxAuiToolBarItem * (wxAuiToolBar::*)(int, const wxString&, const wxBitmap&, const wxString&, wxItemKind))
			& wxAuiToolBar::AddTool, "toolid"_a, label, "bitmap"_a, "shortHelp"_a = wxEmptyString, "kind"_a = wxITEM_NORMAL, py::return_value_policy::reference)
		.def("AddControl", &wxAuiToolBar::AddControl, "control"_a, label_v)
		.def("AddSeparator", &wxAuiToolBar::AddSeparator)
		.def("Realize", &wxAuiToolBar::Realize)
		.def("ClearTools", &wxAuiToolBar::ClearTools)
		.def("GetToolPos", &wxAuiToolBar::GetToolPos)
		.def("SetToolBitmapSize", &wxAuiToolBar::SetToolBitmapSize)
		;
}