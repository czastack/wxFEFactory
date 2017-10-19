#ifdef _WIN32

#include "types.h"
#include "nds.h"

NDS_MEM_TABLE NDS_MEMORY_SIZE = {
	0x00003FFF,  // 0X Instruction TCM (32KB)
	0x00000003,  // 1X UNUSED_RAM
	0x003FFFFF,  // 2X Main Memory     (4MB)
	0x00007FFF,  // 3X Shared WRAM     (0KB, 16KB, or 32KB can be allocated to ARM9)
	0x00FFFFFF,  // 4X ARM9-I/O Ports
	0x000007FF,  // 5X Standard Palettes (2KB)
	0x00FFFFFF,  // 6X VRAM
	0x000007FF,  // 7X OAM (2KB)
	0x01FFFFFF,  // 8X GBA Slot ROM (max 32MB)
	0x0000FFFF,  // 9X GBA Slot RAM (max 64KB)
	// 0x00000003,  // AX 
	// 0x00000003,  // BX 
	// 0x00000003,  // CX 
	// 0x00000003,  // DX 
	// 0x00000003,  // EX 
	// 0x00007FFF,  // FX 
};

#endif