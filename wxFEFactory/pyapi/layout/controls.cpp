#include <wx/wx.h>
#include "controls.h"

long Text::getAlignStyle()
{
	pyobj style = getStyle(STYLE_TEXTALIGN);
	long wxstyle = 0;
	if (style != None)
	{
		wxcstr align = style.cast<wxString>();
		if (align != wxNoneString) {
			if (align == wxT("center"))
			{
				wxstyle |= wxALIGN_CENTER_HORIZONTAL;
			}
			else if (align == wxT("right"))
			{
				wxstyle |= wxALIGN_RIGHT;
			}
			else if (align == wxT("left"))
			{
				wxstyle |= wxALIGN_LEFT;
			}
		}
	}
	return wxstyle;
}

void RadioBox::applyStyle()
{
	View::applyStyle();

	pyobj style;

	style = getStyle(STYLE_FLEXDIRECTION);
	if (style != None)
	{
		wxcstr dir = style.cast<wxString>();
		if (dir != wxNoneString) {
			long style = ctrl().GetWindowStyle();
			if (dir == wxT("row"))
			{
				style |= wxRA_SPECIFY_ROWS;
			}
			else if (dir == wxT("column"))
			{
				style |= wxRA_SPECIFY_COLS;
			}
			ctrl().SetWindowStyle(style);
		}
	}
}