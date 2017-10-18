#include <wx/wx.h>
#include <wx/icon.h>
#include "bitmap.h"

void init_bitmap(py::module & m)
{
	using namespace py::literals;

	auto bptype = "type"_a = (long)wxBITMAP_TYPE_PNG;

	auto Bitmap = py::class_<wxBitmap, PyBitmap>(m, "Bitmap")
		.def(py::init<>())
		.def(py::init<wxcstr, long>(), "name"_a, bptype)
		.def("save", &wxBitmap::SaveFile, "path"_a, bptype, "palette"_a=NULL)
		.def("load", &wxBitmap::LoadFile, "path"_a, bptype)
		.def("loadIcon", &PyBitmap::LoadIcon)
		.def_property("size", &PyBitmap::getSize, &PyBitmap::setSize)
		.ptr();
	
	ATTR_INT(Bitmap, TYPE_BMP, wxBITMAP_),
	ATTR_INT(Bitmap, TYPE_ICON, wxBITMAP_),
	ATTR_INT(Bitmap, TYPE_PNG, wxBITMAP_),
	ATTR_INT(Bitmap, TYPE_JPEG, wxBITMAP_);
}
