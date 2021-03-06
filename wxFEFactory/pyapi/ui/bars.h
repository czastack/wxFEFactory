#pragma once
#include <wx/sharedptr.h>
#include <wx/artprov.h>
#include "uibase.h"
#include "wx/aui/auibar.h"

template <class T>
class ToolBarBase : public Layout
{
public:
	template <class... Args>
	ToolBarBase(long wxstyle/*=wxHORIZONTAL|wxTB_TEXT*/, Args ...args) : Layout(args...)
	{
		bindElem(new T(*safeActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), wxstyle));
		ctrl().Bind(wxEVT_COMMAND_TOOL_CLICKED, &ToolBarBase::onClick, this);
	}

	virtual ~ToolBarBase()
	{
		m_listeners.clear();
		m_listeners.release();
	}

	T& ctrl() const
	{
		return *(T*)m_elem;
	}

	int addTool(wxcstr label, wxcstr shortHelp, pycref bitmap, pycref onclick, int toolid, wxcstr kind)
	{
		wxBitmap bp;
		auto *tool = ctrl().AddTool(toolid, label, castBitmap(bitmap, bp), shortHelp, getItemKind(kind));
		toolid = tool->GetId();
		if (!onclick.is(None))
		{
			m_listeners[py::cast(toolid)] = onclick;
		}
		return toolid;
	}

	int addControl(const View &view, wxcstr label, pycref onclick)
	{
		auto *tool = ctrl().AddControl((wxControl*)view.ptr(), label);
		int toolid = tool->GetId();
		if (!onclick.is(None))
		{
			m_listeners[py::cast(tool->GetId())] = onclick;
		}
		return toolid;
	}

	ToolBarBase& addSeparator() {
		ctrl().AddSeparator();
		return *this;
	}

	ToolBarBase& realize() {
		ctrl().Realize();
		return *this;
	}

	void clear()
	{
		ctrl().ClearTools();
	}

	void onClick(wxCommandEvent &event)
	{
		pycref onclick = PyDictGet(m_listeners, py::cast(event.GetId()));
		if (!onclick.is_none())
		{
			PyCall(onclick, py::cast(this), event.GetId());
		}
	}

	void setToolText(int toolid, wxcstr label)
	{
		auto *tool = ctrl().FindById(toolid);
		tool->SetLabel(label);
	}

	int getToolPos(int toolid)
	{
		return ctrl().GetToolPos(toolid);
	}

	void setToolBitmapSize(int w, int h)
	{
		ctrl().SetToolBitmapSize({w, h});
	}

	void doAdd(View &child) override
	{
		addControl(child, wxNoneString, None);
	}

protected:
	py::dict m_listeners;
};


using ToolBar = ToolBarBase<wxToolBar>;
using AuiToolBar = ToolBarBase<wxAuiToolBar>;


class StatusBar : public Control
{
public:
	template <class... Args>
	StatusBar(Args ...args) : Control(args...)
	{
		Layout &layout = *safeActiveLayout();
		bindElem(new wxStatusBar(layout));
		if (wxIsKindOf(layout.ptr(), wxFrame))
		{
			((wxFrame*)layout.ptr())->SetStatusBar((wxStatusBar*)m_elem);
		}
		else
		{
			log_message("StatusBar must be child of Window");
		}
	}

	wxStatusBar& ctrl() const
	{
		return *(wxStatusBar*)m_elem;
	}

	wxString getText(int n) const
	{
		return ctrl().GetStatusText(n);
	}

	StatusBar& setText(wxcstr text, int n)
	{
		ctrl().SetStatusText(text, n);
		return *this;
	}

	StatusBar& setFieldsCount(pycref list)
	{
		int n;
		auto ptr = PyToArray<int>(list, n);
		ctrl().SetFieldsCount(n, ptr.get());
		return *this;
	}

	StatusBar& setItemWidths(pycref list)
	{
		int n;
		auto ptr = PyToArray<int>(list, n);
		ctrl().SetStatusWidths(n, ptr.get());
		return *this;
	}

	int getStatusWidth(int n) const
	{
		return ctrl().GetStatusWidth(n);
	}

	void popStatusText(int n)
	{
		ctrl().PopStatusText(n);
	}

	void pushStatusText(wxcstr text, int n)
	{
		ctrl().PushStatusText(text, n);
	}
};