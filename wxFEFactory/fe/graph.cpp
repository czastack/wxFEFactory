#include <wx/image.h>
#include <wx/palette.h>
#include <wx/quantize.h>
#include <iostream>
#include "types.h"
#include "graph.h"
#include "utils/utils.h"

namespace FEF {

	/*void copyFromTiles(wxAlphaPixelData &bpData, const TilesData & src, Color32Palette palette, int dstTileX, int dstTileY)
	{
		// 绘制目标位置的指针
		auto dst = bpData.GetPixels();
		dst.Offset(bpData, dstTileX << 3, (dstTileY << 3));
		Tile* srcTile = src.data;
		u32 tileRow;
		// int emptyOffset = bpData.GetRowStride() - (src.colspan << 3) * decltype(dst)::PixelFormat::SizePixel;
		
		for (dstTileY = 0; dstTileY < src.rowspan; ++dstTileY)
		{
			for (int i = 0; i < 8; ++i)
			{
				auto rowStart = dst;
				for (dstTileX = 0; dstTileX < src.colspan; ++dstTileX)
				{
					tileRow = srcTile[dstTileX][i];
					for (int j = 0; j < 8; ++j) {
						dst.Data() = palette[tileRow & 0xF];
						tileRow >>= 4;
						++dst;
					}
				}
				dst = rowStart;
				dst.OffsetY(bpData, 1);
			}
			srcTile += src.tileStride;
		}
	}*/

	void copyFromTiles(wxImage &img, const OffsetTilesData &src, const Palette24 &palette, int dstTileX, int dstTileY)
	{
		// 绘制目标位置的指针
		Color24 *dst = (Color24*)img.GetData() + img.GetWidth() * (dstTileY << 3) + (dstTileX << 3);
		Tile* srcTile = src.GetData();
		u32 tileRow;
		int emptyOffset = img.GetWidth() - (src.colspan << 3);

		for (dstTileY = 0; dstTileY < src.rowspan; ++dstTileY)
		{
			for (int i = 0; i < 8; ++i)
			{
				for (dstTileX = 0; dstTileX < src.colspan; ++dstTileX)
				{
					tileRow = srcTile[dstTileX][i];
					for (int j = 0; j < 8; ++j) {
						*dst = palette[tileRow & 0xF];
						tileRow >>= 4;
						++dst;
					}
				}
				dst += emptyOffset;
			}
			srcTile += src.tileStride;
		}
	}

	void copyToTiles(wxImage &img, const OffsetTilesData &dstData, const Palette24 &palette, int dstTileX, int dstTileY)
	{
		// 绘制目标位置的指针
		Color24 *src = (Color24*)img.GetData() + img.GetWidth() * (dstTileY << 3) + (dstTileX << 3);
		Tile* dstTile = dstData.GetData();
		int emptyOffset = img.GetWidth() - (dstData.colspan << 3);

		for (dstTileY = 0; dstTileY < dstData.rowspan; ++dstTileY)
		{
			for (int i = 0; i < 8; ++i)
			{
				for (dstTileX = 0; dstTileX < dstData.colspan; ++dstTileX)
				{
					u32 &tileRow = dstTile[dstTileX][i];
					tileRow = 0;
					for (int j = 0; j < 8; ++j) {
						tileRow >>= 4;
						tileRow |= palette.find(*src) << 28;
						++src;
					}
				}
				src += emptyOffset;
			}
			dstTile += dstData.tileStride;
		}
	}

	void reduceColor(wxImage &image, Palette24 &palette) 
	{
		if ((image.HasPalette() ? image.GetPalette().GetColoursCount() : image.CountColours()) > GBA_COLOR_MAX)
		{
			wxImage reducedImage;
			if (wxQuantize::Quantize(image, reducedImage, GBA_COLOR_MAX, 0, wxQUANTIZE_FILL_DESTINATION_IMAGE))
			{
				image = reducedImage;
			}
		}
		if (image.HasPalette())
		{
			palette = image.GetPalette();
		}
		else 
		{
			const int iHeight = image.GetHeight();
			const int iWidth = image.GetWidth();
			auto pColors = (const Color24*)image.GetData();
			wxLongToLongHashMap paletteMap;
			u32 value;
			size_t index;

			for (int y = 0; y < iHeight; ++y)
			{
				for (int x = 0; x < iWidth; ++x)
				{
					value = wxImageHistogram::MakeKey(pColors->red, pColors->green, pColors->blue);
					auto it = paletteMap.find(value);

					if (it == paletteMap.end())
					{
						index = paletteMap.size();
						paletteMap[value] = index;
						palette[index] = *pColors;
					}

					++pColors;
				}
			}
		}
	}

