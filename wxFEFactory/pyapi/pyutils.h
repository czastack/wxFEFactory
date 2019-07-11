#pragma once
#undef _
#include <pybind11/pybind11.h>
#include <memory>
#include <wx/string.h>
#include "types.h"
#include "pybindext.h"

namespace py = pybind11;
using pyobj = py::object;
using pycref = const py::object &;

class wxString;
class wxArrayString;

extern const py::none None;


inline auto PyBytesGetBuff(const py::bytes &b)
{
	return PyBytes_AsString(b.ptr());
}

inline wxString pywxstr(const py::object & str, wxcstr def = wxNoneString)
{
	return str.is_none() ? def : str.cast<wxString>();
}

wxString& pystrcpy(wxString &text, const py::handle &h);

/**
 * Dict getitem
 */
py::object PyDictGet(pycref di, pycref key);

inline py::object PyDictGet(pycref di, wxcstr key) {
	return PyDictGet(di, py::str(key));
}

template<class T>
T PyDictGet(pycref di, pycref key, T defval)
{
	if (!di.is_none())
	{
		PyObject* ret = PyDict_GetItem(di.ptr(), key.ptr());

		if (ret)
		{
			return py::handle(ret).cast<T>();
		}
	}
	return defval;
}

template<class T>
T PyDictGet(pycref di, wxcstr key, T defval)
{
	return PyDictGet(di, py::str(key), defval);
}


template<class T>
void wxArrayAddAll(T &array, pycref items)
{
	if (!items.is_none())
	{
		for (auto &item : items) {
			array.Add(item.cast<T::value_type>());
		}
	}
}

template<>
void wxArrayAddAll<wxArrayString>(wxArrayString& array, pycref items);

template<class T> class wxSharedPtr;

template<class T>
wxSharedPtr<T> PyToArray(pycref list, int &n)
{
	n = py::len(list);
	T *data = new T[n];
	T *it = data;
	for (auto &e : list)
	{
		*it++ = e.cast<T>();
	}
	return wxSharedPtr<T>(data);
}

template<class T>
pyobj PyListFromArray(T &array)
{
	py::list list;
	for (const auto &i : array)
	{
		list.append(py::cast(i));
	}
	return list;
}

template <typename... Args>
py::object PyCall(const py::object & obj, Args &&...args) {
	try {
		return obj(std::forward<Args>(args)...);
	}
	catch (py::error_already_set &e)
	{
		e.restore();
		PyErr_Print();
		return None;
	}
}

template <class T>
inline py::handle getself(const T *ptr)
{
	return py::detail::get_object_handle(ptr, py::detail::get_type_info(typeid(T)));
}


/**
 * 在交互解释器中运行，保留结果
 */
void PyInterpreterRun(wxcstr line);


#define ATTR_INT(obj, name, pre) PyObject_SetAttrString(obj, #name, PyLong_FromLong(pre##name))


#define PyIterable_Check(obj) \
    ((obj)->ob_type->tp_iter != NULL && \
     (obj)->ob_type->tp_iter != &_PyObject_NextNotImplemented)

/**
 * 检查类型
 */
#define PY_IS_TYPE(obj, type) obj.ptr()->ob_type == &##type##_Type
#define GEN_TYPE_CHECK(type)\
	inline bool is##type(pycref obj)\
	{\
		return PY_IS_TYPE(obj, type);\
	}

GEN_TYPE_CHECK(PyDict)
GEN_TYPE_CHECK(PyList)
GEN_TYPE_CHECK(PyUnicode)
