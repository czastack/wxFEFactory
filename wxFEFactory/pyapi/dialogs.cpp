#include <wx/sizer.h>
#include <wx/textctrl.h>
#include <wx/button.h>
#include "types.h"
#include "dialogs.h"

wxLongTextDialog::wxLongTextDialog(wxcstr title, wxcstr defaultValue, bool readonly, bool sm, wxWindow *parent)
	:wxDialog(parent, wxID_ANY, title, wxDefaultPosition, wxDefaultSize,
		wxDEFAULT_DIALOG_STYLE | wxRESIZE_BORDER | wxCLIP_CHILDREN)
{
	// Multi-line text editor dialog.
	const int spacing = sm ? 4 : 8;
	wxBoxSizer* topsizer = new wxBoxSizer(wxVERTICAL);
	wxBoxSizer* rowsizer = new wxBoxSizer(wxHORIZONTAL);
	long edStyle = wxTE_MULTILINE;
	if (readonly)
		edStyle |= wxTE_READONLY;

	m_ed = new wxTextCtrl(this, wxID_ANY, defaultValue,
		wxDefaultPosition, wxDefaultSize, edStyle);

	rowsizer->Add(m_ed, wxSizerFlags(1).Expand().Border(wxALL, spacing));
	topsizer->Add(rowsizer, wxSizerFlags(1).Expand());

	wxStdDialogButtonSizer* buttonSizer = new wxStdDialogButtonSizer();
	if (!readonly)
		buttonSizer->AddButton(new wxButton(this, wxID_OK));
	buttonSizer->AddButton(new wxButton(this, wxID_CANCEL));
	buttonSizer->Realize();
	topsizer->Add(buttonSizer, wxSizerFlags(0).Right().Border(wxBOTTOM | wxRIGHT, spacing));

	SetSizer(topsizer);
	topsizer->SetSizeHints(this);

	if (sm)
	{
		SetSize(400, 300);
	}
}
