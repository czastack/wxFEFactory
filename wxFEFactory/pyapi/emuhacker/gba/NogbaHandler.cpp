#include "NogbaHandler.h"

bool NogbaHandler::attach()
{
	bool succeed = attachByWindowName(L"No$dlgClass", L"No$gba Debugger (Fullversion)");
	
	if (succeed) {
		u32 address;
		if (succeed = ProcessHandler::read(PTR_TABLE_BASE, sizeof(address), &address))
			rawRead(address + PTR_TABLE_OFFSET, sizeof(mPtrTable), &mPtrTable);
	}
	
	return succeed;
}
