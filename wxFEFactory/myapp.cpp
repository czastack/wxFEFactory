#include <wx/wx.h>
#include <wx/imagpng.h>
#include "types.h"
#include "pyapi/fefactory_api.h"
#include "myapp.h"

const wxString wxNoneString = wxEmptyString;

IMPLEMENT_APP(MyApp)

bool MyApp::OnInit()
{
	if (!wxApp::OnInit())
		return false;

	wxImage::AddHandler(new wxPNGHandler);

	initPyEnv();

	return true;
}

int MyApp::OnExit()
{
	destroyPyEnv();
	return 0;
}
