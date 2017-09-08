#ifdef __WXMSW__

#include "NogbaHandler.h"

bool NogbaHandler::attach()
{
	bool succeed = attachByWindowName(L"No$dlgClass", L"No$gba Debugger (Fullversion)");
	
	if (succeed) {
		u32 address;
		if (succeed = ProcessHandler::read(PTR_TABLE_BASE, &address, sizeof(address)))
			rawRead(address + PTR_TABLE_OFFSET, &mPtrTable, sizeof(mPtrTable));
	}
	
	return succeed;
}

#endif