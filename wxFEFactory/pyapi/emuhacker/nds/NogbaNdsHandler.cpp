#ifdef _WIN32

#include "NogbaNdsHandler.h"

bool NogbaNdsHandler::attach()
{
	bool succeed = attachByWindowName(L"No$dlgClass", L"No$gba Debugger (Fullversion)");

	if (succeed) {
		u32 address;
		if (succeed = rawRead(PTR_TABLE_BASE, &address, sizeof(address)))
			rawRead(address + PTR_TABLE_OFFSET, &mPtrTable, sizeof(mPtrTable));
	}

	return succeed;
}

#endif