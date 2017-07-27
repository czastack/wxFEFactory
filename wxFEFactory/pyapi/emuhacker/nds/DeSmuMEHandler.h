#pragma once
#include "../ProcessHandler.h"

class DeSmuMEHandler : public ProcessHandler
{
public:
	bool attach() override;

	addr_t prepareAddr(addr_t addr, size_t size) override;

private:
	static const unsigned long long BASE_ADDR = 0x1451E8B90;
};