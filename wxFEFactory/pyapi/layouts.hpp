#pragma once
#include "layoutbase.hpp"
#include "menu.hpp"
#include "bars.hpp"
#include <wx/sizer.h>
#include <wx/panel.h>
#include "wx/splitter.h"


class BaseFrame : public Layout
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

	wxString getTitle()
	{
		return ((wxTopLevelWindow*)m_elem)->GetTitle();
	}

	void setTitle(wxcstr title)
	{
		((wxTopLevelWindow*)m_elem)->SetTitle(title);
	}

	void close()
	{
		m_elem->Close();
	}

	virtual void onClose(class wxCloseEvent &event)
	{
		// 引用减一，销毁对象
		py::cast(this).dec_ref();
		event.Skip();
	}
};


class Window : public BaseFrame
{
public:
	template <class... Args>
	Window(wxcstr title, MenuBar *menuBar, Args ...args) : BaseFrame(args...)
	{
		bindElem(new wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, getStyleSize(), wxDEFAULT_FRAME_STYLE | wxTAB_TRAVERSAL));
		if (menuBar)
		{
			setMenu(*menuBar);
		}
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &Window::onClose, this);
	}

	void setMenu(MenuBar &menubar)
	{
		m_win().SetMenuBar(menubar);
		m_elem->Bind(wxEVT_MENU, &Window::onMenu, this);
		py::cast(&menubar).inc_ref();
	}

	void onMenu(wxCommandEvent & event)
	{
		getMenuBar()->onSelect(event.GetId());
	}

	MenuBar* getMenuBar()
	{
		return ((MenuBar*)m_win().GetMenuBar()->GetClientData());
	}

	StatusBar* getStatusBar()
	{
		return ((StatusBar*)m_win().GetStatusBar()->GetClientData());
	}

	void onClose(class wxCloseEvent &event) override
	{
		py::cast(getMenuBar()).dec_ref();
		BaseFrame::onClose(event);
	}

protected:
	wxFrame& m_win()
	{
		return *(wxFrame*)m_elem;
	}
};


class Dialog : public BaseFrame
{
public:
	template <class... Args>
	Dialog(wxcstr title, Args ...args) : BaseFrame(args...)
	{
		bindElem(new wxDialog(NULL, wxID_ANY, title, wxDefaultPosition, getStyleSize(), 
			wxDEFAULT_DIALOG_STYLE | wxMINIMIZE_BOX));
		m_elem->SetSizeHints(wxDefaultSize, wxDefaultSize);
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &Dialog::onClose, this);
	}
};


class SizerLayout : public Layout
{
public:
	using Layout::Layout;

	/**
	* 获取布局参数
	*/
	void getBoxArg(View &child, int *pFlex, int *pFlag, int *pPadding)
	{
		int flag = 0;
		if (child.getStyle(STYLE_EXPAND, false))
		{
			flag |= wxEXPAND;
		}

		wxcstr showPad = child.getStyle(STYLE_SHOWPADDING, wxNoneString);

		if (showPad != wxNoneString)
		{
			if (showPad.size() == 1)
			{
				if (showPad[0] != '0')
					flag |= wxALL;
			}
			else if (showPad.size() == 7)
			{
				if (showPad[0] != '0')
					flag |= wxTOP;
				if (showPad[2] != '0')
					flag |= wxRIGHT;
				if (showPad[4] != '0')
					flag |= wxBOTTOM;
				if (showPad[6] != '0')
					flag |= wxLEFT;
			}
			else {
				log_message(wxString::Format(wxT("%s: %s not available"), STYLE_SHOWPADDING, showPad));
			}
		}

		wxcstr vertical = child.getStyle(STYLE_VERTICALALIGN, wxNoneString);

		if (vertical != wxNoneString)
		{
			if (vertical == wxT("top"))
			{
				flag |= wxALIGN_TOP;
			}
			else if (vertical == wxT("bottom"))
			{
				flag |= wxALIGN_BOTTOM;
			}
			else if (vertical == wxT("center"))
			{
				flag |= wxALIGN_CENTER_VERTICAL;
			}
			else {
				log_message(wxString::Format(wxT("%s: %s not available"), STYLE_VERTICALALIGN, vertical));
			}
		}

		wxcstr align = child.getStyle(STYLE_ALIGN, wxNoneString);

		if (align != wxNoneString)
		{
			if (vertical == wxT("left"))
			{
				flag |= wxALIGN_LEFT;
			}
			else if (vertical == wxT("right"))
			{
				flag |= wxALIGN_RIGHT;
			}
			else if (vertical == wxT("center"))
			{
				flag |= wxALIGN_CENTER_HORIZONTAL;
			}
			else {
				log_message(wxString::Format(wxT("%s: %s not available"), STYLE_ALIGN, vertical));
			}
		}
		*pFlag = flag;
		*pFlex = child.getStyle(STYLE_FLEX, 0);
		*pPadding = child.getStyle(STYLE_PADDING, 5);
	}

