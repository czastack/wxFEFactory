#include <wx/wx.h>
#include <wx/clipbrd.h>
#include <wx/filedlg.h>
#include "pyutils.h"
#include "functions.h"
#include "fefactory_api.h"
#include "console.h"


void log_message(wxcstr text)
{
	pyConsole.consoleWrite(text);
}


/**
* Ñ¡ÔñÎÄ¼þ
*/
wxString choose_file(wxcstr msg, pycref dir, pycref file, pycref wildcard) {
	wxFileDialog openFileDialog(nullptr, msg, pywxstr(dir), pywxstr(file),
		pywxstr(wildcard, wxFileSelectorDefaultWildcardStr), wxFD_OPEN | wxFD_FILE_MUST_EXIST);
	if (openFileDialog.ShowModal() == wxID_CANCEL)
		return wxNoneString;

	return openFileDialog.GetPath();
}



void alert(wxcstr title, wxcstr msg)
{
	wxMessageBox(msg, title);
}

int confirm_dialog(wxcstr title, wxcstr msg)
{
	return wxMessageBox(msg, title, wxYES_NO | wxCANCEL, nullptr);
}

pyobj input_dialog(wxcstr title, wxcstr msg, wxcstr defaultValue)
{
	wxTextEntryDialog dialog(nullptr, msg, title, defaultValue);
	pyobj ret;
	if (dialog.ShowModal() == wxID_OK)
	{
		ret = py::cast(dialog.GetValue());
	}
	else {
		ret = None;
	}
	dialog.Destroy();
	return ret;
}


wxString get_clipboard()
{
	// Read some text
	wxString result;
	if (wxTheClipboard->Open())
	{
		if (wxTheClipboard->IsSupported(wxDF_TEXT))
		{
			wxTextDataObject data;
			wxTheClipboard->GetData(data);
			result = data.GetText();
		}
		wxTheClipboard->Close();
	}
	return result;
}

void set_clipboard(wxcstr text)
{

	if (wxTheClipboard->Open())
	{
		// This data objects are held by the clipboard,
		// so do not delete them in the app.
		wxTheClipboard->SetData(new wxTextDataObject(text));
		wxTheClipboard->Close();
	}
}