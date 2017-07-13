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
	AuiManager(pycref key) : Layout(*getActiveLayout())
	{
		m_mgr = new wxAuiManager(m_elem);
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &AuiManager::onOwnerClose, this);
		if (key != None)
		{
			m_key = key;
		}
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

			// 替换回原指针
			child.ptr()->SetClientData(&child);

			pyobj data;

			data = pyDictGet(item->m_kwargs, wxT("name"));
			if (data != None)
			{
				info.Name(data.cast<wxString>());
			}

			data = pyDictGet(item->m_kwargs, wxT("direction"));
			if (data != None)
			{
				wxcstr direction = data.cast<wxString>();

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

			data = pyDictGet(item->m_kwargs, wxT("caption"));
			if (data != None)
			{
				info.Caption(data.cast<wxString>());
			}

			if (!pyDictGet(item->m_kwargs, wxT("closeButton"), false))
			{
				info.CloseButton(false);
			}

			data = pyDictGet(item->m_kwargs, wxT("maximizeButton"));
			if (data != None)
			{
				info.MaximizeButton(data.cast<bool>());
			}

			data = pyDictGet(item->m_kwargs, wxT("minimizeButton"));
			if (data != None)
			{
				info.MinimizeButton(data.cast<bool>());
			}

			data = pyDictGet(item->m_kwargs, wxT("captionVisible"));
			if (data != None)
			{
				info.MinimizeButton(data.cast<bool>());
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

		pyobj &self = py::cast(this);
		if (m_key == None)
		{
			// 引用加一，避免被析构
			self.inc_ref();
		}
		else {
			getActiveLayout()->addNamed(m_key, self);
		}
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
		event.Skip();
		// 引用减一，销毁对象
		py::cast(this).dec_ref();
	}

	void hidePane(wxcstr name)
	{
		m_mgr->GetPane(name).Hide();
		layout();
	}

	void showPane(wxcstr name)
	{
		m_mgr->GetPane(name).Show();
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

	void onAdd(View &child) override
	{
		AuiItem *item = (AuiItem*)child.ptr()->GetClientData();
		if (isPyDict(item->m_kwargs))
		{
			// 替换回原指针
			child.ptr()->SetClientData(&child);

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
		else {
			pyCall(m_children.attr("remove"), py::cast((View*)m_ctrl().GetPage(event.GetSelection())->GetClientData()));
		}
	}

protected:
	wxAuiNotebook& m_ctrl()
	{
		return *(wxAuiNotebook*)m_elem;
	}
};