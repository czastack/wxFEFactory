#pragma once
#include <wx/arrstr.h>
#include <wx/textfile.h>
#include "types.h"

class HistorySet: public wxArrayString
{
public:
	HistorySet(int maxsize=-1): m_maxsize(maxsize)
	{

	}

	wxcstr prev() {
		if (size())
		{
			if (m_index == 0)
				m_index = size();

			m_index -= 1;
			return Item(m_index);
		}
		return wxNoneString;
	}

	wxcstr next() {
		if (size())
		{
			m_index += 1;

			if (m_index == size())
				m_index = 0;

			return Item(m_index);
		}
		return wxNoneString;
	}

	void Add(const wxString &text) {
		int i = Index(text);
		if (i != wxNOT_FOUND)
		{
			RemoveAt(i);
		}
		else if (m_maxsize != -1 && size() >= m_maxsize)
		{
			RemoveAt(0);
		}
		wxArrayString::Add(text);
		m_index = 0;
	}

	void clear()
	{
		m_index = 0;
		wxArrayString::clear();
	}

	void save(wxcstr fileName)
	{
		wxFile file(fileName, wxFile::write);
		wxString br("\n");
		for (wxcstr line: *this)
		{
			file.Write(line);
			file.Write(br);
		}
	}

	void load(wxcstr fileName)
	{
		wxTextFile file(fileName);
		if (file.Exists() && file.Open())
		{
			for (const wxString* line = &file.GetFirstLine(); ; line = &file.GetNextLine())
			{
				if (!line->IsEmpty())
					wxArrayString::Add(*line);

				if (file.Eof())
					break;
			}
		}
	}

private:
	int m_index = 0;
	int m_maxsize;
};