#pragma once

#include <pybind11/pybind11.h>
#include "utils/utils.h"

namespace pybind11 {
	
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

	
	template <typename type_, typename... options>
	class class_t : public class_<type_, options...>
	{
	public:
		template <typename... Extra>
		class_t(handle scope, const char *name, const Extra &... extra): class_(scope, name, extra...) {
			auto &internals = detail::get_internals();
			auto *tinfo = internals.registered_types_cpp[std::type_index(typeid(type_))];
			tinfo->init_instance = init_instance;
		}

		static void init_instance(detail::instance *inst, const void *holder_ptr) {
			auto v_h = inst->get_value_and_holder(detail::get_type_info(typeid(type)));
			if (!v_h.instance_registered()) {
				detail::register_instance(inst, v_h.value_ptr(), v_h.type);
				v_h.set_instance_registered();
			}
			class_::init_holder(inst, v_h, (const holder_type *)holder_ptr, v_h.value_ptr<type>());
			if (v_h.holder_constructed())
			{
				(v_h.value_ptr<type_>()->*(&type_::__init))();
			}
		}
	};
}