	/*

	struct CopyArg
	{
		int x, y, w, h, tx, ty;
	};

	wxImage createBigPortraitBitmap(BigPortraitTiles tiles, Palette16 &pal)
	{
		wxImage bp(80, 80, false);

		OffsetTilesData tilesData;
		tilesData.tileStride = 32;

		Palette24 palette24(pal);

		CopyArg args[] = {
			{ 0, 0, 8, 4, 1, 0 },
			{ 8, 0, 8, 4, 1, 4 },
			{ 16, 0, 4, 2, 1, 8 },
			{ 16, 2, 4, 2, 5, 8 },
			{ 21, 1, 1, 3, 0, 7 },
			{ 22, 1, 1, 3, 9, 7 },
			{ 7, 0, 1, 1, 0, 6 },
			{ 7, 0, 1, 1, 9, 6 },
		};

		wxRect empty[] = {
			{ 0, 0, 1, 6 },
			{ 9, 0, 1, 6 }
		};

		tilesData.data = tiles[0];
		for (auto &arg : args)
		{
			tilesData.move(arg.x, arg.y);
			tilesData.setSize(arg.w, arg.h);
			copyFromTiles(bp, tilesData, palette24, arg.tx, arg.ty);
		}

		for (auto &arg : empty) {
			bp.SetRGB({ arg.x << 3, arg.y << 3, arg.width << 3, arg.height << 3 }, 
				palette24[0].red, palette24[0].green, palette24[0].blue);
		}

		/ *reduceColor(bp, palette24);
		wxMemoryBuffer buff(4096);
		BigPortraitTiles * p = (BigPortraitTiles*)buff.GetData();
		tilesData.data = *p[0];
		for (auto &arg : args)
		{
			tilesData.move(arg.x, arg.y);
			tilesData.setSize(arg.w, arg.h);
			copyToTiles(bp, tilesData, palette24, arg.tx, arg.ty);
		}


		bp.Clear();
		for (auto &arg : args)
		{
			tilesData.move(arg.x, arg.y);
			tilesData.setSize(arg.w, arg.h);
			copyFromTiles(bp, tilesData, palette24, arg.tx, arg.ty);
		}

		for (auto &arg : empty) {
			bp.SetRGB({ arg.x << 3, arg.y << 3, arg.width << 3, arg.height << 3 },
				palette24[0].red, palette24[0].green, palette24[0].blue);
		}* /

		/ * // 大头像上部
		tilesData.data = tiles[0];
		tilesData.move(0, 0);
		tilesData.setSize(8, 4);
		copyFromTiles(bp, tilesData, palette24, 1, 0);

		// 大头像中部
		tilesData.move(8, 0);
		copyFromTiles(bp, tilesData, palette24, 1, 4);

		// 大头像左下
		tilesData.move(16, 0);
		tilesData.setSize(4, 2);
		copyFromTiles(bp, tilesData, palette24, 1, 8);

		// 大头像右下
		tilesData.move(16, 2);
		copyFromTiles(bp, tilesData, palette24, 5, 8);

		// 大头像左下角
		tilesData.move(21, 1);
		tilesData.setSize(1, 3);
		copyFromTiles(bp, tilesData, palette24, 0, 7);

		// 大头像右下角
		tilesData.move(22, 1);
		copyFromTiles(bp, tilesData, palette24, 9, 7);


		tilesData.move(7, 0);
		tilesData.setSize(1, 1);
		copyFromTiles(bp, tilesData, palette24, 0, 6);
		copyFromTiles(bp, tilesData, palette24, 9, 6);* /
		return bp;
	}*/
}