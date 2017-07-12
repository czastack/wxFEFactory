#pragma once
#include "GbaEmuHandler.h"

class NogbaHandler : public GbaEmuHandler
{
public:
	bool attach() override;

private:
	static const u32 PTR_TABLE_BASE = 0x4C3B38, PTR_TABLE_OFFSET = 0x8E28;
};