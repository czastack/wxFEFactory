#include "wxpatch.h"

int wxRearrangeListPatched::DoInsertItems(const wxArrayStringsAdapter &items, unsigned int pos, void **clientData, wxClientDataType type)
{
	int ret = wxCheckListBox::DoInsertItems(items, pos, clientData, type);

	auto &order = get_order();
	size_t count = order.size();
	for (size_t i = 0; i < items.GetCount(); i++)
	{
		const int idx = ~(count + i);
		get_order().Insert(idx, pos);
	}
	return ret;
}

int wxRearrangeListPatched::DoInsertOneItem(const wxString& item, unsigned int pos)
{
	wxCheckListBox::DoInsertOneItem(item, pos);
	// Item is not checked initially.
	const int idx = ~get_order().size();
	get_order().Insert(idx, pos);
	return pos;
}

void wxRearrangeListPatched::DoDeleteOneItem(unsigned int n)
{
	wxCheckListBox::DoDeleteOneItem(n);
	auto &order = get_order();
	int idxDeleted = order[n];
	if (idxDeleted < 0)
		idxDeleted = ~idxDeleted;
	order.RemoveAt(n);
	// Remaining items have to be reindexed.
	for (size_t i = 0; i < order.size(); i++)
	{
		int idx = order[i];
		if (idx < 0)
		{
			idx = ~idx;
			if (idx > idxDeleted)
				order[i] = ~(idx - 1);
		}
		else
		{
			if (idx > idxDeleted)
				order[i] = idx - 1;
		}
	}
}

void wxRearrangeListPatched::DoClear()
{
	wxCheckListBox::DoClear();
	get_order().Clear();
}