#include <wx/arrstr.h>
#include <wx/colour.h>
#include "pyutils.h"
#include "pybindext.h"

const py::none None;

wxString& pystrcpy(wxString &text, const py::handle &h) {
	PyObject *temp = h.ptr();
	if (!PyUnicode_Check(temp)) {
		temp = py::str(temp).ptr();
	}
	Py_ssize_t length = PyUnicode_GetLength(temp);
	wxStringBufferLength buff(text, length);
	PyUnicode_AsWideChar(temp, buff, length);
	buff.SetLength(length);
	return text;
}

template<>
void wxArrayAddAll<wxArrayString>(wxArrayString& array, pycref items)
{
	wxString text;
	if (!items.is_none())
	{
		for (auto& item : items) {
			array.Add(pystrcpy(text, item));
		}
	}
}

py::object PyDictGet(pycref di, pycref key)
{
	if (!di.is_none())
	{
		PyObject* ret = PyDict_GetItem(di.ptr(), key.ptr());

		if (ret)
		{
			return py::reinterpret_borrow<py::object>(ret);
		}
	}
	return None;
}


void PyInterpreterRun(wxcstr line) {
	static PyObject *main = PyImport_AddModule("__main__");
	static PyObject *scope = PyModule_GetDict(main);

	PyObject *result = PyRun_String(line.mb_str(wxConvUTF8), Py_single_input, scope, scope);
	if (result == NULL)
	{
		PyErr_Print();
		return;
	}

	if (result != Py_None)
	{
		PyObject_Print(result, stdout, Py_PRINT_RAW);
	}

	Py_DECREF(result);


	/*
	PyObject *result = PyObject_Str(v);

	Py_ssize_t length = PyUnicode_GetLength(result);
	wxString resultText;
	wxStringBufferLength resultBuffer(resultText, length);
	PyUnicode_AsWideChar(result, resultBuffer, length);
	resultBuffer.SetLength(length);

	Py_DECREF(result);
	Py_DECREF(v);

	// resultText;
	*/
}

