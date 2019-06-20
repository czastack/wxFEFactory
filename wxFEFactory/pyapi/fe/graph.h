#pragma once

class wxImage;
class wxPalette;

namespace FEF {

enum MyEnum
{
	GBA_COLOR_MAX = 16,
};

/**
 * ��ɫ BGR555 2�ֽ�
 */
struct Color
{
	u16 red   : 5;
	u16 green : 5;
	u16 blue  : 5;

	Color &operator=(struct Color24 c);
};


/**
 * ��ɫ BGR888 3�ֽ�
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
 * ��ɫ ABGR 4�ֽ�
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
 * ��ɫ��
 */
template<class color_t, int bpp=4>
struct CPalette
{
	enum {
		SIZE = 1 << bpp
	};

	/**
	 * wxPalette ��ɫ����
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
 * ͼ��
 * 32�ֽڣ���8*8С����ɣ�ÿС��4λ��16ɫ
 */
typedef u32 Tile[8];

/**
 * �����ͷ��
 * 4*32��Tile
 */
typedef Tile BigPortraitTiles[4][32];

/**
 * ͼ������
 */
struct TilesData
{
	Tile* data;
	int tileStride;	// һ�е�Tile����
	int colspan;	// Tile����
	int rowspan;	// Tile����

	void setSize(int w, int y)
	{
		colspan = w;
		rowspan = y;
	}
};

/**
 * ��¼ƫ�Ƶ�ͼ������
 */
struct OffsetTilesData : TilesData
{
	int offsetX;	// ��ƫ��
	int offsetY;	// ��ƫ��
	/**
	 * ��ȡ��ǰƫ��Tile��ָ��
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
 * ÿ�ֽڸߵ�4λ����
 * 4λ����Bitmap��ÿ�ֽڸ�4λ����ǰһ�����أ�
 * ��4λ������һ�����أ�GBA 4pp���෴
 */
/*
inline u32 reverse4bits(u32 data)
{
	return ((data >> 4) & 0x0F0F0F0F) | ((data & 0x0F0F0F0F) << 4);
}*/


/**
 * �ɴ�ͷ����
 */
/*wxImage createBigPortraitBitmap(BigPortraitTiles, Palette16&);*/

void copyFromTiles(wxImage &img, const OffsetTilesData &src, const Palette24 &palette, int dstTileX, int dstTileY);
void copyToTiles(wxImage &img, const OffsetTilesData &dstData, const Palette24 &palette, int dstTileX, int dstTileY);

void reduceColor(wxImage &image, Palette24 &palette);
}