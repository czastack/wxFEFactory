#pragma once
#undef _
#include <pybind11/pybind11.h>
#include <memory>
#include "types.h"
#include "pybindext.h"

namespace py = pybind11;
using pyobj = py::object;
using pycref = const py::object &;

class wxString;
class wxArrayString;

extern const py::none None;


inline wxString pywxstr(const py::object & str, wxcstr def = wxNoneString)
{
	return str.is_none() ? def : str.cast<wxString>();
}

inline auto bytesGetBuff(const py::bytes &b)
{
	return PyBytes_AsString(b.ptr());
}

wxString& pystrcpy(wxString &text, const py::handle &h);


void addAll(wxArrayString &array, py::iterable &items);

/**
 * Dict getitem
 */
py::object pyDictGet(pycref di, pycref key);

inline py::object pyDictGet(pycref di, wxcstr key) {
	return pyDictGet(di, py::str(key));
}

template<class T>
T pyDictGet(pycref di, pycref key, T defval)
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
T pyDictGet(pycref di, wxcstr key, T defval)
{
	return pyDictGet(di, py::str(key), defval);
}


template<class T>
void addAll(T &array, pycref items)
{
	if (!items.is_none())
	{
		for (auto &item : items) {
			array.Add(item.cast<T::value_type>());
		}
	}
}

template<class T> class wxSharedPtr;

template<class T>
wxSharedPtr<T> asArray(pycref list, int &n)
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
pyobj asPyList(T &array)
{
	py::list list;
	for (const auto &i : array)
	{
		list.append(i);
	}
	return list;
}

/**
 * 会返回options和values的值
 */
void prepareOptions(pyobj &options, pyobj &values, bool rangeIfNone = false);

template <typename... Args>
py::object pyCall(const py::object & obj, Args &&...args) {
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
inline py::handle getSelf(const T *ptr)
{
	return py::detail::get_object_handle(ptr, py::detail::get_type_info(typeid(T)));
}


/**
 * 在交互解释器中运行，保留结果
 */
void py_interpreter_run(wxcstr line);


#define ATTR_INT(obj, name, pre) PyObject_SetAttrString(obj, #name, PyLong_FromLong(pre##name))

/**
 * 检查类型
 */
#define GEN_TYPE_CHECK(type)\
	inline bool is##type(pycref obj)\
	{\
		return obj.ptr()->ob_type == &##type##_Type;\
	}

GEN_TYPE_CHECK(PyDict)
GEN_TYPE_CHECK(PyList)
GEN_TYPE_CHECK(PyUnicode)

/* 
PyFilter_Type
PyMap_Type
PyZip_Type
PyBool_Type
PyByteArray_Type
PyByteArrayIter_Type
PyBytes_Type
PyBytesIter_Type
PyCell_Type
PyMethod_Type
PyInstanceMethod_Type
PyCode_Type
PyComplex_Type
PyClassMethodDescr_Type
PyGetSetDescr_Type
PyMemberDescr_Type
PyMethodDescr_Type
PyWrapperDescr_Type
PyDictProxy_Type
_PyMethodWrapper_Type
PyProperty_Type
PyDict_Type
PyDictIterKey_Type
PyDictIterValue_Type
PyDictIterItem_Type
PyDictKeys_Type
PyDictItems_Type
PyDictValues_Type
PyEnum_Type
PyReversed_Type
PyStdPrinter_Type
PyFloat_Type
PyFrame_Type
PyFunction_Type
PyClassMethod_Type
PyStaticMethod_Type
PyGen_Type
PyCoro_Type
_PyCoroWrapper_Type
_PyAIterWrapper_Type
PyNullImporter_Type
PySeqIter_Type
PyCallIter_Type
PyCmpWrapper_Type
PyList_Type
PyListIter_Type
PyListRevIter_Type
PySortWrapper_Type
PyLong_Type
_PyManagedBuffer_Type
PyMemoryView_Type
PyCFunction_Type
PyModule_Type
PyModuleDef_Type
_PyNamespace_Type
PyType_Type
PyBaseObject_Type
PySuper_Type
_PyNone_Type
_PyNotImplemented_Type
PyODict_Type
PyODictIter_Type
PyODictKeys_Type
PyODictItems_Type
PyODictValues_Type
PyCapsule_Type
PyRange_Type
PyRangeIter_Type
PyLongRangeIter_Type
PySet_Type
PyFrozenSet_Type
PySetIter_Type
PySlice_Type
PyEllipsis_Type
PySTEntry_Type
PyTraceBack_Type
PyTuple_Type
PyTupleIter_Type
PyUnicode_Type
PyUnicodeIter_Type
_PyWeakref_RefType
_PyWeakref_ProxyType
_PyWeakref_CallableProxyType
 */