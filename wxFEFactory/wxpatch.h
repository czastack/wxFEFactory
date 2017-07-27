#pragma once
#include <wx/rearrangectrl.h>

class wxRearrangeListPatched: public wxRearrangeList
{
public:
	using wxRearrangeList::wxRearrangeList;

protected:
	int DoInsertItems(const wxArrayStringsAdapter & items, unsigned int pos, void **clientData, wxClientDataType type) wxOVERRIDE;
	int DoInsertOneItem(const wxString& item, unsigned int pos) wxOVERRIDE;
	void DoDeleteOneItem(unsigned int n) wxOVERRIDE;

	void DoClear() wxOVERRIDE;

	wxArrayInt& get_order()
	{
		return *const_cast<wxArrayInt*>(&GetCurrentOrder());
	}
};