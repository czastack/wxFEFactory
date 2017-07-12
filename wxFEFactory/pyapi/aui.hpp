#pragma once
#include "layoutbase.hpp"
#include <wx/aui/aui.h>

struct AuiItem
{
	AuiItem(View &view, py::kwargs kwargs) :
		m_view(view), m_kwargs(kwargs)
	{
	}

	void __init()
	{
		m_view.ptr()->SetClientData(this);
		py::cast(this).inc_ref();
	}

	operator View &()
	{
		return m_view;
	}

	pyobj m_kwargs;
	View &m_view;
};


class AuiManager : public Layout
{
public:
	AuiManager() : Layout(*getActiveLayout())
	{
		m_mgr = new wxAuiManager(m_elem);
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &AuiManager::onOwnerClose, this);
	}

	~AuiManager()
	{
		m_mgr->UnInit();
		m_elem->Destroy();
		delete m_mgr;
	}

	void onAdd(View &child) override
	{
		AuiItem *item = (AuiItem*)child.ptr()->GetClientData();
		if (isPyDict(item->m_kwargs))
		{
			wxAuiPaneInfo info;

			wxcstr direction = pyDictGet(item->m_kwargs, wxT("direction"), wxNoneString);
			if (direction != wxNoneString)
			{
				if (direction == wxT("top"))
					info.Top();
				else if (direction == wxT("right"))
					info.Right();
				else if (direction == wxT("bottom"))
					info.Bottom();
				else if (direction == wxT("left"))
					info.Left();
				else if (direction == wxT("center"))
					info.Center();
			}

			wxcstr caption = pyDictGet(item->m_kwargs, wxT("caption"), wxNoneString);
			if (caption != wxNoneString)
			{
				info.Caption(caption);
			}

			bool closeButton = pyDictGet(item->m_kwargs, wxT("closeButton"), false);
			if (!closeButton)
			{
				info.CloseButton(closeButton);
			}

			if (item->m_kwargs.contains(wxT("maximizeButton")))
			{
				info.MaximizeButton(pyDictGet(item->m_kwargs, wxT("maximizeButton"), true));
			}

			if (item->m_kwargs.contains(wxT("minimizeButton")))
			{
				info.MinimizeButton(pyDictGet(item->m_kwargs, wxT("minimizeButton"), true));
			}

			if (item->m_kwargs.contains(wxT("captionVisible")))
			{
				info.MinimizeButton(pyDictGet(item->m_kwargs, wxT("captionVisible"), true));
			}

			m_mgr->AddPane(child, info);

			py::cast(item).dec_ref();
		}
		else
		{
			log_message(wxString::Format("Child of %s must be AuiItem.", "AuiManager"));
		}
	}

	void __exit__(py::args &args) override
	{
		LAYOUTS.pop_back();

		for (auto &e : m_children)
		{
			View &child = *py::cast<View*>(e);
			onAdd(child);
		}

		layout();
		// 引用加一，避免被析构
		py::cast(this).inc_ref();
	}

	void reLayout() override
	{
		layout();

		PyList_Type;
	}

	void layout()
	{
		m_mgr->Update();
	}

	void onOwnerClose(class wxCloseEvent &event)
	{
		// 引用减一，销毁对象
		py::cast(this).dec_ref();
		event.Skip();
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

	void onAdd(View &child) override
	{
		AuiItem *item = (AuiItem*)child.ptr()->GetClientData();
		if (isPyDict(item->m_kwargs))
		{
			wxcstr caption = pyDictGet(item->m_kwargs, wxT("caption"), wxNoneString);
			if (caption != wxNoneString)
			{
				
			}
			m_ctrl().AddPage(child, caption);

			py::cast(item).dec_ref();
		}
		else
		{
			log_message(wxString::Format("Child of %s must be AuiItem.", "AuiNotebook"));
		}
	}

	void closePage()
	{
		if (canPageClose())
			m_ctrl().DeletePage(m_ctrl().GetSelection());
	}

	bool canPageClose(int n=-1)
	{
		if (m_ctrl().GetPageCount() == 0)
			return false;

		if (n == -1)
			n = m_ctrl().GetSelection();

		// PageManager *page = (PageManager*)m_ctrl().GetPage(n)->GetClientData();
		// return !page || page->OnClose();
		return true;
	}

	void OnPageClose(wxAuiNotebookEvent & event)
	{
		if (!canPageClose(event.GetSelection()))
		{
			event.Veto();
		}
	}

protected:
	wxAuiNotebook& m_ctrl()
	{
		return *(wxAuiNotebook*)m_elem;
	}
};