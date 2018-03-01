#include <wx/wx.h>
#include <wx/icon.h>
#include "bitmap.h"


void wxBitmap__setSize(wxBitmap &self, py::tuple &size)
{
	self.SetSize({ size[0].cast<int>(), size[1].cast<int>() });
}

pyobj wxBitmap__getSize(wxBitmap &self)
{
	py::tuple ret = py::tuple(2);
	const wxSize &sz = self.GetSize();
	ret[0] = sz.GetWidth();
	ret[1] = sz.GetHeight();
	return ret;
}

auto wxBitmap__LoadIcon(wxBitmap &self, wxcstr path)
{
	self.CopyFromIcon(wxIcon(path, wxBITMAP_TYPE_ICO));
	return &self;
}

void init_bitmap(py::module & m)
{
	using namespace py::literals;

	auto bptype = "type"_a = (long)wxBITMAP_TYPE_PNG;

	auto Bitmap = py::class_<wxBitmap>(m, "Bitmap")
		.def(py::init<>())
		.def(py::init<wxcstr, long>(), "name"_a, bptype)
		.def("save", &wxBitmap::SaveFile, "path"_a, bptype, "palette"_a=NULL)
		.def("load", &wxBitmap::LoadFile, "path"_a, bptype)
		.def("loadIcon", wxBitmap__LoadIcon)
		.def_property("size", wxBitmap__getSize, wxBitmap__setSize)
		.ptr();
	
	ATTR_INT(Bitmap, TYPE_BMP, wxBITMAP_),
	ATTR_INT(Bitmap, TYPE_ICON, wxBITMAP_),
	ATTR_INT(Bitmap, TYPE_PNG, wxBITMAP_),
	ATTR_INT(Bitmap, TYPE_JPEG, wxBITMAP_);
}
