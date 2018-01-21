#include <pybind11/eval.h>
#include <wx/wx.h>
#include <wx/clipbrd.h>
#include <wx/filedlg.h>
#include <wx/textctrl.h>
#include "pyutils.h"
#include "functions.h"
#include "fefactory_api.h"
#include "layout/console.h"
#include "layout/dialogs.h"

void log_message(wxcstr text)
{
	pyConsole.consoleWrite(text);
}


void alert(wxcstr title, wxcstr msg)
{
	wxMessageBox(msg, title);
}

int confirm_dialog(wxcstr title, wxcstr msg, int defaultButton)
{
	int style = wxYES_NO | wxCANCEL;

	if (defaultButton == wxNO)
		style |= wxNO_DEFAULT;
	else if (defaultButton == wxCANCEL)
		style |= wxCANCEL_DEFAULT;
	
	return wxMessageBox(msg, title, style, nullptr);
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

void exec_file(py::str file, pyobj scope)
{
	if (scope.is_none())
	{
		scope = py::module::import("__main__").attr("__dict__");
	}
	py::eval_file(file, scope);
}

wxItemKind getItemKind(wxcstr kindStr)
{
	wxItemKind kind = wxITEM_NORMAL;
	if (!kindStr.IsEmpty())
	{
		if (kindStr == wxT("check"))
		{
			kind = wxITEM_CHECK;
		}
		else if (kindStr == wxT("radio"))
		{
			kind = wxITEM_RADIO;
		}
		else if (kindStr == wxT("dropdown"))
		{
			kind = wxITEM_DROPDOWN;
		}
	}
	return kind;
}

long getBitmapTypeByExt(wxcstr path)
{
	long type = 0;
	if (path.EndsWith(".png"))
	{
		type = wxBITMAP_TYPE_PNG;
	}
	else if (path.EndsWith(".jpg") || path.EndsWith(".jpeg"))
	{
		type = wxBITMAP_TYPE_JPEG;
	}
	else if (path.EndsWith(".bmp"))
	{
		type = wxBITMAP_TYPE_BMP;
	}
	else if (path.EndsWith(".ico"))
	{
		type = wxBITMAP_TYPE_ICO;
	}
	else if (path.EndsWith(".gif"))
	{
		type = wxBITMAP_TYPE_GIF;
	}
	return type;
}
