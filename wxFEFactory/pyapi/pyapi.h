#pragma once

namespace pybind11 {
	class scoped_interpreter;
}

extern class ConsoleHandler console;
extern class pybind11::scoped_interpreter* g_interpreter;

void py_init();
void py_exit();
void py_reload();