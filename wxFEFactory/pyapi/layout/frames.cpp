#include <wx/wx.h>
#include "frames.h"


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
		py::print(hotkeyId, "��֧�ֵĸ�ʽ");
		return false;
	}
	return true;
}

void HotkeyWindow::RegisterHotKey(pyobj hotkeyId, int modifiers, int virtualKeyCode, pycref onhotkey)
{
	WORD _hotkeyId;
	const pyobj origin_hotkey_id = hotkeyId;

	if (prepareHotkey(hotkeyId, _hotkeyId))
	{
		if (m_hotkey_map.contains(hotkeyId))
		{
			py::print(origin_hotkey_id, "�Ѿ���ʹ����");
			return;
		}
		if (m_elem->RegisterHotKey(_hotkeyId, modifiers, virtualKeyCode))
		{
			m_hotkey_map[hotkeyId] = onhotkey;
			onhotkey.inc_ref();
		}
		else {
			py::print(origin_hotkey_id, "�ȼ�ע��ʧ��");
		}
	}
}

void HotkeyWindow::RegisterHotKeys(py::iterable &items)
{
	for (auto e : items)
	{
		const py::tuple &item = e.cast<py::tuple>();
		RegisterHotKey(item[0], item[1].cast<int>(), item[2].cast<int>(), item[3]);
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