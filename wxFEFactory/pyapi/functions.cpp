#include <pybind11/eval.h>
#include <wx/wx.h>
#include <wx/clipbrd.h>
#include <wx/filedlg.h>
#include <wx/textctrl.h>
#include "pyutils.h"
#include "functions.h"
#include "fefactory_api.h"
#include "ui/console.h"
#include "ui/dialogs.h"

void log_message(wxcstr text)
{
	console.write(text);
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
	wxLongTextDialog dialog(title, defaultValue, readonly, sm);

	pyobj ret;

	if (dialog.ShowModal() == wxID_OK)
	{
		ret = py::cast(dialog.GetValue());
	}
	else
	{
		ret = None;
	}
	dialog.Destroy();
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

py::bytes mem_read(size_t address, size_t size)
{
	const char *p = (const char *)address;
	return py::bytes(p, size);
}

void mem_write(size_t address, py::bytes value, size_t size)
{
	Py_ssize_t ssize;
	char *p = NULL;
	PyBytes_AsStringAndSize(value.ptr(), &p, &ssize);
	if (size == 0 || (Py_ssize_t)size > ssize)
	{
		size = ssize;
	}

	if (p && size)
	{
		memcpy((void *)address, p, size);
	}
}

int get_bit()
{
	return (sizeof(size_t) == 8) ? 64: 32;
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

wxBitmap & castBitmap(pycref bitmap, wxBitmap & bp)
{
	if (py::isinstance<wxBitmap>(bitmap))
	{
		bp = bitmap.cast<wxBitmap>();
	}
	else if (PY_IS_TYPE(bitmap, PyUnicode))
	{
		wxcstr path = bitmap.cast<wxString>();
		wxBitmapType type = (wxBitmapType)getBitmapTypeByExt(path);
		if (type == wxBITMAP_TYPE_ICO)
		{
			bp.CopyFromIcon(wxIcon(path, wxBITMAP_TYPE_ICO));
		}
		else
		{
			bp.LoadFile(path, type);
		}
	}
	else
	{
		bp.Create({ 1, 1 });
	}
	return bp;
}


pyobj object_from_id(size_t id) {
	return py::reinterpret_borrow<py::object>((PyObject*)id);
}
