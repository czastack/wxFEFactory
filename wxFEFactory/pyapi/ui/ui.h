#pragma once
#include "../pyutils.h"

namespace pybind11 {
	class module;
}


class PyFunctor
{
public:
	PyFunctor(pycref fn=None) : fn(fn) {};

	void operator()(wxEvent& event) {
		PyCall(fn, event);
	}

	pyobj fn;
};


namespace pybind11 {
	namespace detail {

		// wxSize
		/*template <> class type_caster<wxSize> {
		public:
			bool load(handle src, bool) {
				auto temp = py::reinterpret_borrow<sequence>(src);
				value.x = temp[0].cast<int>();
				value.y = temp[1].cast<int>();
				return true;
			}

			static handle cast(const wxSize& src, return_value_policy, handle) {
				py::tuple result(2);
				result[0] = src.x;
				result[0] = src.y;
				return result;
			}

			PYBIND11_TYPE_CASTER(wxSize, (_)("wxSize"));
		protected:
			bool success = false;
		};*/

		// PyFunctor
		template <> struct type_caster<PyFunctor> {
		public:
			PYBIND11_TYPE_CASTER(PyFunctor, _("PyFunctor"));

			bool load(handle src, bool) {
				value.fn = reinterpret_steal<object>(src);
				return true;
			}

			static handle cast(const PyFunctor& src, return_value_policy, handle) {
				return src.fn;
			}
		};

		// wxColor
		template <> struct type_caster<wxColour> {
		public:
			PYBIND11_TYPE_CASTER(wxColour, (_)("wxColor"));

			bool load(handle src, bool) {
				value.SetRGB((wxUint32)src.cast<pybind11::int_>());
				return true;
			}

			static handle cast(const wxColour& src, return_value_policy, handle) {
				return PyLong_FromUnsignedLong(src.GetRGB());
			}
		};

#define ENUM_CASTER(type)\
		template <> struct type_caster<type> {\
		public:\
			PYBIND11_TYPE_CASTER(type, (_)(#type));\
			bool load(handle src, bool) {\
				value = (type)src.cast<long>();\
				return true;\
			}\
			static handle cast(const type& src, return_value_policy, handle) {\
				return PyLong_FromUnsignedLong(src);\
			}\
		}

		ENUM_CASTER(wxKeyCode);
	}
}


#define PACK(...) __VA_ARGS__


class UiModule
{
public:
	UiModule(pybind11::module &parent);

	void init_ui();
	void init_aui();
	void init_image();
	void init_containers();
	void init_controls();
	void init_datacontrols();
	void init_frames();
	void init_menu();
	void init_events();

	/**
	 * ѡ��ת��
	 */
	static wxArrayString get_choices(pycref choices);

	static void start_cache()
	{
		m_choices_cache_on = true;
	}

	static void end_cache()
	{
		m_choices_cache_on = false;
		m_choices_cache.clear();
	}
protected:
	static std::unordered_map<PyObject*, wxArrayString> m_choices_cache;
	static bool m_choices_cache_on;

private:
	pybind11::module module;
	pybind11::module ui;
	pybind11::arg parent, id, style, label, pos, size, validator, name,
		event, value, text, title, show, item, items, choices, window,
		colour, data;
	pybind11::arg_v late_v, id_v, label_v, pos_v, size_v, style_0, validator_v, name_v;
};
