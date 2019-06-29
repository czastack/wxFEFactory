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
		// ����Ŀ��λ�õ�ָ��
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
		// ����Ŀ��λ�õ�ָ��
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
		// ����Ŀ��λ�õ�ָ��
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
}