#pragma once
#include <wx/dialog.h>


class SimpleDialog : public wxDialog
{
public:
	SimpleDialog(wxcstr title, bool readonly = false, bool sm = false, wxWindow *parent = nullptr);

	void setContentView(wxWindow* view, int spacing=4);

protected:
	class wxBoxSizer* m_rowsizer;
};


class wxLongTextDialog: public SimpleDialog
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