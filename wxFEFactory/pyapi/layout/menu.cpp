#include <wx/wx.h>
#include "menu.h"

wxVector<MenuHolder*> BaseMenu::MENUS;

bool MenuHolder::onSelect(int id)
{
	pycref item = getMenu(id);
	if (py::isinstance<MenuItem>(item))
	{
		return item.cast<MenuItem>().onSelect();
	}
	return false;
}

Menu::Menu(wxcstr text, wxcstr helpStr)
{
	MenuHolder* parent = getActiveMenu();
	if (parent)
	{
		m_ptr = new wxMenu;
		parent->append(m_ptr, text, helpStr);
		m_handlers_ptr = parent->getHandlers();
	}
	else
	{
		m_ptr = nullptr;
	}
}

void Menu::remove(MenuItem &item)
{
	m_ptr->Remove(item.ptr());
}


void init_menu(py::module &m)
{
	using namespace py::literals;

	py::class_<BaseMenu>(m, "BaseMenu");

	py::class_<MenuHolder, BaseMenu>(m, "MenuHolder")
		.def("__enter__", &MenuHolder::__enter__)
		.def("__exit__", &MenuHolder::__exit__)
		//.def("__getattr__", &MenuHolder::__getattr__)
		;

	py::class_<MenuBar, MenuHolder>(m, "MenuBar")
		.def(py::init<pyobj>(), "onselect"_a = None)
		.def("remove", &MenuBar::remove, "menu"_a);

	py::class_<Menu, MenuHolder>(m, "Menu")
		.def(py::init<wxcstr, wxcstr>(), "text"_a, "helpStr"_a = wxEmptyString)
		.def("remove", &Menu::remove, "menuitem"_a);

	py::class_<ContextMenu, MenuHolder>(m, "ContextMenu")
		.def(py::init<pyobj>(), "onselect"_a = None);

	py::class_t<MenuItem, BaseMenu>(m, "MenuItem")
		.def_init(py::init<wxcstr, wxcstr, wxcstr, int, bool, pyobj>(),
			"text"_a, "helpStr"_a = wxEmptyString, "kind"_a = wxEmptyString,
			"id"_a = -1, "sep"_a = false, "onselect"_a = None)
		.def("getId", &MenuItem::getId)
		.def("getText", &MenuItem::getText)
		.def_readwrite("onselect", &MenuItem::m_onselect)
		.def_property("checked", &MenuItem::isChecked, &MenuItem::check);
}

bool ContextMenu::onSelect(pycref view, int id)
{
	if (MenuHolder::onSelect(id))
	{
		return true;
	}
	else if (!m_onselect.is_none())
	{
		pycref item = getMenu(id);
		pyCall(m_onselect, view, item);
		return true;
	}
	return false;
}

void MenuBar::remove(Menu & m)
{
	for (int i = m_ptr->GetMenuCount() - 1; i >= 0; --i)
	{
		if (m_ptr->GetMenu(i) == m.ptr())
		{
			m_ptr->Remove(i);
		}
	}
}

bool MenuBar::onSelect(int id)
{
	if (MenuHolder::onSelect(id))
	{
		return true;
	}
	else if (!m_onselect.is_none())
	{
		pycref item = getMenu(id);
		pyCall(m_onselect, item);
		return true;
	}
	return false;
}

MenuItem::MenuItem(wxcstr text, wxcstr helpStr, wxcstr kind, int id, bool sep, pycref onselect)
	:m_onselect(onselect)
{
	MenuHolder* parent = getActiveMenu();
	if (parent)
	{
		if (sep && typeid(*parent) == typeid(Menu))
		{
			((Menu*)parent)->appendSeparator();
		}
		m_ptr = parent->append(id, text, helpStr, kind);
	}
	else
	{
		m_ptr = nullptr;
	}
}
