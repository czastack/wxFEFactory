#pragma once

class wxImage;
class wxPalette;

namespace FEF {

enum MyEnum
{
	GBA_COLOR_MAX = 16,
};

/**
 * 颜色 BGR555 2字节
 */
struct Color
{
	u16 red   : 5;
	u16 green : 5;
	u16 blue  : 5;

	Color &operator=(struct Color24 c);
};


/**
 * 颜色 BGR888 3字节
 */
struct Color24
{
	u8 red;
	u8 green;
	u8 blue;

	Color24 &operator=(Color c)
	{
		blue = c.blue << 3;
		green = c.green << 3;
		red = c.red << 3;
		return *this;
	}

	Color24 &operator=(u32 rgb)
	{
		const u8* p = (u8*)&rgb;
		blue  = p[0];
		green = p[1];
		red   = p[2];
		return *this;
	}

	bool operator==(const Color24 &c) const
	{
		return red == c.red && green == c.green && blue == c.blue;
	}

	void asBGR(Color c)
	{
		blue = c.red << 3;
		green = c.green << 3;
		red = c.blue << 3;
	}

	void put24(u8 *dst)
	{
		*(Color24*)dst = *this;
	}
};


/**
 * 颜色 ABGR 4字节
 */
struct Color32: Color24
{
	u8 alpha;

	Color32 &operator=(Color c) 
	{
		(void)Color24::operator=(c);
		alpha = 0xFFu;
		return *this;
	}

	bool operator==(const Color32 &c) const
	{
		return *(u32*)this == *(u32*)&c;
	}

	operator u32()
	{
		return *(u32*)this;
	}
};


inline Color& Color::operator=(Color24 c) {
	blue = c.blue >> 3;
	green = c.green >> 3;
	red = c.red >> 3;
	return *this;
}

/**
 * 调色板
 */
template<class color_t, int bpp=4>
struct CPalette
{
	enum {
		SIZE = 1 << bpp
	};

	/**
	 * wxPalette 颜色分量
	 */
	struct wxPaletteComp
	{
		u8 red[SIZE];
		u8 green[SIZE];
		u8 blue[SIZE];
	};


	color_t data[SIZE];

	CPalette() = default;

	template<class palette_t>
	CPalette(palette_t &pal)
	{
		for (int i = 0; i < SIZE; i++)
		{
			data[i] = pal[i];
		}
	}
	
	CPalette(const wxPalette &pal)
	{
		(void)operator=(pal);
	}

	int find(color_t c) const {
		int i;
		for (i = 0; i < SIZE; i++)
		{
			if (data[i] == c)
				break;
		}
		if (i == SIZE)
			i = -1;
		return i;
	}

	void clear()
	{
		memset(data, 0, sizeof(data));
	}

	wxPalette toWxPalette() const {
		wxPaletteComp tmp;
		for (int i = 0; i < SIZE; ++i)
		{
			tmp.red[i] = data[i].red;
			tmp.blue[i] = data[i].blue;
			tmp.green[i] = data[i].green;
		}
		return wxPalette(SIZE, tmp.red, tmp.green, tmp.blue);
	}

	CPalette& operator=(const wxPalette &pal)
	{
		for (int i = 0; i < SIZE; i++)
		{
			pal.GetRGB(i, &data[i].red, &data[i].green, &data[i].blue);
		}
		return *this;
	}

	operator color_t *()
	{
		return data;
	}

	operator const color_t *() const
	{
		return data;
	}
};

typedef CPalette<Color> Palette16;
typedef CPalette<Color24> Palette24;
typedef CPalette<Color32> Palette32;


/**
 * 图块
 * 32字节，由8*8小格组成，每小格4位，16色
 */
typedef u32 Tile[8];

/**
 * 人物大头像
 * 4*32个Tile
 */
typedef Tile BigPortraitTiles[4][32];

/**
 * 图块数据
 */
struct TilesData
{
	Tile* data;
	int tileStride;	// 一行的Tile个数
	int colspan;	// Tile列数
	int rowspan;	// Tile行数

	void setSize(int w, int y)
	{
		colspan = w;
		rowspan = y;
	}
};

/**
 * 记录偏移的图块数据
 */
struct OffsetTilesData : TilesData
{
	int offsetX;	// 列偏移
	int offsetY;	// 行偏移
	/**
	 * 获取当前偏移Tile的指针
	 */
	Tile* GetData() const
	{
		return data + offsetX + offsetY * tileStride;
	}

	void move(int x, int y) {
		offsetX = x;
		offsetY = y;
	}
};

/**
 * 每字节高低4位互换
 * 4位索引Bitmap中每字节高4位决定前一个像素，
 * 低4位决定后一个像素，GBA 4pp则相反
 */
/*
inline u32 reverse4bits(u32 data)
{
	return ((data >> 4) & 0x0F0F0F0F) | ((data & 0x0F0F0F0F) << 4);
}*/


/**
 * 由大头像构造
 */
/*wxImage createBigPortraitBitmap(BigPortraitTiles, Palette16&);*/

void copyFromTiles(wxImage &img, const OffsetTilesData &src, const Palette24 &palette, int dstTileX, int dstTileY);
void copyToTiles(wxImage &img, const OffsetTilesData &dstData, const Palette24 &palette, int dstTileX, int dstTileY);

void reduceColor(wxImage &image, Palette24 &palette);
}