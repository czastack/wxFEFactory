#pragma once
#include "layoutbase.h"
#include <wx/sizer.h>
#include <wx/panel.h>
#include <wx/splitter.h>
#include <wx/notebook.h>
#include <wx/listbook.h>


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

	wxScrolledWindow& ctrl() const
	{
		return *(wxScrolledWindow*)m_elem;
	}

	void layout() override
	{
		m_elem->GetSizer()->FitInside(m_elem);
		m_elem->Layout();
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

	wxSplitterWindow& ctrl() const
	{
		return *(wxSplitterWindow*)m_elem;
	}

	void __exit__(py::args &args) override;

	bool isHorizontal()
	{
		return m_horizontal;
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


class BookCtrlBase : public Layout
{
public:
	using Layout::Layout;
	wxBookCtrlBase& ctrl() const
	{
		return *(wxBookCtrlBase*)m_elem;
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

	View* getPage(int n = -1);

	virtual void setOnPageChange(pycref fn, bool reset = true) = 0;
};


class Notebook : public BookCtrlBase
{
public:
	template <class... Args>
	Notebook(long wxstyle, Args ...args) : BookCtrlBase(args...)
	{
		bindElem(new wxNotebook(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), wxstyle));
	}

	void setOnPageChange(pycref fn, bool reset = true) override
	{
		bindEvt(wxEVT_NOTEBOOK_PAGE_CHANGED, fn, reset);
	}
};


class Listbook : public BookCtrlBase
{
public:
	template <class... Args>
	Listbook(long wxstyle, Args ...args) : BookCtrlBase(args...)
	{
		bindElem(new wxListbook(*getActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), wxstyle));
	}

	void setOnPageChange(pycref fn, bool reset = true) override
	{
		bindEvt(wxEVT_LISTBOOK_PAGE_CHANGED, fn, reset);
	}
};

void init_containers(py::module &m);