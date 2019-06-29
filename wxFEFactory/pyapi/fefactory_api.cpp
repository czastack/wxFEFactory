#include <pybind11/embed.h>
#include <wx/wx.h>
#include "pyutils.h"
#include "fefactory_api.h"
#include "wx/myapp.h"
#include "functions.h"
#include "ui/console.h"
#include "ui/ui.h"
#include "fe/fe.h"

#ifdef __WXMSW__
	#include "auto/auto.h"
	#include "emuhacker/emuhacker.h"
#endif

py::module fefactory;
ConsoleHandler console;
pyobj onAppExit;

void reloadFefactory()
{
	if (fefactory)
	{
		fefactory.reload();
	}
	else
	{
		try
		{
			fefactory = py::module::import("fefactory");
		}
		catch (py::error_already_set &e)
		{
			e.restore();
			PyErr_Print();
		}
	}
}

void set_on_exit(pycref fn)
{
	onAppExit = fn;
}


PYBIND11_EMBEDDED_MODULE(fefactory_api, m) {
	using namespace py::literals;
	m.def("log_message", log_message)
		.def("alert", alert, "title"_a, "msg"_a)
		.def("confirm", confirm_dialog, "title"_a, "msg"_a, "defaultButton"_a=wxOK)
		.def("input", input_dialog, "title"_a, "msg"_a, "defaultValue"_a=wxEmptyString)
		.def("longtext_dialog", longtext_dialog, "title"_a, "defaultValue"_a=wxEmptyString, "readonly"_a=false, "small"_a=false)
		.def("choose_file", choose_file, "msg"_a, "dir"_a=None, "file"_a=None, "wildcard"_a=None, "mustExist"_a=false)
		.def("choose_dir", choose_dir, "msg"_a, "defaultPath"_a=None, "mustExist"_a=false)
		.def("set_on_exit", set_on_exit)
		.def("exec_file", &exec_file)
		.def("get_clipboard", get_clipboard)
		.def("set_clipboard", set_clipboard)
		.def("mem_read", mem_read, "address"_a, "size"_a)
		.def("mem_write", mem_write, "address"_a, "value"_a, "size"_a)
		.def("get_bit", get_bit)
		.def("object_from_id", object_from_id)

		.def("GlobalAddAtom", GlobalAddAtom)
		.def("GlobalGetAtomName", GlobalGetAtomName)
		.def("GlobalDeleteAtom", GlobalDeleteAtom);

	UiModule ui(m);
	init_fe(m);
#ifdef _WIN32
	init_auto(m);
	init_emuhacker(m);
#endif
}

void initPyEnv()
{
	py::module::import("fefactory_api");
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
		PyCall(onAppExit);
	}
}