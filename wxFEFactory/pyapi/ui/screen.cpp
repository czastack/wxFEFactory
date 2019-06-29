#include <windows.h>
#include "../pyutils.h"
#include "screen.h"

py::tuple Screen::get_screen_size()
{
	auto size = py::tuple(2);
	int width, height;
	wxDisplaySize(&width, &height);
	size[0] = width;
	size[1] = height;
	return size;
}

py::tuple Screen::get_dpi()
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
