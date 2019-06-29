#pragma once
#include <wx/wx.h>

class Screen
{
public:
	static py::tuple get_screen_size();

	static py::tuple get_dpi();
};