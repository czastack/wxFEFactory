#include <wx/wx.h>
#include <wx/mdi.h>
#include "ui.h"


void UiModule::init_frames()
{
	using namespace py::literals;
	py::class_<NODELETE(wxTopLevelWindow), wxWindow>(ui, "TopLevelWindow")
		.def("GetTitle", &wxTopLevelWindow::GetTitle)
		.def("SetTitle", &wxTopLevelWindow::SetTitle, title)
		.def("SetIcon", &wxTopLevelWindow::SetIcon, "icon"_a)
		.def("Destroy", &wxFrame::Destroy)
		;

	py::class_<NODELETE(wxFrame), wxTopLevelWindow>(ui, "Frame")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, title, pos_v, size_v, style = wxDEFAULT_FRAME_STYLE, name = (const char*)wxFrameNameStr)
		.def("GetMenuBar", &wxFrame::GetMenuBar, py::return_value_policy::reference)
		.def("SetMenuBar", &wxFrame::SetMenuBar, py::keep_alive<1, 2>())
		.def("GetStatusBar", &wxFrame::GetStatusBar, py::return_value_policy::reference)
		.def("SetStatusBar", &wxFrame::SetStatusBar, py::keep_alive<1, 2>())
		.def("SetStatusText", &wxFrame::SetStatusText, text, "number"_a = 0)
		.def("SetStatusWidths", &wxFrame::SetStatusWidths, "n"_a, "widths_field"_a)
		.def("PushStatusText", &wxFrame::PushStatusText, text, "number"_a = 0)
		.def("PopStatusText", &wxFrame::PopStatusText, "number"_a = 0)
		.def("SetStatusBarPane", &wxFrame::SetStatusBarPane, "n"_a)
		.def("GetStatusBarPane", &wxFrame::GetStatusBarPane)
		;

	py::class_<NODELETE(wxMDIParentFrame), wxFrame>(ui, "MDIParentFrame")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, title, pos_v, size_v, style = wxDEFAULT_FRAME_STYLE | wxVSCROLL | wxHSCROLL, name = (const char*)wxFrameNameStr)
		;

	py::class_<NODELETE(wxMDIChildFrame), wxFrame>(ui, "MDIChildFrame")
		.def(py::init<wxMDIParentFrame*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, title, pos_v, size_v, style = wxDEFAULT_FRAME_STYLE, name = (const char*)wxFrameNameStr)
		;

	py::class_<NODELETE(wxDialog), wxTopLevelWindow>(ui, "Dialog")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, title, pos_v, size_v, style = wxDEFAULT_DIALOG_STYLE, name = (const char*)wxDialogNameStr)
		.def("IsModal", &wxDialog::IsModal)
		.def("ShowModal", &wxDialog::ShowModal)
		.def("EndModal", &wxDialog::EndModal, "retCode"_a)
		;
}