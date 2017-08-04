#include <wx/wx.h>
#include "fe.h"
#include "../pyutils.h"
#include "../functions.h"
#include "feimg.hpp"


void init_fe(pybind11::module &m)
{
	using namespace py::literals;

	py::class_<FeImage>(m, "FeImage")
		.def(py::init<>())
		.def("create", &FeImage::create, "width"_a, "height"_a, "tileStride"_a, "tiles"_a, "pal"_a, "moveArgs"_a)
		.def("toTiles", &FeImage::toTiles, "width"_a, "height"_a, "tileStride"_a, "size"_a, "moveArgs"_a)
		.def("fillColor", &FeImage::fillColor, "rects"_a, "index"_a = 0)
		.def("rescale", &FeImage::rescale, "width"_a, "height"_a)
		.def("savePng", &FeImage::savePng, "path"_a)
		.def("view", &FeImage::view, "title"_a);
}