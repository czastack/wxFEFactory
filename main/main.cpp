#include "pch.h"

extern "C" int WINAPI wWinMain(
	_In_ HINSTANCE hInstance,
	_In_opt_ HINSTANCE hPrevInstance,
	_In_ LPTSTR lpCmdLine,
	_In_ int nShowCmd
)
{
	SetEnvironmentVariable(L"PYTHONPATH", L"python");
	Py_Initialize();

	PyObject * pModule = PyImport_ImportModule("main2");

	if (pModule == NULL) {
		if (PyErr_Occurred())
			PyErr_Print();
	}

	if (Py_FinalizeEx() < 0) {
		exit(120);
	}
}