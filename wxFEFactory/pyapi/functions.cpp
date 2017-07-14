#include <wx/wx.h>
#include <wx/clipbrd.h>
#include <wx/filedlg.h>
#include <wx/textctrl.h>
#include "pyutils.h"
#include "functions.h"
#include "fefactory_api.h"
#include "console.h"
#include "dialogs.h"

void log_message(wxcstr text)
{
	pyConsole.consoleWrite(text);
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

pyobj longtext_dialog(wxcstr title, wxcstr defaultValue, bool readonly, bool sm)
{
	// launch editor dialog
	wxLongTextDialog dlg(title, defaultValue, readonly, sm);

	pyobj ret;
	
	if (dlg.ShowModal() == wxID_OK)
	{
		ret = py::cast(dlg.GetValue());
	}
	else
	{
		ret = None;
	}
	dlg.Destroy();
	return ret;
}


/**
 * 选择文件
 */
wxString choose_file(wxcstr msg, pycref dir, pycref file, pycref wildcard, bool mustExist) {
	int flag = wxFD_OPEN;
	if (mustExist)
	{
		flag |= wxFD_FILE_MUST_EXIST;
	}
	wxFileDialog dialog(nullptr, msg, pywxstr(dir), pywxstr(file), pywxstr(wildcard, wxFileSelectorDefaultWildcardStr), flag);
	if (dialog.ShowModal() == wxID_CANCEL)
		return wxNoneString;

	return dialog.GetPath();
}


/**
 * 选择文件夹
 */
wxString choose_dir(wxcstr msg, pycref defaultPath, bool mustExist) {
	int flag = wxFD_OPEN;
	if (mustExist)
	{
		flag |= wxFD_FILE_MUST_EXIST;
	}
	wxDirDialog dialog(nullptr, msg, pywxstr(defaultPath), flag);
	if (dialog.ShowModal() == wxID_CANCEL)
		return wxNoneString;

	return dialog.GetPath();
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