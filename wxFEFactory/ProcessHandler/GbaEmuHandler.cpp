#include <windows.h>
#include "GbaEmuHandler.h"
#include "utils/utils.h"

bool GbaEmuHandler::read(u32 dwBaseAddr, size_t dwSize, LPVOID lpBuffer)
{
	if (dwBaseAddr < 0x0A000000) {
		int index = (dwBaseAddr & 0x0F000000) >> 24;
		if (index > 8)
			index = 8;
		dwBaseAddr &= 0x00FFFFFF;

		if (dwBaseAddr + dwSize <= GBA_MEMORY_SIZE[index])
			return ProcessHandler::read(mPtrTable[index] + dwBaseAddr, dwSize, lpBuffer);
	}
	return false;
}

bool GbaEmuHandler::write(u32 dwBaseAddr, size_t dwSize, LPCVOID lpBuffer)
{
	if (dwBaseAddr < 0x0A000000) {
		int index = (dwBaseAddr & 0x0F000000) >> 24;
		if (index > 8)
			index = 8;
		dwBaseAddr &= 0x00FFFFFF;

		if (dwBaseAddr + dwSize <= GBA_MEMORY_SIZE[index])
			return ProcessHandler::write(mPtrTable[index] + dwBaseAddr, dwSize, lpBuffer);
	}
	return false;
}