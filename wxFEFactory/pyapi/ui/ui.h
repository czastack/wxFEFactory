#pragma once

namespace pybind11 {
	class module;
}


void init_aui(py::module &m);
void init_bars(py::module &m);
void init_bitmap(py::module &m);
void init_containers(py::module &m);
void init_controls(py::module &m);
void init_datacontrols(py::module &m);
void init_frames(py::module &m);
void init_menu(py::module &m);
void init_events(py::module &m);
void init_ui(pybind11::module &m);