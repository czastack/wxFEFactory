#include <wx/combobox.h>
#include <wx/textctrl.h>
#include <iostream>
#include <memory>
#include "../pyutils.h"
#include "../functions.h"
#include "console.h"
#include "dialogs.h"
#include "utils/HistorySet.hpp"
using namespace std;

constexpr auto PS1 = _T(">>> "), PS2 = _T("... "), HISTORY_FILE = _T("python_history.txt");
constexpr int HISTORY_SIZE = 10;

ConsoleHandler::ConsoleHandler() : m_history(new HistorySet(HISTORY_SIZE)), m_input(nullptr), m_output(nullptr)
{
	m_history->load(HISTORY_FILE);
}

ConsoleHandler::~ConsoleHandler() {
	m_history->save(HISTORY_FILE);

	delete m_history;
}

void ConsoleHandler::bindElem(wxComboBox* input, wxTextCtrl* output)
{
	m_input = input;
	m_output = output;

	input->Bind(wxEVT_TEXT_ENTER, &ConsoleHandler::onInput, this);
	input->Bind(wxEVT_CHAR, &ConsoleHandler::onInputKey, this);
	input->Bind(wxEVT_TEXT_PASTE, &ConsoleHandler::onInputPaste, this);
	input->Bind(wxEVT_COMBOBOX_DROPDOWN, &ConsoleHandler::onDropdown, this);

	std::cout.rdbuf(output);
	std::cerr.rdbuf(output);
}

void ConsoleHandler::onInputKey(wxKeyEvent & event)
{
	int code = event.GetKeyCode();
	if (code == WXK_TAB)
		m_input->AppendText(_T("    "));
	else if (code == WXK_UP)
		setInputValue(m_history->prev());
	else if (code == WXK_DOWN)
		setInputValue(m_history->next());
	else if (code == WXK_CONTROL_L && event.m_shiftDown)
	{
		m_output->Clear();
		m_history->clear();
	}
	else if (code == WXK_CONTROL_L)
		m_output->Clear();
	else
		event.Skip();
}

void ConsoleHandler::onDropdown(wxCommandEvent & event)
{
	m_input->Clear();
	m_input->Insert(*m_history, 0);
}

void ConsoleHandler::onInputPaste(wxClipboardTextEvent & event)
{
	wxcstr text = get_clipboard();
	if (text.Contains('\n'))
	{
		int start = 0;
		int i = 0;
		wxString line;
		for(;;)
		{
			i = text.find('\n', i);
			if (i == wxNOT_FOUND)
			{
				i = text.size();
			}
			line = text.SubString(start, i - 1);

			if (i < text.size())
			{
				input(line);
			}
			else
			{
				break;
			}
			++i;
			start = i;
		}
		setInputValue(line);
	}
	else
	{
		event.Skip();
	}
}

void ConsoleHandler::write(wxcstr text)
{
	if (m_output)
	{
		m_output->AppendText(text);
	}
	else
	{
		if (!m_dialog)
		{
			m_dialog = new wxLongTextDialog("控制台未初始化");
			m_dialog->Bind(wxEVT_BUTTON, [this](auto) {
				m_dialog->Destroy();
				exit(1);
			});
			m_dialog->Show();
		}
		m_dialog->getEditor()->AppendText(text);
	}
}

void ConsoleHandler::writeln(wxcstr text)
{
	write(text + _T('\n'));
}

void ConsoleHandler::setInputValue(wxcstr text)
{
	int n = text.Length();
	if (n)
	{
		m_input->SetValue(text);
		m_input->SetSelection(n, n);
	}
}

void ConsoleHandler::input(wxcstr line)
{
	write(PS1);
	writeln(line);
	if (!line.IsEmpty())
	{
		m_history->Add(line);
		m_input->Clear();

		PyInterpreterRun(line);
	}
}