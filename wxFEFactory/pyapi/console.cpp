#include "utils/HistorySet.hpp"
#include <wx/textctrl.h>
#include "pyutils.h"
#include "console.h"
#include "functions.h"
#include "dialogs.h"
#include <iostream>
#include <memory>
using  namespace std;

constexpr auto PS1 = _T(">>> "), PS2 = _T("... "), HISTORY_FILE = _T("python_history.txt");
constexpr int HISTORY_SIZE = 10;

ConsoleHandler::ConsoleHandler() : m_history(new HistorySet(HISTORY_SIZE)), m_input(nullptr), m_output(nullptr)
{
	m_history->load(HISTORY_FILE);
}

ConsoleHandler::~ConsoleHandler() {
	m_history->save(HISTORY_FILE);

	delete m_history;

	if (m_dialog)
	{
		m_dialog->Destroy();
		delete m_dialog;
	}
}

void ConsoleHandler::setConsoleElem(wxTextCtrl* input, wxTextCtrl* output)
{
	m_input = input;
	m_output = output;

	input->Bind(wxEVT_TEXT_ENTER, &ConsoleHandler::OnConsoleInput, this);
	input->Bind(wxEVT_CHAR, &ConsoleHandler::OnConsoleInputKey, this);


	std::cout.rdbuf(output);
	std::cerr.rdbuf(output);
}

void ConsoleHandler::OnConsoleInputKey(wxKeyEvent & event)
{
	int code = event.GetKeyCode();
	if (code == WXK_TAB)
		m_input->AppendText(_T("    "));
	else if (code == WXK_UP)
		setConsoleInput(m_history->prev());
	else if (code == WXK_DOWN)
		setConsoleInput(m_history->next());
	else if (code == WXK_CONTROL_L && event.m_controlDown)
		m_output->Clear();
	else
		event.Skip();
}

void ConsoleHandler::consoleWrite(wxcstr text)
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

void ConsoleHandler::consoleWriteln(wxcstr text)
{
	consoleWrite(text + _T('\n'));
}

void ConsoleHandler::setConsoleInput(wxcstr text)
{
	int n = text.Length();
	if (n)
	{
		m_input->SetValue(text);
		m_input->SetSelection(n, n);
	}
}

void ConsoleHandler::consoleInput(wxcstr line)
{
	consoleWrite(PS1);
	consoleWriteln(line);
	if (!line.IsEmpty())
	{
		m_history->Add(line);
		m_input->Clear();

		py_interpreter_run(line);
	}
}