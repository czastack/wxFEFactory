#include <wx/wx.h>
#include "pyutils.h"
#include "fefactory_api.h"
#include "myapp.h"
#include "functions.h"
#include "layout/console.h"
#include "layout/layout.h"
#include "emuhacker/emuhacker.h"
#include "fe/fe.h"
#include "auto/auto.h"

py::module fefactory;
ConsoleHandler pyConsole;
pyobj onAppExit;

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

void setOnAppExit(pycref fn)
{
	onAppExit = fn;
}


PyObject *fefactory_api() {
	using namespace py::literals;

	py::module m("fefactory_api");

	m
		.def("log_message", log_message)
		.def("alert", alert, "title"_a, "msg"_a)
		.def("confirm", confirm_dialog, "title"_a, "msg"_a, "defaultButton"_a=wxOK)
		.def("input", input_dialog, "title"_a, "msg"_a, "defaultValue"_a = wxEmptyString)
		.def("longtext_dialog", longtext_dialog, "title"_a, "defaultValue"_a=wxEmptyString, "readonly"_a=false, "small"_a=false)
		.def("choose_file", choose_file, "msg"_a, "dir"_a=None, "file"_a=None, "wildcard"_a=None, "mustExist"_a=false)
		.def("choose_dir", choose_dir, "msg"_a, "defaultPath"_a=None, "mustExist"_a=false)
		.def("setOnAppExit", setOnAppExit)
		.def("exec_file", &exec_file)
		.def("get_clipboard", get_clipboard)
		.def("set_clipboard", set_clipboard);

	ATTR_INT(m.ptr(), YES, wx),
	ATTR_INT(m.ptr(), NO, wx),
	ATTR_INT(m.ptr(), CANCEL, wx);

	init_layout(m);
	init_emuhacker(m);
	init_fe(m);
	init_auto(m);
	return m.ptr();
}


void initPyEnv() {
	PyImport_AppendInittab("fefactory_api", &fefactory_api);
	SetEnvironmentVariable(L"PYTHONPATH", L"python");
	Py_Initialize();

	auto &app = wxGetApp();
	auto &args = app.argv.GetArguments();
	const wchar_t ** argv = new const wchar_t *[app.argc];
	for (int i = 0; i < app.argc; ++i)
	{
		argv[i] = args[i].wc_str();
	}
	PySys_SetArgv(app.argc, (wchar_t **)argv);
	delete[] argv;
	
	reloadFefactory();
}

void destroyPyEnv()
{
	if (onAppExit)
	{
		pyCall(onAppExit);
	}
	Py_Finalize();
}