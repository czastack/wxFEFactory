#include <wx/wx.h>
#include "layouts.h"

bool HotkeyWindow::prepareHotkey(pyobj & hotkeyId, WORD & int_hotkeyId)
{
	if (PY_IS_TYPE(hotkeyId, PyUnicode))
	{
		int_hotkeyId = GlobalAddAtom(py::cast<wxString>(hotkeyId));
		hotkeyId = py::int_(int_hotkeyId);
	}
	else if (PY_IS_TYPE(hotkeyId, PyLong))
	{
		int_hotkeyId = py::cast<int>(hotkeyId);
	}
	else
	{
		py::print(hotkeyId, "不支持的格式");
		return false;
	}
	return true;
}

void HotkeyWindow::RegisterHotKey(pyobj hotkeyId, int modifiers, int virtualKeyCode, pycref onhotkey)
{
	WORD _hotkeyId;
	if (prepareHotkey(hotkeyId, _hotkeyId))
	{
		if (m_hotkey_map.contains(hotkeyId))
		{
			py::print(hotkeyId, "已经在使用了");
			return;
		}
		if (m_elem->RegisterHotKey(_hotkeyId, modifiers, virtualKeyCode))
		{
			m_hotkey_map[hotkeyId] = onhotkey;
			onhotkey.inc_ref();
		}
		else {
			py::print(hotkeyId, "热键注册失败");
		}
	}
}

void HotkeyWindow::UnregisterHotKey(pyobj hotkeyId, bool force)
{
	WORD _hotkeyId;
	if (prepareHotkey(hotkeyId, _hotkeyId))
	{
		if (force || m_hotkey_map.contains(hotkeyId))
		{
			m_elem->UnregisterHotKey(_hotkeyId);
		}
	}
}

void HotkeyWindow::stopHotkey()
{
	wxChar buf[32];
	int hotkeyId;
	for (auto e : m_hotkey_map)
	{
		hotkeyId = e.first.cast<WORD>();
		GlobalGetAtomName(hotkeyId, buf, 32);
		if (!wxIsEmpty(buf))
		{
			GlobalDeleteAtom(hotkeyId);
		}
		m_elem->UnregisterHotKey(hotkeyId);
	}
}

void HotkeyWindow::onHotkey(wxKeyEvent & event)
{
	pycref hotkeyId = py::cast(event.GetId());
	pycref ret = pyCall(m_hotkey_map[hotkeyId], hotkeyId);
	if (!PyObject_IsTrue(ret.ptr()))
	{
		event.Skip();
	}
}

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

void Notebook::doAdd(View & child)
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

pyobj StdModalDialog::__enter__()
{
	long style = m_elem->GetWindowStyle();
	style |= wxRESIZE_BORDER | wxCLIP_CHILDREN;
	m_elem->SetWindowStyle(style);

	auto ret = Layout::__enter__();
	wxSizer* topsizer = new wxBoxSizer(wxVERTICAL);
	m_elem->SetSizer(topsizer);
	return ret;
}

void StdModalDialog::__exit__(py::args & args)
{
	Layout::__exit__(args);

	wxStdDialogButtonSizer* buttonSizer = new wxStdDialogButtonSizer();
	buttonSizer->AddButton(new wxButton(m_elem, wxID_OK));
	buttonSizer->AddButton(new wxButton(m_elem, wxID_CANCEL));
	buttonSizer->Realize();

	wxSizer* topsizer = m_elem->GetSizer();
	topsizer->Add(buttonSizer, wxSizerFlags(0).Right().Border(wxBOTTOM | wxRIGHT, 5));
}
