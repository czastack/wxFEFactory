#include <wx/wx.h>
#include <wx/bitmap.h>
#include <wx/icon.h>
#include "ui.h"


void UiModule::init_image()
{
	using namespace py::literals;

#define ENUM_VAL(name) value(#name, wx##name)
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

	auto type = "type"_a;
	auto type_v = type = wxBITMAP_TYPE_PNG;

	py::class_<wxBitmap>(ui, "Bitmap")
		.def(py::init<>())
		.def(py::init<wxcstr, long>(), "src"_a, type_v)
		.def("GetSize", &wxBitmap::GetSize)
		.def("CopyFromIcon", &wxBitmap::CopyFromIcon)
		.def("LoadFile", &wxBitmap::LoadFile, "path"_a, type_v)
		.def("SaveFile", &wxBitmap::SaveFile, "path"_a, type_v, "palette"_a = NULL);

	py::class_<wxIcon>(ui, "Icon")
		.def(py::init<>())
		.def(py::init<const wxString &, wxBitmapType, int, int>(),
			name, type = wxICON_DEFAULT_TYPE, "desiredWidth"_a = -1, "desiredHeight"_a = -1)
		;
}
