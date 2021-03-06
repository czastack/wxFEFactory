#pragma once
#include "uibase.h"
#include "menu.h"
#include "bars.h"
#include <wx/mdi.h>


class BaseTopLevelWindow : public Layout
{

public:
	using Layout::Layout;

	void init()
	{
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &BaseTopLevelWindow::_onClose, this);
	}

	void __exit__(py::args &args) override;

	void setSize(py::sequence &size);

	pyobj getSize();

	void setPosition(py::sequence &point);

	pyobj getPosition();

	wxString getTitle()
	{
		return ((wxTopLevelWindow*)m_elem)->GetTitle();
	}

	void setTitle(wxcstr title)
	{
		((wxTopLevelWindow*)m_elem)->SetTitle(title);
	}

	bool setIcon(wxcstr path);

	// bool bring_top();

	void setOnClose(pycref onclose)
	{
		_bindEvt((int)wxEVT_CLOSE_WINDOW, onclose, true, false);
	}

	void _onClose(class wxCloseEvent &event);

	bool onClose(class wxCloseEvent &event);

	virtual void onRelease();
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

	void onRelease() override;
};


class Window : public BaseFrame
{
public:
	template <class... Args>
	Window(wxcstr title, MenuBar *menubar, long wxstyle/*=wxDEFAULT_FRAME_STYLE | wxTAB_TRAVERSAL*/, Args ...args) : BaseFrame(args...)
	{
		bindElem(new wxFrame(getActiveWindow(), wxID_ANY, title, wxDefaultPosition, getStyleSize(), wxstyle));
		if (menubar)
		{
			setMenu(*menubar);
		}
		init();
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
		init();
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
		init();
	}
};


class HotkeyWindow : public Window
{
protected:
	py::dict m_hotkey_map;

public:
	template <class... Args>
	HotkeyWindow(Args ...args) : Window(args...)
	{
		m_elem->Bind(wxEVT_HOTKEY, &HotkeyWindow::onHotkey, this);
	}

	virtual ~HotkeyWindow()
	{
		m_hotkey_map.clear();
		m_hotkey_map.release();
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

	void onRelease() override;
};


class ParamEvent : public wxThreadEvent
{
public:
	ParamEvent(wxEventType eventType, WXWPARAM wParam, WXLPARAM lParam): wxThreadEvent(eventType), wParam(wParam), lParam(lParam) {}

	WXWPARAM wParam;
	WXLPARAM lParam;
};


wxDECLARE_EVENT(EVT_KEYHOOK, ParamEvent);


class KeyHookWindow : public Window
{
protected:
	py::dict m_hotkey_map;
	static HMODULE hookDll;
	static HHOOK (*SetHook)(DWORD ownerThreadID, DWORD targetThreadID, bool onKeyUp);
	static void (*UnsetHook)();
public:
	friend class KeyHookThread;

	template <class... Args>
	KeyHookWindow(Args ...args) : Window(args...)
	{
		m_elem->Bind(EVT_KEYHOOK, &KeyHookWindow::onKeyMsg, this);
	}

	virtual ~KeyHookWindow()
	{
		m_hotkey_map.clear();
		m_hotkey_map.release();
	}

	void setHook(DWORD dwThreadId, bool onKeyUp);
	void unsetHook();
	void RegisterHotKeys(py::iterable &items);

	void onKeyMsg(const ParamEvent &event);

	void onRelease() override;

	pyobj getHotkeys()
	{
		return py::module::import("types").attr("MappingProxyType")(m_hotkey_map);
	}
};


class KeyHookThread : public wxThread
{
private:
	KeyHookWindow *m_owner = nullptr;
	DWORD dwThreadId;
	bool onKeyUp;
public:
	KeyHookThread(KeyHookWindow *owner, DWORD dwThreadId, bool onKeyUp) :
		m_owner(owner), dwThreadId(dwThreadId), onKeyUp(onKeyUp)
	{}

	void* Entry() override;
};


class Dialog : public BaseTopLevelWindow
{
public:
	template <class... Args>
	Dialog(wxcstr title, long wxstyle/*=wxDEFAULT_DIALOG_STYLE | wxMINIMIZE_BOX*/, Args ...args) : BaseTopLevelWindow(args...)
	{
		bindElem(new wxDialog(safeActiveWindow(), wxID_ANY, title, wxDefaultPosition, getStyleSize(), 
			wxstyle ? wxstyle : wxDEFAULT_DIALOG_STYLE | wxMINIMIZE_BOX | wxRESIZE_BORDER | wxCLIP_CHILDREN));
		init();
	}

	wxDialog& win() const
	{
		return *(wxDialog*)m_elem;
	}

	void __exit__(py::args &args) override;

	virtual ~Dialog()
	{
		win().Destroy();
	}

	bool showModal()
	{
		return win().ShowModal() == wxID_OK;
	}

	void endModal(bool ok = true)
	{
		win().EndModal(ok ? wxID_OK: wxID_CANCEL);
	}

	bool isModal()
	{
		return win().IsModal();
	}

	void dismiss(bool ok = true);
};
