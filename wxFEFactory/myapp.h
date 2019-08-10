#pragma once

#include <wx/wx.h>


class MyApp: public wxApp
{
public:
	bool OnInit() override;
	int OnExit() override;

	void SetRestartFlag(bool flag) { m_restart_flag = flag; }
	bool GetRestartFlag() { return m_restart_flag; }

private:
	bool m_restart_flag;
};

DECLARE_APP(MyApp)