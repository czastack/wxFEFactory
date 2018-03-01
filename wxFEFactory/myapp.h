#pragma once

#include <wx/wx.h>

namespace pybind11 {
	class scoped_interpreter;
};

class MyApp: public wxApp
{
public:
	bool OnInit() override;
	int OnExit() override;

private:
	pybind11::scoped_interpreter *m_guard;
};

DECLARE_APP(MyApp)