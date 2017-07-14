#pragma once
#include <wx/dialog.h>

class wxLongTextDialog: public wxDialog
{
public:
	wxLongTextDialog(wxcstr title, wxcstr defaultValue=wxNoneString, bool readonly=false, bool sm=false, wxWindow *parent=nullptr);

	wxString GetValue()
	{
		return m_ed->GetValue();
	}

	wxTextCtrl *getEditor()
	{
		return m_ed;
	}

private:
	class wxTextCtrl *m_ed;
};