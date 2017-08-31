#pragma once
#include "layoutbase.h"
#include "menu.h"
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
		m_onclose = None;
	}

	void setMenu(MenuBar &menubar)
	{
		win().SetMenuBar(menubar);
		m_elem->Bind(wxEVT_MENU, &Window::onMenu, this);
		py::cast(&menubar).inc_ref();
	}

	void onMenu(wxCommandEvent &event)
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


class Dialog : public BaseFrame
{
public:
	template <class... Args>
	Dialog(wxcstr title, Args ...args) : BaseFrame(args...)
	{
		bindElem(new wxDialog(safeActiveWindow(), wxID_ANY, title, wxDefaultPosition, getStyleSize(),
			wxDEFAULT_DIALOG_STYLE | wxMINIMIZE_BOX));
		m_elem->Bind(wxEVT_CLOSE_WINDOW, &Dialog::onClose, this);
		m_onclose = None;
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
	void getBoxArg(View &child, int *pFlex, int *pFlag, int *pPadding);

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

	void __exit__(py::args &args) override;

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

	void doAdd(View &child) override;

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

	pyobj __enter__() override;

	void __exit__(py::args &args) override;

	void doAdd(View &child) override
	{
		m_elem->GetSizer()->Add(child, wxSizerFlags(1).Expand().Border(wxALL, 5));
	}
};