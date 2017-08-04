#pragma once

#include <pybind11/pybind11.h>
#include "utils/utils.h"

namespace pybind11 {
	/*class wstr : public str {
	public:
		using str::str;

		wstr() : str(){}

		wstr(const wchar_t *c, ssize_t n)
			: str(PyUnicode_FromWideChar(c, n), stolen) {
			if (!m_ptr) pybind11_fail("Could not allocate string object!");
		}

		wstr(const std::wstring &s) : wstr(s.data(), s.size()) { }

		operator std::wstring() const {
			object temp;
			if (!PyUnicode_Check(ptr())) {
				temp = reinterpret_steal<object>(PyUnicode_FromObject(ptr()));
			}
			else {
				temp = *this;
			}
			ssize_t length = -1;
			wchar_t *buffer = PyUnicode_AsWideCharString(temp.ptr(), &length);
			std::wstring value = std::wstring(buffer, length);
			PyMem_Free(buffer);
			return value;
		}

		operator class wxString() const {
			return operator wxStringImpl();
		}
	};
*/
	
	namespace detail {
#if wxUSE_UNICODE_WCHAR && wxUSE_STL_BASED_WXSTRING
		template <> class type_caster<wxString> {
		public:
			bool load(handle src, bool) {
				object temp;
				handle load_src = src;
				if (!src) {
					return false;
				}
				else if (!PyUnicode_Check(load_src.ptr())) {
					temp = reinterpret_steal<object>(PyUnicode_FromObject(load_src.ptr()));
					if (!temp) { PyErr_Clear(); return false; }
					load_src = temp;
				}
#if PY_MAJOR_VERSION >= 3
				// buffer = PyUnicode_AsWideCharString(load_src.ptr(), &length);
				Py_ssize_t length = PyUnicode_GetLength(load_src.ptr());
				wxStringBufferLength buff(value, length);
				PyUnicode_AsWideChar(load_src.ptr(), buff, length);
				buff.SetLength(length);
#else
				wchar_t *buffer = nullptr;
				temp = reinterpret_steal<object>(PyUnicode_AsEncodedString(
					load_src.ptr(), sizeof(wchar_t) == sizeof(short)
					? "utf16" : "utf32", nullptr));

				if (temp) {
					int err = PYBIND11_BYTES_AS_STRING_AND_SIZE(temp.ptr(), (char **)&buffer, &length);
					if (err == -1) { buffer = nullptr; }  // TypeError
					length = length / (ssize_t) sizeof(wchar_t) - 1; ++buffer; // Skip BOM
				}
				if (!buffer) { PyErr_Clear(); return false; }
				value.append(buffer, buffer + length);
#endif
				success = true;
				return true;
			}

			static handle cast(const wxString &src, return_value_policy /* policy */, handle /* parent */) {
				return PyUnicode_FromWideChar(src.wc_str(), (ssize_t)src.length());
			}

			PYBIND11_TYPE_CASTER(wxString, (_)(PYBIND11_STRING_NAME));
		protected:
			bool success = false;
		};
#endif

		HAS_MEM_FUNC(Add, hasAdd);

		template <typename ArrayType> class type_caster<ArrayType, std::enable_if_t<hasAdd<ArrayType>::value>> {
		public:
			bool load(handle src, bool) {
				addAll(value, py::reinterpret_borrow<py::object>(src));
				return true;
			}

			static handle cast(const ArrayType &src, return_value_policy /* policy */, handle /* parent */) {
				return asPyList(src).inc_ref();
			}

			PYBIND11_TYPE_CASTER(ArrayType, (_)("wxArray"));
		protected:
			bool success = false;
		};
	}



	/*template <typename... options>
	class class_cza : public class_<options...>
	{
	public:
		using class_::class_;
		using init_t = void (type::*)();

		template <typename... Args, typename... Extra>
		class_ &def_init(init_t initfn, const detail::init<Args...> &init, const Extra&... extra)
		{
			def("__init__", [initfn](type *self_, Args... args) { (new (self_) type(args...)->*initfn)(); }, extra...);
			return *this;
		}
	};*/

	
	template <typename... options>
	class class_t : public class_<options...>
	{
	public:
		using class_::class_;
		using init_t = void (type::*)();

		template <typename... Args, typename... Extra>
		auto &def_init(const detail::init<Args...> &init, const Extra&... extra)
		{
			def("__init__", [](type *self_, Args... args) { (new (self_) type(args...)->*(&type::__init))(); }, extra...);
			return *this;
		}

/*
		auto &def_alias(const char *alias, const char *origin)
		{
			py::setattr(*this, alias, this->attr(origin));
			return *this;
		}*/
	};
}