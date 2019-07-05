#include <pybind11/embed.h>
#include <wx/imagpng.h>
#include "types.h"
#include "myapp.h"
#include "pyapi/fefactory_api.h"

const wxString wxNoneString = wxEmptyString;

// IMPLEMENT_APP(MyApp)
extern "C" int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, wxCmdLineArgType, int nCmdShow)
{
	return wxEntry(hInstance, hPrevInstance, 0, nCmdShow);
}
MyApp& wxGetApp() { return *static_cast<MyApp*>(wxApp::GetInstance()); }
wxAppConsole* wxCreateApp()
{
	wxAppConsole::CheckBuildOptions(
		"3.1.2 (wchar_t,Visual C++ 1900,wx containers,compatible with 3.0)",
		"your program"
	);
	return new MyApp;
}
wxAppInitializer wxTheAppInitializer((wxAppInitializerFunction)wxCreateApp);

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
