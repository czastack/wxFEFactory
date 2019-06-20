#pragma once
#include <wx/dnd.h>
#include "../pyutils.h"

class FileDropListener : public wxFileDropTarget
{
public:
	FileDropListener(pycref ondrop): m_ondrop(ondrop) {}
	virtual bool OnDropFiles(wxCoord x, wxCoord y,
		const wxArrayString& filenames)
	{
		if (m_ondrop)
		{
			pycref ret = PyCall(m_ondrop, filenames);
			if (ret.ptr() == Py_False)
			{
				return false;
			}
		}

		return true;
	}
private:
	pyobj m_ondrop;
};


class TextDropListener : public wxTextDropTarget
{
public:
	TextDropListener(pycref ondrop) : m_ondrop(ondrop) {}
	virtual bool OnDropText(wxCoord x, wxCoord y, wxcstr text)
	{
		if (m_ondrop)
		{
			pycref ret = PyCall(m_ondrop, text);
			if (ret.ptr() == Py_False)
			{
				return false;
			}
		}

		return true;
	}
private:
	pyobj m_ondrop;
};