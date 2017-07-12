#include <wx/arrstr.h>
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
	if (temp != h.ptr())
		Py_XDECREF(temp);
	return text;
}

void addAll(wxArrayString &array, py::iterable &items)
{
	wxString text;
	if (!items.is_none())
	{
		for (auto &item : items) {
			array.Add(pystrcpy(text, item));
		}
	}
}

py::object pyDictGet(pycref di, pycref key)
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


void py_interpreter_run(wxcstr line) {
	static PyObject *m = PyImport_AddModule("__main__");
	static PyObject *d = PyModule_GetDict(m);

	PyObject *v = PyRun_String(line.mb_str(wxConvUTF8), Py_single_input, d, d);
	if (v == NULL)
	{
		PyErr_Print();
		return;
	}

	if (v != Py_None)
		PyObject_Print(v, stdout, Py_PRINT_RAW);

	Py_DECREF(v);


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

