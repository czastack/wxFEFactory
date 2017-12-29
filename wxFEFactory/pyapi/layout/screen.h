#pragma once
#include <wx/wx.h>
#include "layoutbase.h"

class Screen
{
public:
	static py::tuple getScreenSize()
	{
		auto size = py::tuple(2);
		int width, height;
		wxDisplaySize(&width, &height);
		size[0] = width;
		size[1] = height;
		return size;
	}
};