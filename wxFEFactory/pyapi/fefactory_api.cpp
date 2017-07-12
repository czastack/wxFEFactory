
#include <wx/filedlg.h>
#include "pyutils.h"
#include "fefactory_api.h"
#include "myapp.h"
#include "functions.h"
#include "layout.hpp"
#include "feimg.hpp"
#include "console.h"

py::module fefactory;
ConsoleHandler pyConsole;

// #define BINDFN(fn) .def(#fn, &PyVbaHandler::fn)

#pragma region module function

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

int confirm_dialog(wxcstr title, wxcstr msg)
{
	return wxMessageBox(msg, title,
		wxYES_NO | wxCANCEL, nullptr);
}

#pragma endregion


void reloadFefactory()
{
	if (fefactory)
	{
		if (!PyImport_ReloadModule(fefactory.ptr()))
			PyErr_Print();
	} 
	else
	{
		PyObject *module = PyImport_ImportModule("fefactory");
		if (module) {
			fefactory = py::reinterpret_borrow<py::module>(module);
		}
		else
			PyErr_Print();
		/*try
		{
			fefactory = py::module::import("fefactory");
		}
		catch (py::error_already_set &e)
		{
			e.restore();
			PyErr_Print();
		}*/
	}
}


void setConsoleElem(TextInput &input, TextInput &output)
{
	pyConsole.setConsoleElem((wxTextCtrl*)input.ptr(), (wxTextCtrl*)output.ptr());
}


PyObject *fefactory_api() {
	using namespace py::literals;

	py::module m("fefactory_api");

	m
		.def("log_message", log_message)
		.def("choose_file", choose_file, "msg"_a, "dir"_a = None, "file"_a = None, "wildcard"_a = None)
		.def("confirm_dialog", confirm_dialog)
		.def("setConsoleElem", setConsoleElem, "input"_a, "output"_a);

	py::class_<FeImage>(m, "FeImage")
		.def(py::init<>())
		.def("create", &FeImage::create, "width"_a, "height"_a, "tileStride"_a, "tiles"_a, "pal"_a, "moveArgs"_a)
		.def("toTiles", &FeImage::toTiles, "width"_a, "height"_a, "tileStride"_a, "size"_a, "moveArgs"_a)
		.def("fillColor", &FeImage::fillColor, "rects"_a, "index"_a = 0)
		.def("rescale", &FeImage::rescale, "width"_a, "height"_a)
		.def("savePng", &FeImage::savePng, "path"_a)
		.def("view", &FeImage::view, "title"_a);

	initLayout(m);
	return m.ptr();
}

void initPyEnv() {
	PyImport_AppendInittab("fefactory_api", &fefactory_api);
	SetEnvironmentVariable(L"PYTHONPATH", L"python");
	Py_Initialize();
	reloadFefactory();
}

void destroyPyEnv()
{
	Py_Finalize();
}