	void onAdd(View &child) override
	{
		// Layout::add(child);
		int flex, flag, padding;
		getBoxArg(child, &flex, &flag, &padding);
		m_elem->GetSizer()->Add(child, flex, flag, padding);
	}

	void reLayout() override
	{
		/*
		int flex, flag, padding;
		wxSizerItem *item;
		wxSizer *sizer = m_elem->GetSizer();
		for (auto &child : m_children)
		{
			View * pChild = py::cast<View*>(child);
			item = sizer->GetItem(*pChild);
			getBoxArg(*pChild, &flex, &flag, &padding);

			item->SetProportion(flex);
			item->SetFlag(flag);
			item->SetBorder(padding);
		}*/
		layout();
	}

	virtual void layout() {
		m_elem->GetSizer()->Layout();
	}

	void __exit__(py::args &args) override
	{
		Layout::__exit__(args);
		layout();
	}
};


class LinearLayout : public SizerLayout
{
public:
	template <class... Args>
	LinearLayout(Args ...args) : SizerLayout(args...)
	{
		bindElem(new wxPanel(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize()));
	}

	pyobj __enter__() override
	{
		auto ret = Layout::__enter__();
		m_elem->SetSizer(new wxBoxSizer(getDirection()));
		return ret;
	}
protected:
	virtual wxOrientation getDirection() = 0;
};


class Vertical : public LinearLayout
{
public:
	using LinearLayout::LinearLayout;
	wxOrientation getDirection() override
	{
		return wxVERTICAL;
	}
};


class Horizontal : public LinearLayout
{
public:
	using LinearLayout::LinearLayout;
	wxOrientation getDirection() override
	{
		return wxHORIZONTAL;
	}
};


class GridLayout : public SizerLayout
{
public:
	template <class... Args>
	GridLayout(int rows, int cols, int vgap, int hgap, Args ...args) : SizerLayout(args...)
	{
		bindElem(new wxPanel(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize()));
		m_elem->SetSizer(new wxGridSizer(rows, cols, vgap, hgap));
	}
};


class FlexGridLayout : public SizerLayout
{
public:
	template <class... Args>
	FlexGridLayout(int rows, int cols, int vgap, int hgap, Args ...args) : SizerLayout(args...)
	{
		bindElem(new wxPanel(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize()));
		
		wxFlexGridSizer* sizer = new wxFlexGridSizer(rows, cols, vgap, hgap);
		sizer->SetFlexibleDirection(wxBOTH);
		sizer->SetNonFlexibleGrowMode(wxFLEX_GROWMODE_SPECIFIED);
		m_elem->SetSizer(sizer);
	}
};


class ScrollView : public SizerLayout
{
public:
	template <class... Args>
	ScrollView(bool horizontal, Args ...args) : SizerLayout(args...)
	{
		bindElem(new wxScrolledWindow(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(),
			wxHSCROLL | wxVSCROLL));
		m_elem->SetSizer(new wxBoxSizer(horizontal ? wxHORIZONTAL: wxVERTICAL));
		m_ctrl().SetScrollRate(5, 5);
	}

	void layout() override
	{
		m_elem->GetSizer()->FitInside(m_elem);
		m_elem->Layout();
	}

protected:
	wxScrolledWindow& m_ctrl()
	{
		return *(wxScrolledWindow*)m_elem;
	}
};


class SplitterWindow : public Layout
{
public:
	template <class... Args>
	SplitterWindow(bool horizontal, int sashpos, Args ...args) : Layout(args...), m_horizontal(horizontal), m_sashpos(sashpos)
	{
		bindElem(new wxSplitterWindow(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize()));
	}

	void __exit__(py::args &args) override
	{
		int len = m_children.size();
		if (len > 2)
		{
			log_message("SplitterWindow 不支持大于2个子元素");
			return;
		}
		Layout::__exit__(args);
		if (len == 1)
		{
			View &child = *py::cast<View*>(m_children[0]);
			m_ctrl().Initialize(child);
		}
		else if (len == 2)
		{
			View &child1 = *py::cast<View*>(m_children[0]);
			View &child2 = *py::cast<View*>(m_children[1]);
			if (m_horizontal)
				m_ctrl().SplitHorizontally(child1, child2, m_sashpos);
			else
				m_ctrl().SplitVertically(child1, child2, m_sashpos);
		}
	}

	bool isHorizontal()
	{
		return m_horizontal;
	}

protected:
	bool m_horizontal;
	int m_sashpos;

	wxSplitterWindow& m_ctrl()
	{
		return *(wxSplitterWindow*)m_elem;
	}
};


