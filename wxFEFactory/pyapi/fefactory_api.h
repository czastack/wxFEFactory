#pragma once

namespace pybind11 {
	class module;
}

extern pybind11::module fefactory;
extern class ConsoleHandler console;

void initPyEnv();
void destroyPyEnv();