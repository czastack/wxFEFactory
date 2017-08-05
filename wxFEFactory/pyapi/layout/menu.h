#pragma once
#include "../pyutils.h"
#include "../fefactory_api.h"
#include "../functions.h"
#include "myapp.h"


class BaseMenu
{
public:
	static wxVector<class MenuHolder*> MENUS;

	static class MenuHolder* getActiveMenu()
	{
		return MENUS.empty() ? nullptr : MENUS.back();
	}

	friend void init_menu(py::module &m);
};

class MenuHolder : public BaseMenu
{
public:
	virtual void append(wxMenu *menu, wxcstr text, wxcstr helpStr) = 0;
	virtual wxMenuItem* append(int id, wxcstr text, wxcstr helpStr, wxcstr kindStr) = 0;
	virtual py::dict* getHandlers() = 0;

	pyobj __enter__() {
		MENUS.push_back(this);
		return py::cast(this);
	}

	void __exit__(py::args &args) {
		MENUS.pop_back();
	}

	/*pyobj __getattr__(pyobj key)
	{
	return pyDictGet(m_named_children, key);
	}*/

	pyobj getMenu(int id)
	{
		return pyDictGet(*getHandlers(), py::cast(id));
	}

	void setMenu(int id, pycref item)
	{
		(*getHandlers())[py::cast(id)] = item;
	}

	bool onSelect(int id);

protected:
	py::list m_children;
};


class Menu : public MenuHolder
{
public:
	Menu(py::dict *handlers_ptr) : m_ptr(new wxMenu), m_handlers_ptr(handlers_ptr)
	{

	}

	Menu(wxcstr text, wxcstr helpStr);

	void append(wxMenu *menu, wxcstr text, wxcstr helpStr) override
	{
		m_ptr->AppendSubMenu(menu, text, helpStr);
	}

	wxMenuItem* append(int id, wxcstr text, wxcstr helpStr, wxcstr kind) override
	{
		return m_ptr->Append(id, text, helpStr, getItemKind(kind));
	}

	void remove(class MenuItem &item);

	py::dict* getHandlers() override
	{
		return m_handlers_ptr;
	}

	void appendSeparator()
	{
		m_ptr->AppendSeparator();
	}

	wxString getText()
	{
		return m_ptr->GetTitle();
	}

	wxMenu* ptr()
	{
		return m_ptr;
	}

protected:
	wxMenu *m_ptr;
	py::dict *m_handlers_ptr;
};


/**
 * ÓÒ¼ü²Ëµ¥¸ù²Ëµ¥
 */
class ContextMenu: public Menu
{
public:
	ContextMenu(pycref onselect): Menu(&m_handlers), m_onselect(onselect)
	{

	}

	bool onSelect(pycref view, int id);

private:
	py::dict m_handlers;
	pyobj m_onselect;
};


class MenuBar : public MenuHolder
{
public:
	MenuBar(pycref onselect) : m_ptr(new wxMenuBar(0)), m_onselect(onselect)
	{
		m_ptr->SetClientData(this);
	}

	void append(wxMenu *menu, wxcstr text, wxcstr helpStr) override
	{
		m_ptr->Append(menu, text);
	}

	wxMenuItem* append(int id, wxcstr text, wxcstr helpStr, wxcstr kind) override
	{
		log_message(wxT("Child of MenuBar must be Menu."));
		return nullptr;
	}

	void remove(Menu &m);

	py::dict* getHandlers() override
	{
		return &m_handlers;
	}

	bool onSelect(int id);

	operator wxMenuBar*()
	{
		return m_ptr;
	}

protected:
	wxMenuBar *m_ptr;
	py::dict m_handlers;
	pyobj m_onselect;
};


class MenuItem : public BaseMenu
{
public:
	MenuItem(wxcstr text, wxcstr helpStr, wxcstr kind, int id, bool sep, pycref onselect);

	void __init()
	{
		if (m_ptr)
		{
			MenuHolder* parent = getActiveMenu();
			parent->setMenu(getId(), py::cast(this));
		}
	}

	wxMenuItem* ptr() const
	{
		return m_ptr;
	}

	wxString getText()
	{
		return m_ptr->GetItemLabel();
	}

	int getId()
	{
		return m_ptr->GetId();
	}

	bool onSelect()
	{
		if (!m_onselect.is_none())
		{
			pyCall(m_onselect, py::cast(this));
			return true;
		}
		return false;
	}

	bool isChecked()
	{
		return m_ptr->IsCheck();
	}

	void check(bool checked=true)
	{
		m_ptr->Check(checked);
	}

	friend void init_menu(py::module &m);

private:
	wxMenuItem *m_ptr;
	pyobj m_onselect;
};


void init_menu(py::module &m);