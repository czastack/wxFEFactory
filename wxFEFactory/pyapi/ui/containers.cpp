#include <wx/wx.h>
#include <wx/sizer.h>
#include <wx/panel.h>
#include <wx/splitter.h>
#include <wx/notebook.h>
#include <wx/listbook.h>
#include "ui.h"


void UiModule::init_containers()
{
	using namespace py::literals;

	py::arg_v proportion("proportion", 0),
		flag("flag", 0),
		border("border", 0),
		userData("userData", (wxObject*)nullptr);

	py::class_<NODELETE(wxSizerItem)>(ui, "SizerItem")
		.def(py::init<wxWindow*, int, int, int, wxObject*>(),
			window, proportion, flag, border, userData)
		.def(py::init<wxSizer*, int, int, int, wxObject*>(),
			"sizer"_a, proportion, flag, border, userData)
		.def(py::init<int, int, int, int, int, wxObject*>(),
			"width"_a, "height"_a, proportion, flag, border, userData)
		;

	py::class_<NODELETE(wxSizer)>(ui, "Sizer")
		.def("Add", (wxSizerItem * (wxSizer::*)(wxWindow*, int, int, int, wxObject*)) & wxSizer::Add,
			window, proportion, flag, border, userData, py::return_value_policy::reference)
		.def("Add", (wxSizerItem * (wxSizer::*)(wxSizerItem*)) & wxSizer::Add, "item"_a, py::return_value_policy::reference)
		.def("InsertSpacer", &wxSizer::InsertSpacer, "index"_a, "size"_a)
		.def("Layout", &wxSizer::Layout)
		.def("FitInside", &wxSizer::FitInside, window);

	py::class_<NODELETE(wxBoxSizer), wxSizer>(ui, "BoxSizer")
		.def(py::init<int>(), "orient"_a);

	py::class_<NODELETE(wxGridSizer), wxSizer>(ui, "GridSizer")
		.def(py::init<int, int, int>(), "cols"_a, "vgap"_a, "hgap"_a)
		.def(py::init<int, int, int, int>(), "rows"_a, "cols"_a, "vgap"_a, "hgap"_a);

#define ENUM_VAL(name) value(#name, wx##name)

	py::enum_<wxFlexSizerGrowMode>(ui, "FlexSizerGrowMode")
		.ENUM_VAL(FLEX_GROWMODE_NONE)
		.ENUM_VAL(FLEX_GROWMODE_SPECIFIED)
		.ENUM_VAL(FLEX_GROWMODE_ALL)
		.export_values();

	py::class_<NODELETE(wxFlexGridSizer), wxGridSizer>(ui, "FlexGridSizer")
		.def(py::init<int, int, int>(), "cols"_a, "vgap"_a, "hgap"_a)
		.def(py::init<int, int, int, int>(), "rows"_a, "cols"_a, "vgap"_a, "hgap"_a)
		.def("AddGrowableRow", &wxFlexGridSizer::AddGrowableRow, "idx"_a, "proportion"_a = 0)
		.def("RemoveGrowableRow", &wxFlexGridSizer::RemoveGrowableRow, "idx"_a)
		.def("AddGrowableCol", &wxFlexGridSizer::AddGrowableCol, "idx"_a, "proportion"_a = 0)
		.def("RemoveGrowableCol", &wxFlexGridSizer::RemoveGrowableCol, "idx"_a)
		.def("GetFlexibleDirection", &wxFlexGridSizer::GetFlexibleDirection)
		.def("SetFlexibleDirection", &wxFlexGridSizer::SetFlexibleDirection, "direction"_a)
		.def("SetNonFlexibleGrowMode", &wxFlexGridSizer::SetNonFlexibleGrowMode, "mode"_a)
		;

	py::class_<NODELETE(wxPanel), wxWindow>(ui, "Panel")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, pos_v, size_v, style = wxTAB_TRAVERSAL | wxNO_BORDER, name = (const char*)wxPanelNameStr);

	py::class_<NODELETE(wxStaticBox), wxWindow>(ui, "StaticBox")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, label_v, pos_v, size_v, style_0, name = (const char*)wxStaticBoxNameStr);

	py::class_<NODELETE(wxScrolledWindow), wxWindow>(ui, "ScrolledWindow")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, pos_v, size_v, style = wxScrolledWindowStyle, name = (const char*)wxPanelNameStr)
		.def("SetScrollRate", &wxScrolledWindow::SetScrollRate, "xstep"_a, "ystep"_a);

	py::class_<NODELETE(wxSplitterWindow), wxWindow>(ui, "SplitterWindow")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, pos_v, size_v, style = wxSP_3D, name = L"splitter")
		.def("Initialize", &wxSplitterWindow::Initialize, window)
		.def("SplitHorizontally", &wxSplitterWindow::SplitHorizontally, "window1"_a, "window2"_a, "sashPosition"_a = 0)
		.def("SplitVertically", &wxSplitterWindow::SplitVertically, "window1"_a, "window2"_a, "sashPosition"_a = 0);

	py::class_<NODELETE(wxBookCtrlBase), wxControl>(ui, "BookCtrlBase")
		.def("AddPage", &wxBookCtrlBase::AddPage, "page"_a, text, "bSelect"_a = false, "imageId"_a = -1)
		.def("GetPageCount", &wxBookCtrlBase::GetPageCount)
		.def("GetSelection", &wxBookCtrlBase::GetSelection)
		.def("GetPage", &wxBookCtrlBase::GetPage, "n"_a)
		.def("SetSelection", &wxBookCtrlBase::SetSelection, "n"_a)
		.def("SetPageText", &wxBookCtrlBase::SetPageText, "n"_a, text)
		.def("GetPageText", &wxBookCtrlBase::GetPageText, "n"_a);

	py::class_<NODELETE(wxNotebook), wxBookCtrlBase>(ui, "Notebook")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, pos_v, size_v, style_0, name = (const char*)wxNotebookNameStr);

	py::class_<NODELETE(wxListbook), wxBookCtrlBase>(ui, "Listbook")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, pos_v, size_v, style_0, name = wxEmptyString);
}