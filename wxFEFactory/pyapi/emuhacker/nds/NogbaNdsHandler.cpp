#ifdef __WXMSW__

#include "NogbaNdsHandler.h"

bool NogbaNdsHandler::attach()
{
	bool succeed = attachByWindowName(L"No$dlgClass", L"No$gba Debugger (Fullversion)");

	if (succeed) {
		u32 address;
		if (succeed = rawRead(PTR_TABLE_BASE, sizeof(address), &address))
			rawRead(address + PTR_TABLE_OFFSET, sizeof(mPtrTable), &mPtrTable);
	}

	return succeed;
}

#endif