#pragma once
#include "layoutbase.h"
#include "frames.h"
#include <wx/aui/aui.h>
#include <wx/aui/tabmdi.h>

using AuiItem = Item;


class AuiManager : public Layout
{
protected:
	py::dict m_close_listeners;

public:
	AuiManager() : Layout(*safeActiveLayout())
	{
		m_mgr = new wxAuiManager(m_elem);
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &AuiManager::onOwnerClose, this);
	}

	~AuiManager()
	{
		m_mgr->UnInit();
		delete m_mgr;
		m_close_listeners.clear();
		m_close_listeners.release();
	}

	void doAdd(View &child) override;

	void __exit__(py::args &args) override;

	void reLayout() override
	{
		layout();
	}

	void layout()
	{
		m_mgr->Update();
	}

	void onOwnerClose(class wxCloseEvent &event)
	{
		event.Skip();
		// 引用减一，销毁对象
		py::cast(this).release().dec_ref();
		// delete this;
		m_mgr->UnInit();
	}

	void hidePane(wxcstr name)
	{
		m_mgr->GetPane(name).Hide();
		layout();
	}

	void showPane(wxcstr name, bool show)
	{
		m_mgr->GetPane(name).Show(show);
		layout();
	}

	void togglePane(wxcstr name)
	{
		wxAuiPaneInfo &pane = m_mgr->GetPane(name);
		if (pane.IsShown())
			pane.Hide();
		else
			pane.Show();
		layout();
	}

protected:
	wxAuiManager *m_mgr;
};


class AuiNotebook: public Layout
{
protected:
	py::dict m_close_listeners;

public:
	template <class... Args>
	AuiNotebook(Args ...args) : Layout(args...)
	{
		bindElem(new wxAuiNotebook(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(),
			wxAUI_NB_TOP | wxAUI_NB_TAB_SPLIT | wxAUI_NB_TAB_MOVE | wxAUI_NB_SCROLL_BUTTONS | wxAUI_NB_CLOSE_ON_ACTIVE_TAB | wxAUI_NB_WINDOWLIST_BUTTON));
		m_elem->Bind(wxEVT_AUINOTEBOOK_PAGE_CLOSE, &AuiNotebook::OnPageClose, this);
	}

	virtual ~AuiNotebook()
	{
		m_close_listeners.clear();
		m_close_listeners.release();
	}

	wxAuiNotebook& ctrl() const
	{
		return *(wxAuiNotebook*)m_elem;
	}

	void doAdd(View &child) override;

	int getSelection()
	{
		return ctrl().GetSelection();
	}

	void setSelection(int n)
	{
		ctrl().SetSelection(n);
	}

	int getPageCount()
	{
		return ctrl().GetPageCount();
	}

	bool canPageClose(int n = -1);

	View* getPage(int n = -1);

	void _removePage(int n);

	void OnPageClose(wxAuiNotebookEvent & event);

	bool closePage(int n = -1);

	bool closeAllPage();
};


class AuiMDIParentFrame : public BaseFrame {
protected:
	wxAuiManager *m_mgr;

public:
	template <class... Args>
	AuiMDIParentFrame(wxcstr title, MenuBar *menubar, long wxstyle/*=wxDEFAULT_FRAME_STYLE | wxTAB_TRAVERSAL*/, Args ...args) : BaseFrame(args...)
	{
		bindElem(new wxAuiMDIParentFrame(NULL, wxID_ANY, title, wxDefaultPosition, getStyleSize(), wxstyle));
		if (!menubar)
		{
			menubar = new MenuBar(None);
		}
		setMenu(*menubar);
		init();

		m_mgr = new wxAuiManager(m_elem);
	}

	wxAuiMDIParentFrame& win() const
	{
		return *(wxAuiMDIParentFrame*)m_elem;
	}

	void onRelease() override;
};


class AuiMDIChildFrame : public BaseTopLevelWindow
{
public:
	template <class... Args>
	AuiMDIChildFrame(wxcstr title, long wxstyle, Args ...args) : BaseTopLevelWindow(args...)
	{
		wxAuiMDIParentFrame *parent = (wxAuiMDIParentFrame*)getActiveWindow();
		bindElem(new wxAuiMDIChildFrame(parent, wxID_ANY, title, wxDefaultPosition, getStyleSize(), wxstyle));
		init();
	}

	void __exit__(py::args &args) override
	{
		Layout::__exit__(args);
	}
};