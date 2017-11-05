#pragma once
#include "layoutbase.h"
#include "menu.h"
#include "bars.hpp"
#include <wx/mdi.h>


class BaseTopLevelWindow : public Layout
{
public:
	using Layout::Layout;

	void __exit__(py::args &args) override
	{
		Layout::__exit__(args);
		m_elem->Show();
		if (!m_elem->GetParent())
		{
			py::cast(this).inc_ref();
		}
	}

	void setSize(py::tuple &size)
	{
		m_elem->SetSize({ size[0].cast<int>(), size[1].cast<int>() });
	}

	pyobj getSize()
	{
		py::tuple ret = py::tuple(2);
		const wxSize &sz = m_elem->GetSize();
		ret[0] = sz.GetWidth();
		ret[1] = sz.GetHeight();
		return ret;
	}

	void setPosition(py::tuple &point)
	{
		m_elem->SetPosition({ point[0].cast<int>(), point[1].cast<int>() });
	}

	pyobj getPosition()
	{
		py::tuple ret = py::tuple(2);
		const wxPoint &pt = m_elem->GetPosition();
		ret[0] = pt.x;
		ret[1] = pt.y;
		return ret;
	}

	wxString getTitle()
	{
		return ((wxTopLevelWindow*)m_elem)->GetTitle();
	}

	void setTitle(wxcstr title)
	{
		((wxTopLevelWindow*)m_elem)->SetTitle(title);
	}

	bool setIcon(wxcstr path)
	{
		wxIcon icon;
		wxBitmapType type = (wxBitmapType)getBitmapTypeByExt(path);
		if (type)
		{
			icon.LoadFile(path, type);
			((wxTopLevelWindow*)m_elem)->SetIcon(icon);
			return true;
		}
		return false;
	}

	void setOnClose(pycref onclose)
	{
		m_onclose = onclose;
	}

	void close()
	{
		m_elem->Close();
	}

	virtual void onClose(class wxCloseEvent &event)
	{
		if (!m_onclose.is_none())
		{
			handleEvent(m_onclose, event);
		}

		// 引用减一，销毁对象
		py::cast(this).dec_ref();
		event.Skip();
	}

protected:
	pyobj m_onclose;
};


class BaseFrame : public BaseTopLevelWindow {
public:
	using BaseTopLevelWindow::BaseTopLevelWindow;
	wxFrame& win() const
	{
		return *(wxFrame*)m_elem;
	}

	void setMenu(MenuBar &menubar)
	{
		win().SetMenuBar(menubar);
		m_elem->Bind(wxEVT_MENU, &BaseFrame::onMenu, this);
		py::cast(&menubar).inc_ref();
	}

	void onMenu(wxCommandEvent &event)
	{
		getMenuBar()->onSelect(event.GetId());
	}

	MenuBar* getMenuBar()
	{
		auto menubar = win().GetMenuBar();
		return menubar ? ((MenuBar*)menubar->GetClientData()) : nullptr;
	}

	StatusBar* getStatusBar()
	{
		return ((StatusBar*)win().GetStatusBar()->GetClientData());
	}

	void onClose(class wxCloseEvent &event) override
	{
		auto menubar = getMenuBar();

		if (menubar)
			py::cast(menubar).dec_ref();

		BaseTopLevelWindow::onClose(event);
	}

	bool isKeepTop()
	{
		long style = m_elem->GetWindowStyle();
		return (style & wxSTAY_ON_TOP) != 0;
	}

	void keepTop(bool top)
	{
		long style = m_elem->GetWindowStyle();
		if (top)
		{
			style |= wxSTAY_ON_TOP;
		}
		else {
			style &= ~wxSTAY_ON_TOP;
		}
		m_elem->SetWindowStyle(style);
	}
};


class Window : public BaseFrame
{
public:
	template <class... Args>
	Window(wxcstr title, MenuBar *menubar, long wxstyle/*=wxDEFAULT_FRAME_STYLE | wxTAB_TRAVERSAL*/, Args ...args) : BaseFrame(args...)
	{
		bindElem(new wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, getStyleSize(), wxstyle));
		if (menubar)
		{
			setMenu(*menubar);
		}
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &Window::onClose, this);
		m_onclose = None;
	}
};


class MDIParentFrame : public BaseFrame
{
public:
	template <class... Args>
	MDIParentFrame(wxcstr title, MenuBar *menubar, long wxstyle, Args ...args) : BaseFrame(args...)
	{
		bindElem(new wxMDIParentFrame(getActiveWindow(), wxID_ANY, title, wxDefaultPosition, getStyleSize(), wxstyle));
		if (!menubar)
		{
			menubar = new MenuBar(None);
		}
		setMenu(*menubar);
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &MDIParentFrame::onClose, this);
		m_onclose = None;
	}
};


class MDIChildFrame : public BaseFrame
{
public:
	template <class... Args>
	MDIChildFrame(wxcstr title, MenuBar *menubar, long wxstyle, Args ...args) : BaseFrame(args...)
	{
		wxMDIParentFrame *parent = (wxMDIParentFrame*)getActiveWindow();
		bindElem(new wxMDIChildFrame(parent, wxID_ANY, title, wxDefaultPosition, getStyleSize(), wxstyle));
		if (menubar)
		{
			setMenu(*menubar);
		}
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &MDIChildFrame::onClose, this);
		m_onclose = None;
	}
};


class HotkeyWindow : public Window
{
public:
	template <class... Args>
	HotkeyWindow(Args ...args) : Window(args...)
	{
		m_elem->Bind(wxEVT_HOTKEY, &HotkeyWindow::onHotkey, this);
	}

	bool prepareHotkey(pyobj &hotkeyId, WORD &int_hotkeyId);

	void RegisterHotKey(pyobj hotkeyId, int modifiers, int virtualKeyCode, pycref onhotkey);

	void RegisterHotKeys(py::iterable & items);

	void UnregisterHotKey(pyobj hotkeyId, bool force = false);

	void stopHotkey();

	void onHotkey(wxKeyEvent &event);

	pyobj getHotkeys()
	{
		return py::module::import("types").attr("MappingProxyType")(m_hotkey_map);
	}

	void onClose(class wxCloseEvent &event) override
	{
		stopHotkey();

		Window::onClose(event);
	}

protected:
	py::dict m_hotkey_map;
};


class Dialog : public BaseTopLevelWindow
{
public:
	template <class... Args>
	Dialog(wxcstr title, long wxstyle/*=wxDEFAULT_DIALOG_STYLE | wxMINIMIZE_BOX*/, Args ...args) : BaseTopLevelWindow(args...)
	{
		bindElem(new wxDialog(safeActiveWindow(), wxID_ANY, title, wxDefaultPosition, getStyleSize(), wxstyle));
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &Dialog::onClose, this);
		m_onclose = None;
	}

	wxDialog& win() const
	{
		return *(wxDialog*)m_elem;
	}

	virtual ~Dialog()
	{
		win().Destroy();
	}

	bool showModal()
	{
		return win().ShowModal() == wxID_OK;
	}

	void endModal()
	{
		win().EndModal(wxID_OK);
	}

};


class StdModalDialog : public Dialog
{
public:
	using Dialog::Dialog;

	pyobj __enter__() override;

	void __exit__(py::args &args) override;

	void doAdd(View &child) override
	{
		m_elem->GetSizer()->Add(child, wxSizerFlags(1).Expand().Border(wxALL, 5));
	}
};