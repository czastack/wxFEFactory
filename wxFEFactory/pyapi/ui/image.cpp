#include <wx/wx.h>
#include <wx/bitmap.h>
#include <wx/icon.h>
#include "ui.h"


void UiModule::init_image()
{
	using namespace py::literals;

	py::enum_<wxBitmapType>(ui, "BitmapType")
		.ENUM_VAL(BITMAP_TYPE_BMP)
		.ENUM_VAL(BITMAP_TYPE_ICO)
		.ENUM_VAL(BITMAP_TYPE_ICO_RESOURCE)
		.ENUM_VAL(BITMAP_TYPE_CUR)
		.ENUM_VAL(BITMAP_TYPE_TIFF)
		.ENUM_VAL(BITMAP_TYPE_GIF)
		.ENUM_VAL(BITMAP_TYPE_PNG)
		.ENUM_VAL(BITMAP_TYPE_JPEG)
		.ENUM_VAL(BITMAP_TYPE_PNM)
		.ENUM_VAL(BITMAP_TYPE_PCX)
		.ENUM_VAL(BITMAP_TYPE_PICT)
		.ENUM_VAL(BITMAP_TYPE_ICON)
		.ENUM_VAL(BITMAP_TYPE_ANI)
		.ENUM_VAL(BITMAP_TYPE_IFF)
		.ENUM_VAL(BITMAP_TYPE_TGA)
		.ENUM_VAL(BITMAP_TYPE_MACCURSOR)

		.ENUM_VAL(BITMAP_TYPE_MAX)
		.ENUM_VAL(BITMAP_TYPE_ANY)
		.export_values();

	py::enum_<wxBitmapTransparency>(ui, "BitmapTransparency")
		.ENUM_VAL(BitmapTransparency_Auto)
		.ENUM_VAL(BitmapTransparency_None)
		.ENUM_VAL(BitmapTransparency_Always)
		.export_values();

	py::arg type("type");
	py::arg_v bp_type_v(type, wxBITMAP_TYPE_PNG),
		ico_type_v(type, wxICON_DEFAULT_TYPE),
		desiredWidth("desiredWidth", -1),
		desiredHeight("desiredHeight", -1);

	py::class_<wxBitmap>(ui, "Bitmap")
		.def(py::init<>())
		.def(py::init<wxcstr, long>(), "src"_a, bp_type_v)
		.def("GetSize", &wxBitmap::GetSize)
		.def("CopyFromIcon", &wxBitmap::CopyFromIcon, "icon"_a, "transp"_a=wxBitmapTransparency_Auto)
		.def("LoadFile", &wxBitmap::LoadFile, "path"_a, bp_type_v)
		.def("SaveFile", &wxBitmap::SaveFile, "path"_a, bp_type_v, "palette"_a = NULL);

	py::class_<wxIcon>(ui, "Icon")
		.def(py::init<>())
		.def(py::init<const wxString &, wxBitmapType, int, int>(),
			name, ico_type_v, desiredWidth, desiredHeight)
		.def("LoadFile", &wxIcon::LoadFile, "path"_a, ico_type_v, desiredWidth, desiredHeight)
		;
}
