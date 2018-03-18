#include "screen.h"
#include <windows.h>


py::tuple Screen::getScreenSize()
{
	auto size = py::tuple(2);
	int width, height;
	wxDisplaySize(&width, &height);
	size[0] = width;
	size[1] = height;
	return size;
}

py::tuple Screen::getDpi()
{
	auto size = py::tuple(2);
	// ªÒ»°DPI  
	HDC hdc = GetDC(NULL);
	if (hdc != NULL) {
		size[0] = GetDeviceCaps(hdc, LOGPIXELSX);
		size[1] = GetDeviceCaps(hdc, LOGPIXELSY);
		ReleaseDC(NULL, hdc);
	}
	return size;
}
