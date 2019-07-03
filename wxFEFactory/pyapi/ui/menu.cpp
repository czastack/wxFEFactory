#include <wx/wx.h>
#include <wx/menu.h>
#include "ui.h"


void UiModule::init_menu()
{
	using namespace py::literals;

	py::class_<NODELETE(wxMenu), wxEvtHandler>(ui, "Menu")
		.def(py::init<int>(), style_0)
		.def(py::init<const wxString&, int>(), title, style_0)
		.def("AppendSubMenu", &wxMenu::AppendSubMenu, "subemenu"_a, text, "help"_a = wxEmptyString, py::return_value_policy::reference)
		.def("Append", (wxMenuItem * (wxMenu::*)(int, const wxString&, const wxString&, wxItemKind)) & wxMenu::Append,
			"itemid"_a, text=wxEmptyString, "help"_a=wxEmptyString, "kind"_a=wxITEM_NORMAL, py::return_value_policy::reference)
		.def("Remove", (wxMenuItem * (wxMenu::*)(wxMenuItem*)) & wxMenu::Remove, item)
		.def("AppendSeparator", &wxMenu::AppendSeparator, py::return_value_policy::reference)
		.def("GetMenuItemCount", &wxMenu::GetMenuItemCount)
		.def("GetTitle", &wxMenu::GetTitle)
		;


	py::class_<NODELETE(wxMenuBar), wxWindow>(ui, "MenuBar")
		.def(py::init<>())
		.def(py::init<long>(), style)
		// .def(py::init<size_t, wxMenu *[], const wxString[], long>(), "n"_a, "menus"_a, "titles"_a, style_0)
		.def("Append", &wxMenuBar::Append, "menu"_a, title)
		.def("Insert", &wxMenuBar::Insert, pos, "menu"_a, title)
		.def("Remove", &wxMenuBar::Remove)
		.def("GetMenu", &wxMenuBar::GetMenu, pos)
		.def("GetMenuCount", &wxMenuBar::GetMenuCount)
		;


	py::class_<wxMenuItem>(ui, "MenuItem")
		.def("GetItemLabel", &wxMenuItem::GetItemLabel)
		.def("SetItemLabel", &wxMenuItem::SetItemLabel)
		.def("GetId", &wxMenuItem::GetId)
		.def("IsCheck", &wxMenuItem::IsCheck)
		.def("Check", &wxMenuItem::Check, "bDoCheck"_a = true)
		.def("Enable", &wxMenuItem::Enable, "bDoEnable"_a = true)
		;
}