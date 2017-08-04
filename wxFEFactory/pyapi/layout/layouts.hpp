#pragma once
#include "layoutbase.hpp"
#include "menu.hpp"
#include "bars.hpp"
#include <wx/sizer.h>
#include <wx/panel.h>
#include <wx/splitter.h>
#include <wx/notebook.h>


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
		win().SetMenuBar(menubar);
		m_elem->Bind(wxEVT_MENU, &Window::onMenu, this);
		py::cast(&menubar).inc_ref();
	}

	void onMenu(wxCommandEvent & event)
	{
		getMenuBar()->onSelect(event.GetId());
	}

	MenuBar* getMenuBar()
	{
		auto menubar = win().GetMenuBar();
		return menubar ? ((MenuBar*)menubar->GetClientData()): nullptr;
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

		BaseFrame::onClose(event);
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

protected:
	wxFrame& win()
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
		bindElem(new wxDialog(safeActiveWindow(), wxID_ANY, title, wxDefaultPosition, getStyleSize(),
			wxDEFAULT_DIALOG_STYLE | wxMINIMIZE_BOX));
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &Dialog::onClose, this);
	}

	bool showOnce()
	{
		bool ret = win().ShowModal() == wxID_OK;
		win().Destroy();
		return ret;
	}

	void endModal()
	{
		win().EndModal(wxID_OK);
	}

protected:
	wxDialog& win()
	{
		return *(wxDialog*)m_elem;
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
			else if (vertical == wxT("middle"))
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

	void doAdd(View &child) override
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
		sizer->SetNonFlexibleGrowMode(wxFLEX_GROWMODE_SPECIFIED);
		m_elem->SetSizer(sizer);
	}

	void AddGrowableRow(size_t idx, int proportion = 0) { get_sizer().AddGrowableRow(idx, proportion); }
	void RemoveGrowableRow(size_t idx) { get_sizer().RemoveGrowableRow(idx); }
	void AddGrowableCol(size_t idx, int proportion = 0) { get_sizer().AddGrowableCol(idx, proportion); }
	void RemoveGrowableCol(size_t idx) { get_sizer().RemoveGrowableCol(idx); }

	void SetFlexibleDirection(int direction) { get_sizer().SetFlexibleDirection(direction); }
	int GetFlexibleDirection() const { return get_sizer().GetFlexibleDirection(); }

	wxFlexGridSizer& get_sizer() const
	{
		return *(wxFlexGridSizer*)m_elem->GetSizer();
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
		ctrl().SetScrollRate(5, 5);
	}

	void layout() override
	{
		m_elem->GetSizer()->FitInside(m_elem);
		m_elem->Layout();
	}
	wxScrolledWindow& ctrl()
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
			ctrl().Initialize(child);
		}
		else if (len == 2)
		{
			View &child1 = *py::cast<View*>(m_children[0]);
			View &child2 = *py::cast<View*>(m_children[1]);
			if (m_horizontal)
				ctrl().SplitHorizontally(child1, child2, m_sashpos);
			else
				ctrl().SplitVertically(child1, child2, m_sashpos);
		}
	}

	bool isHorizontal()
	{
		return m_horizontal;
	}

	wxSplitterWindow& ctrl()
	{
		return *(wxSplitterWindow*)m_elem;
	}

protected:
	bool m_horizontal;
	int m_sashpos;
};


class StaticBox : public SizerLayout
{
public:
	template <class... Args>
	StaticBox(wxcstr label, Args ...args) : SizerLayout(args...)
	{
		bindElem(new wxStaticBox(*getActiveLayout(), wxID_ANY, label, wxDefaultPosition, getStyleSize()));
		wxSizer* sizer = new wxBoxSizer(wxVERTICAL);
		sizer->InsertSpacer(0, 15);
		m_elem->SetSizer(sizer);
	}
};


class Notebook : public Layout
{
public:
	template <class... Args>
	Notebook(Args ...args) : Layout(args...)
	{
		bindElem(new wxNotebook(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize()));
	}

	void doAdd(View &child) override
	{
		Item *item = (Item*)child.ptr()->GetClientData();
		if (Item::isInstance(item))
		{
			// 替换回原指针
			child.ptr()->SetClientData(&child);

			wxcstr caption = pyDictGet(item->m_kwargs, wxT("caption"), wxNoneString);
			ctrl().AddPage(child, caption);

			py::cast(item).dec_ref();
		}
		else
		{
			log_message(wxString::Format("Child of %s must be Item.", "Notebook"));
		}
	}

	size_t getPageCount() const {
		return ctrl().GetPageCount();
	}

	int getSelection() {
		return ctrl().GetSelection();
	}

	int setSelection(int n) {
		return ctrl().SetSelection(n);
	}

	bool setPageText(size_t n, wxcstr text)
	{
		return ctrl().SetPageText(n, text);
	}

	wxString getPageText(size_t n) const
	{
		return ctrl().GetPageText(n);
	}

	View* getPage(int n)
	{
		return (View*)ctrl().GetPage(n)->GetClientData();
	}

	wxNotebook& ctrl() const
	{
		return *(wxNotebook*)m_elem;
	}
};


class StdModalDialog : public Dialog
{
public:
	using Dialog::Dialog;

	pyobj __enter__() override
	{
		long style = m_elem->GetWindowStyle();
		style |= wxRESIZE_BORDER | wxCLIP_CHILDREN;
		m_elem->SetWindowStyle(style);

		auto ret = Layout::__enter__();
		wxSizer* topsizer = new wxBoxSizer(wxVERTICAL);
		m_elem->SetSizer(topsizer);
		return ret;
	}

	void __exit__(py::args &args) override
	{
		Layout::__exit__(args);

		wxStdDialogButtonSizer* buttonSizer = new wxStdDialogButtonSizer();
		buttonSizer->AddButton(new wxButton(m_elem, wxID_OK));
		buttonSizer->AddButton(new wxButton(m_elem, wxID_CANCEL));
		buttonSizer->Realize();

		wxSizer* topsizer = m_elem->GetSizer();
		topsizer->Add(buttonSizer, wxSizerFlags(0).Right().Border(wxBOTTOM | wxRIGHT, 5));
	}

	void doAdd(View &child) override
	{
		m_elem->GetSizer()->Add(child, wxSizerFlags(1).Expand().Border(wxALL, 5));
	}
};