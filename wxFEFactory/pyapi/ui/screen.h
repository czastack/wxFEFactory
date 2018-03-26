#pragma once
#include <wx/wx.h>
#include "uibase.h"

class Screen
{
public:
	static py::tuple getScreenSize();

	static py::tuple getDpi();
};