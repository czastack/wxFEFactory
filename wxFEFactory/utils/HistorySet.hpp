#pragma once
#include <wx/arrstr.h>
#include "types.h"

class HistorySet: public wxArrayString
{
public:
	HistorySet() = default;

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
		wxArrayString::Add(text);
		m_index = 0;
	}

private:
	int m_index = 0;
};