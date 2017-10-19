#ifdef _WIN32

#include "DeSmuMEHandler.h"
#include "nds.h"

bool DeSmuMEHandler::attach()
{
	bool succeed = attachByWindowName(L"DeSmuME", NULL);

	return succeed;
}

addr_t DeSmuMEHandler::prepareAddr(addr_t addr, size_t size)
{
	if (addr < 0x0A000000) {
		addr &= 0x00FFFFFF;

		if (addr + size <= NDS_MEMORY_SIZE[2])
			return BASE_ADDR + addr;
	}
	return false;
}

#endif