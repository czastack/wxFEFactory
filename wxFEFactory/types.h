#pragma once

typedef unsigned char byte, u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned int uint;

typedef const class wxString& wxcstr;
extern const class wxString wxNoneString;

#ifndef NULL
#define NULL 0
#endif

#define NOVTABLE	__declspec(novtable)
#define NOTREDEF	__declspec(selectany)
#define BEGIN_PACK	__pragma(pack(1))
#define END_PACK	__pragma(pack())