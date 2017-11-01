#pragma once
#include "layoutbase.h"
#include "layouts.h"
#include <wx/aui/aui.h>
#include <wx/aui/tabmdi.h>

using AuiItem = Item;


class AuiManager : public Layout
{
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
public:
	template <class... Args>
	AuiNotebook(Args ...args) : Layout(args...)
	{
		bindElem(new wxAuiNotebook(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(),
			wxAUI_NB_TOP | wxAUI_NB_TAB_SPLIT | wxAUI_NB_TAB_MOVE | wxAUI_NB_SCROLL_BUTTONS | wxAUI_NB_CLOSE_ON_ACTIVE_TAB | wxAUI_NB_WINDOWLIST_BUTTON));
		m_elem->Bind(wxEVT_AUINOTEBOOK_PAGE_CLOSE, &AuiNotebook::OnPageClose, this);
	}

	~AuiNotebook()
	{
		
	}

	wxAuiNotebook& ctrl() const
	{
		return *(wxAuiNotebook*)m_elem;
	}

	void doAdd(View &child) override;

	void closePage()
	{
		if (canPageClose())
			ctrl().DeletePage(ctrl().GetSelection());
	}

	bool canPageClose(int n = -1);

	View* getPage(int n)
	{
		return (View*)ctrl().GetPage(n)->GetClientData();
	}

	void OnPageClose(wxAuiNotebookEvent & event)
	{
		if (!canPageClose(event.GetSelection()))
		{
			event.Veto();
		}
		else {
			pyCall(m_children.attr("remove"), py::cast(getPage(event.GetSelection())));
		}
	}

protected:
	py::dict m_close_listeners;
};


using AuiMDIChildFrame = BaseWindow<wxAuiMDIChildFrame>;


class AuiMDIParentFrame : public BaseFrame {
public:
	template <class... Args>
	AuiMDIParentFrame(wxcstr title, MenuBar *menuBar, long exstyle/*=wxDEFAULT_FRAME_STYLE | wxTAB_TRAVERSAL*/, Args ...args) : BaseFrame(args...)
	{
		bindElem(new wxAuiMDIParentFrame(NULL, wxID_ANY, title, wxDefaultPosition, getStyleSize(), exstyle));
		if (menuBar)
		{
			setMenu(*menuBar);
		}
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &Window::onClose, this);
		m_onclose = None;

		m_mgr = new wxAuiManager(m_elem);
	}

	virtual ~AuiMDIParentFrame()
	{
		m_mgr->UnInit();
		delete m_mgr;
	}

	wxAuiMDIParentFrame& win() const
	{
		return *(wxAuiMDIParentFrame*)m_elem;
	}

	void onClose(class wxCloseEvent &event) override
	{
		wxAuiNotebook * notebook = win().GetNotebook();
		if (notebook)
		{
			/// 关闭所有子窗口.
			notebook->DeleteAllPages();
		}

		BaseFrame::onClose(event);
	}


protected:
	wxAuiManager *m_mgr;
};