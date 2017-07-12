#pragma once
#include "types.h"

union Color {
	struct C6
	{
		u8 b;
		u8 g;
		u8 r;
		u8 a;

		void swapBR()
		{
			u8 temp = b;
			b = r;
			r = temp;
		}
	} c6;
	struct C3_6
	{
		u8 bl : 4;
		u8 bh : 4;
		u8 gl : 4;
		u8 gh : 4;
		u8 rl : 4;
		u8 rh : 4;
		u8 al : 4;
		u8 ah : 4;
	} c3_6;
	struct C3
	{
		u8 b : 4;
		u8 g : 4;
		u8 r : 4;
		u8   : 4;
		u16 unused;

		void swapBR()
		{
			u8 temp = b;
			b = r;
			r = temp;
		}
	} c3;

	Color(): Color(0){}

	Color(uint rgb)
	{
		*this = rgb;
	}

	Color& operator=(uint rgb)
	{
		*((uint*)this) = rgb;
		return *this;
	}

	operator uint&()
	{
		return *((uint*)this);
	}

	void fromHalf(Color rgb)
	{
		c3_6.bl = c3_6.bh = rgb.c3.b;
		c3_6.gl = c3_6.gh = rgb.c3.g;
		c3_6.rl = c3_6.rh = rgb.c3.r;
	}

	Color toHalf()
	{
		Color c;
		c.c3.b = c3_6.bh;
		c.c3.g = c3_6.gh;
		c.c3.r = c3_6.rh;
		return c;
	}
};