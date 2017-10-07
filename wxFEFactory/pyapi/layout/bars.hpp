#pragma once
#include <wx/sharedptr.h>
#include <wx/artprov.h>
#include "layoutbase.h"

class ToolBar : public Layout
{
public:
	template <class... Args>
	ToolBar(long direction, long exstyle/*=wxTB_TEXT*/, Args ...args) : Layout(args...)
	{
		bindElem(new wxToolBar(*safeActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), direction | exstyle));
		ctrl().Bind(wxEVT_COMMAND_TOOL_CLICKED, &ToolBar::onClick, this);
	}

	wxToolBar& ctrl() const
	{
		return *(wxToolBar*)m_elem;
	}

	ToolBar& addTool(wxcstr label, wxcstr shortHelp, wxcstr bitmap, pycref onclick, int toolid, wxcstr kind)
	{
		wxBitmap bp;

		if (bitmap.IsEmpty())
		{
			bp = wxNullBitmap;
		}
		else
		{
			bp.LoadFile(bitmap/*, wxBITMAP_TYPE_PNG*/);
		}
		wxToolBarToolBase *tool = ctrl().AddTool(toolid, label, bp, shortHelp, getItemKind(kind));
		if (onclick != None)
		{
			m_listeners[py::cast(tool->GetId())] = onclick;
		}
		return *this;
	}

	ToolBar& addControl(const View &view, wxcstr label, pycref onclick)
	{
		wxToolBarToolBase *tool = ctrl().AddControl((wxControl*)view.ptr(), label);
		if (onclick != None)
		{
			m_listeners[py::cast(tool->GetId())] = onclick;
		}
		return *this;
	}

	ToolBar& addSeparator() {
		ctrl().AddSeparator();
		return *this;
	}

	ToolBar& realize() {
		ctrl().Realize();
		return *this;
	}

	void clear()
	{
		ctrl().ClearTools();
	}

	void onClick(wxCommandEvent &event)
	{
		pycref onclick = pyDictGet(m_listeners, py::cast(event.GetId()));
		if (!onclick.is_none())
		{
			pyCall(onclick, py::cast(this), event.GetId());
		}
	}

	void setToolText(int id, wxcstr label)
	{
		wxToolBarToolBase *tool = ctrl().FindById(id);
		tool->SetLabel(label);
	}

	void doAdd(View &child) override
	{
		addControl(child, wxNoneString, None);
	}

protected:
	py::dict m_listeners;
};


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
		auto ptr = asArray<int>(list, n);
		ctrl().SetFieldsCount(n, ptr.get());
		return *this;
	}

	StatusBar& setItemWidths(pycref list)
	{
		int n;
		auto ptr = asArray<int>(list, n);
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