#pragma once

class wxComboBox;
class wxTextCtrl;

class ConsoleHandler
{
public:
	ConsoleHandler();
	~ConsoleHandler();
	void bindElem(wxComboBox* input, wxTextCtrl* output);
	void input(wxcstr line);
	void write(wxcstr text);
	void writeln(wxcstr text);
	void setInputValue (wxcstr text = wxEmptyString);
	auto getHistory() { return m_history; }
	void onInput(class wxCommandEvent &event) { input(event.GetString()); }
	void onInputKey(class wxKeyEvent &event);
	void onDropdown(class wxCommandEvent &event);
	void onInputPaste(class wxClipboardTextEvent &event);
private:
	wxComboBox *m_input;
	wxTextCtrl *m_output;
	class wxLongTextDialog *m_dialog;
	class HistorySet *m_history;
};