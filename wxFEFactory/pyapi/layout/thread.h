#pragma once
#include <wx/thread.h>
#include "layoutbase.h"


class PyThread : public wxThread
{
private:
	pycref m_fn;
	DWORD m_delay;
public:
	PyThread(pycref fn, DWORD delay): m_fn(fn), m_delay(delay)
	{

	}
	virtual void* Entry()
	{
		if (m_delay)
		{
			wxMilliSleep(m_delay);
		}
		pyCall(m_fn);
	}
};