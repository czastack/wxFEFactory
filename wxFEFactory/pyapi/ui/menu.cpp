#include <wx/wx.h>
#include <wx/menu.h>
#include "ui.h"


void UiModule::init_menu()
{
	using namespace py::literals;

	py::class_<wxMenu>(ui, "Menu")
		.def(py::init<int>(), style)
		.def(py::init<const wxString&, int>(), title, style)
		.def("AppendSubMenu", &wxMenu::AppendSubMenu)
		.def("Append", (wxMenuItem * (wxMenu::*)(int, const wxString&, const wxString&, wxItemKind)) & wxMenu::Append)
		.def("Remove", (wxMenuItem * (wxMenu::*)(wxMenuItem*)) & wxMenu::Remove)
		.def("AppendSeparator", &wxMenu::AppendSeparator)
		.def("GetMenuItemCount", &wxMenu::GetMenuItemCount)
		.def("GetTitle", &wxMenu::GetTitle)
		;


	py::class_<wxMenuBar, wxWindow>(ui, "MenuBar")
		.def(py::init<>())
		.def(py::init<long>(), style)
		// .def(py::init<size_t, wxMenu *[], const wxString[], long>(), "n"_a, "menus"_a, "titles"_a, style_0)
		.def("Append", &wxMenuBar::Append, "menu"_a, title)
		.def("Insert", &wxMenuBar::Insert, "pos"_a, "menu"_a, title)
		.def("Remove", &wxMenuBar::Remove)
		;


	py::class_<wxMenuItem>(ui, "MenuItem")
		.def("GetItemLabel", &wxMenuItem::GetItemLabel)
		.def("SetItemLabel", &wxMenuItem::SetItemLabel)
		.def("GetId", &wxMenuItem::GetId)
		.def("IsCheck", &wxMenuItem::IsCheck)
		.def("Check", &wxMenuItem::Check, "bDoEnable"_a = true)
		.def("Enable", &wxMenuItem::Enable, "bDoCheck"_a = true)
		;
}