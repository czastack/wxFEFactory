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

	py_init();
	return true;
}

int MyApp::OnExit()
{
	py_exit();
	if (m_restart_flag)
	{
		wxExecute(argv[0]);
	}
	return 0;
}
