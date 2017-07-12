#pragma once

namespace pybind11 {
	class module;
}

void initPyEnv();
void destroyPyEnv();
void reloadFefactory();

void log_message(wxcstr text);
int confirm_dialog(wxcstr title, wxcstr msg);

class PageManager {
public:
	virtual bool OnClose() {
		m_closed = true;
		return true; 
	};

protected:
	bool m_closed = false;
};

extern pybind11::module fefactory;
extern class ConsoleHandler pyConsole;