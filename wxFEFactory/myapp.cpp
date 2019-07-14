#include <pybind11/embed.h>
#include <wx/imagpng.h>
#include "types.h"
#include "myapp.h"
#include "pyapi/pyapi.h"

const wxString wxNoneString = wxEmptyString;

IMPLEMENT_APP(MyApp)

bool MyApp::OnInit()
{
	if (!wxApp::OnInit())
		return false;

	wxImage::AddHandler(new wxPNGHandler);

	SetEnvironmentVariable(L"PYTHONPATH", L"python");
	m_guard = new pybind11::scoped_interpreter;
	initPyEnv();

	return true;
}

int MyApp::OnExit()
{
	destroyPyEnv();
	delete m_guard;
	return 0;
}
