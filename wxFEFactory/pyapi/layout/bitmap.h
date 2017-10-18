#pragma once
#include "layoutbase.h"
#include <wx/bitmap.h>


class PyBitmap : public wxBitmap
{
public:
	using wxBitmap::wxBitmap;

	void setSize(py::tuple &size)
	{
		SetSize({ size[0].cast<int>(), size[1].cast<int>() });
	}

	pyobj getSize()
	{
		py::tuple ret = py::tuple(2);
		const wxSize &sz = GetSize();
		ret[0] = sz.GetWidth();
		ret[1] = sz.GetHeight();
		return ret;
	}

	auto LoadIcon(wxcstr path)
	{
		CopyFromIcon(wxIcon(path, wxBITMAP_TYPE_ICO));
		return this;
	}
};


void init_bitmap(py::module &m);