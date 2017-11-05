#include <wx/wx.h>
#include "containers.h"


/**
 * 获取布局参数
 */

void SizerLayout::getBoxArg(View & child, int * pFlex, int * pFlag, int * pPadding)
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

void SplitterWindow::__exit__(py::args & args)
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


void BookCtrlBase::doAdd(View & child)
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