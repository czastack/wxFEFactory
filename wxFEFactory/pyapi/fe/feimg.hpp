#include "../pyutils.h"
#include "graph.h"
#include "myapp.h"
#include <wx/image.h>
#include <wx/palette.h>
#include "pyapi/ui/dialogs.h"


class FeImage: wxImage
{
public:
	FeImage() = default;

	void create(int width, int height, int tileStride, py::bytes tiles, py::bytes pal, py::iterable moveArgs)
	{
		using namespace FEF;

		Destroy();
		Create(width, height, false);
		SetOption(wxIMAGE_OPTION_PNG_FORMAT, wxPNG_TYPE_PALETTE);

		OffsetTilesData tilesData;
		tilesData.tileStride = tileStride;

		Palette24 palette = *(Palette16*)bytesGetBuff(pal);
		SetPalette(palette.toWxPalette());

		tilesData.data = (Tile*)bytesGetBuff(tiles);
		for (auto &item : moveArgs)
		{
			const py::tuple &arg = item.cast<py::tuple>();
			tilesData.move(arg[0].cast<int>(), arg[1].cast<int>());
			tilesData.setSize(arg[2].cast<int>(), arg[3].cast<int>());
			copyFromTiles(*this, tilesData, palette, arg[4].cast<int>(), arg[5].cast<int>());
		}
	}

	py::bytes toTiles(int width, int height, int tileStride, size_t size, py::iterable moveArgs)
	{
		using namespace FEF;

		OffsetTilesData tilesData;
		Palette24 palette;
		py::bytes buff(nullptr, size);

		tilesData.tileStride = tileStride;
		tilesData.data = (Tile*)bytesGetBuff(buff);
		reduceColor(*this, palette);

		for (auto &item : moveArgs)
		{
			const py::tuple &arg = item.cast<py::tuple>();
			tilesData.move(arg[0].cast<int>(), arg[1].cast<int>());
			tilesData.setSize(arg[2].cast<int>(), arg[3].cast<int>());
			copyToTiles(*this, tilesData, palette, arg[4].cast<int>(), arg[5].cast<int>());
		}
		return buff;
	}

	void fillColor(py::iterable rects, int index)
	{
		using namespace FEF;

		if (IsOk())
		{
			Color24 color;
			GetPalette().GetRGB(index, &color.red, &color.green, &color.blue);
			for (auto &item : rects) {
				const py::tuple &arg = item.cast<py::tuple>();
				SetRGB({ arg[0].cast<int>() << 3, arg[1].cast<int>() << 3, arg[2].cast<int>() << 3, arg[3].cast<int>() << 3 },
					color.red, color.green, color.blue);
			}
		}
	}

	void rescale(int width, int height)
	{
		(void)Rescale(width, height);
	}

	/**
	 * Ԥ��
	 */
	void view(wxcstr title)
	{
		if (IsOk())
		{
			wxWindow *win = wxGetApp().GetTopWindow();
			SimpleDialog *dialog = new SimpleDialog(title, true, false, win);
			wxStaticBitmap *bpView = new wxStaticBitmap(dialog, wxID_ANY, wxBitmap(*this));
			dialog->setContentView(bpView, 8);
			dialog->Show();
		}
	}

	void savePng(wxcstr path)
	{
		SaveFile(path);
	}
private:

};