#ifndef AGE2HANDLER_H
#define AGE2HANDLER_H

#include "GbaEmuHandler.h"

struct VBA_PtrEntry
{
	DWORD	dwPointer;
	DWORD	dwSize;
};

using PtrEntryRef = const VBA_PtrEntry &;

struct VBA_PtrStruct
{
	VBA_PtrEntry	peBIOS;
	VBA_PtrEntry	peConst;
	VBA_PtrEntry	peWRAM;
	VBA_PtrEntry	peIRAM;
	VBA_PtrEntry	peIO;
	VBA_PtrEntry	pePalette;
	VBA_PtrEntry	peVRAM;
	VBA_PtrEntry	peOAM;
	VBA_PtrEntry	peROM;

	operator const VBA_PtrEntry *() {
		return  reinterpret_cast<CONST VBA_PtrEntry *>(this);
	}
};

class VbaHandler: public GbaEmuHandler
{
public:
	bool attach() override;

private:
	static const u32 MAP_ADDR = 0x00604230;
	static BOOL CALLBACK EnumVBAWindowProc(HWND hWnd, LPARAM lParam);
};

#endif
