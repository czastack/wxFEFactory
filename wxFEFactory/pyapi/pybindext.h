#pragma once

#include <pybind11/pybind11.h>
#include "utils/utils.h"

namespace pybind11 {
	namespace detail {

#if wxUSE_UNICODE_WCHAR && wxUSE_STL_BASED_WXSTRING
		template <> class type_caster<wxString> {
		public:
			PYBIND11_TYPE_CASTER(wxString, (_)(PYBIND11_STRING_NAME));

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

				// buffer = PyUnicode_AsWideCharString(load_src.ptr(), &length);
				Py_ssize_t length = PyUnicode_GetLength(load_src.ptr());
				wxStringBufferLength buff(value, length);
				PyUnicode_AsWideChar(load_src.ptr(), buff, length);
				buff.SetLength(length);

				success = true;
				return true;
			}

			static handle cast(const wxString& src, return_value_policy /* policy */, handle /* parent */) {
				return PyUnicode_FromWideChar(src.wc_str(), (ssize_t)src.length());
			}
		protected:
			bool success = false;
		};
#endif


		template<typename T>
		struct IsArray {
			template <typename C> static typename C::wxBaseArray test(int);
			template <typename C> static std::false_type test(...);
			static constexpr bool value = !std::is_same<decltype(test<T>(0)), std::false_type>::value;
		};

		template <typename ArrayType> class type_caster<ArrayType, std::enable_if_t<IsArray<ArrayType>::value>> {
		public:
			PYBIND11_TYPE_CASTER(ArrayType, (_)("wxArray"));

			bool load(handle src, bool) {
				wxArrayAddAll(value, py::reinterpret_borrow<py::object>(src));
				return true;
			}

			static handle cast(const ArrayType& src, return_value_policy, handle) {
				return PyListFromArray(src).release();
			}
		protected:
			bool success = false;
		};


		HAS_MEM_FUNC(Add, HasAdd);

		template <typename ArrayType> class type_caster<ArrayType, std::enable_if_t<HasAdd<ArrayType>::value>> {
		public:
			PYBIND11_TYPE_CASTER(ArrayType, (_)("wxArrayLike"));

			bool load(handle src, bool) {
				wxArrayAddAll(value, py::reinterpret_borrow<py::object>(src));
				return true;
			}

			static handle cast(const ArrayType& src, return_value_policy, handle) {
				return PyListFromArray(src).release();
			}
		protected:
			bool success = false;
		};
	}
}