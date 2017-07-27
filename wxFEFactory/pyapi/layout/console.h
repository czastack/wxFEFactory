#pragma once

class ConsoleHandler
{
public:
	ConsoleHandler();
	~ConsoleHandler();

	void setConsoleElem(wxTextCtrl* input, wxTextCtrl* output);

	void OnConsoleInput(wxCommandEvent &event) { consoleInput(event.GetString()); }
	void OnConsoleInputKey(class wxKeyEvent &event);
	void consoleInput(wxcstr line);
	void consoleWrite(wxcstr text);
	void consoleWriteln(wxcstr text);
	void setConsoleInput(wxcstr text = wxEmptyString);

	bool check()
	{
		return true;
	}
private:
	wxTextCtrl *m_input;
	wxTextCtrl *m_output;
	class wxLongTextDialog *m_dialog;
	class HistorySet *m_history;
};