#ifdef __WXMSW__

#include "types.h"
#include "gba.h"

GBA_MEM_TABLE GBA_MEMORY_SIZE = {
	0x00003FFF, //BIOS
	0,		    //Const
	0x0003FFFF, //WRAM
	0x00007FFF, //IRAM
	0x000003FE, //IO
	0x000003FF, //Palette
	0x00017FFF, //VRAM
	0x000003FF, //OAM
	0x01FFFFFF, //ROM
	// 	0x01FFFFFF,
	// 	0x01FFFFFF,
	// 	0x0000FFFF,
};

#endif