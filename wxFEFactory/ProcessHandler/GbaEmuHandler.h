#pragma once
#include "ProcessHandler.h"
#include "gba/gba.h"

class GbaEmuHandler : public ProcessHandler
{
public:
	virtual bool attach() = 0;

	bool read(u32 dwBaseAddr, size_t dwSize, LPVOID lpBuffer) override;

	bool write(u32 dwBaseAddr, size_t dwSize, LPCVOID lpBuffer) override;

	using ProcessHandler::read;
	using ProcessHandler::write;

protected:
	u32	mPtrTable[9];
};