#include <wx/wx.h>
#include "containers.h"


/**
 * 获取布局参数
 */

void SizerLayout::getBoxArg(View & child, int * pFlex, int * pFlag, int * pPadding)
{
	int flag = 0;
	if (child.getStyle(STYLE_EXPAND, false))
	{
		flag |= wxEXPAND;
	}

	wxcstr showPad = child.getStyle(STYLE_SHOWPADDING, wxNoneString);

	if (showPad != wxNoneString)
	{
		if (showPad.size() == 1)
		{
			if (showPad[0] != '0')
				flag |= wxALL;
		}
		else if (showPad.size() == 7)
		{
			if (showPad[0] != '0')
				flag |= wxTOP;
			if (showPad[2] != '0')
				flag |= wxRIGHT;
			if (showPad[4] != '0')
				flag |= wxBOTTOM;
			if (showPad[6] != '0')
				flag |= wxLEFT;
		}
		else {
			log_message(wxString::Format(wxT("%s: %s not available"), STYLE_SHOWPADDING, showPad));
		}
	}

	wxcstr vertical = child.getStyle(STYLE_VERTICALALIGN, wxNoneString);

	if (vertical != wxNoneString)
	{
		if (vertical == wxT("top"))
		{
			flag |= wxALIGN_TOP;
		}
		else if (vertical == wxT("bottom"))
		{
			flag |= wxALIGN_BOTTOM;
		}
		else if (vertical == wxT("middle"))
		{
			flag |= wxALIGN_CENTER_VERTICAL;
		}
		else {
			log_message(wxString::Format(wxT("%s: %s not available"), STYLE_VERTICALALIGN, vertical));
		}
	}

	wxcstr align = child.getStyle(STYLE_ALIGN, wxNoneString);

	if (align != wxNoneString)
	{
		if (vertical == wxT("left"))
		{
			flag |= wxALIGN_LEFT;
		}
		else if (vertical == wxT("right"))
		{
			flag |= wxALIGN_RIGHT;
		}
		else if (vertical == wxT("center"))
		{
			flag |= wxALIGN_CENTER_HORIZONTAL;
		}
		else {
			log_message(wxString::Format(wxT("%s: %s not available"), STYLE_ALIGN, vertical));
		}
	}
	*pFlag = flag;
	*pFlex = child.getStyle(STYLE_FLEX, 0);
	*pPadding = child.getStyle(STYLE_PADDING, 5);
}

void SplitterWindow::__exit__(py::args & args)
{
	int len = m_children.size();
	if (len > 2)
	{
		log_message("SplitterWindow 不支持大于2个子元素");
		return;
	}
	Layout::__exit__(args);
	if (len == 1)
	{
		View &child = *py::cast<View*>(m_children[0]);
		ctrl().Initialize(child);
	}
	else if (len == 2)
	{
		View &child1 = *py::cast<View*>(m_children[0]);
		View &child2 = *py::cast<View*>(m_children[1]);
		if (m_horizontal)
			ctrl().SplitHorizontally(child1, child2, m_sashpos);
		else
			ctrl().SplitVertically(child1, child2, m_sashpos);
	}
}


void BookCtrlBase::doAdd(View & child)
{
	Item *item = (Item*)child.ptr()->GetClientData();
	if (Item::isInstance(item))
	{
		// 替换回原指针
		child.ptr()->SetClientData(&child);

		wxcstr caption = pyDictGet(item->m_kwargs, wxT("caption"), wxNoneString);
		ctrl().AddPage(child, caption);

		py::cast(item).dec_ref();
	}
	else
	{
		log_message(wxString::Format("Child of %s must be Item.", "Notebook"));
	}
}

View * BookCtrlBase::getPage(int n)
{
	if (n == -1)
	{
		n = getSelection();
	}
	return (View*)ctrl().GetPage(n)->GetClientData();
}


void init_containers(py::module & m)
{
	using namespace py::literals;

	auto className = "className"_a = None;
	auto style = "style"_a = None;
	auto styles = "styles"_a = None;
	auto wxstyle = "wxstyle"_a = 0;

	py::class_t<Vertical, Layout>(m, "Vertical")
		.def_init(py::init<pyobj, pyobj, pyobj>(), styles, className, style);

	py::class_t<Horizontal, Layout>(m, "Horizontal")
		.def_init(py::init<pyobj, pyobj, pyobj>(), styles, className, style);

	py::class_t<GridLayout, Layout>(m, "GridLayout")
		.def_init(py::init<int, int, int, int, pyobj, pyobj, pyobj>(),
			"rows"_a = 0, "cols"_a = 2, "vgap"_a = 0, "hgap"_a = 0,
			styles, className, style);

	py::class_t<FlexGridLayout, Layout>(m, "FlexGridLayout")
		.def_init(py::init<int, int, int, int, pyobj, pyobj, pyobj>(),
			"rows"_a = 0, "cols"_a = 2, "vgap"_a = 0, "hgap"_a = 0,
			styles, className, style)
		.def("AddGrowableRow", &FlexGridLayout::AddGrowableRow, "index"_a, "flex"_a = 0)
		.def("RemoveGrowableRow", &FlexGridLayout::RemoveGrowableRow, "index"_a)
		.def("AddGrowableCol", &FlexGridLayout::AddGrowableCol, "index"_a, "flex"_a = 0)
		.def("RemoveGrowableCol", &FlexGridLayout::RemoveGrowableCol, "index"_a)
		.def_property("flexDirection", &FlexGridLayout::GetFlexibleDirection, &FlexGridLayout::SetFlexibleDirection);

	py::class_t<ScrollView, Layout>(m, "ScrollView")
		.def_init(py::init<bool, pyobj, pyobj, pyobj>(),
			"horizontal"_a = false, styles, className, style);

	py::class_t<SplitterWindow, Layout>(m, "SplitterWindow")
		.def_init(py::init<bool, int, pyobj, pyobj, pyobj>(),
			"horizontal"_a = false, "sashpos"_a = 0, styles, className, style);

	py::class_t<StaticBox, Layout>(m, "StaticBox")
		.def_init(py::init<wxcstr, pyobj, pyobj, pyobj>(),
			"label"_a, styles, className, style)
		.def("getLabel", &StaticBox::getLabel)
		.def("setLabel", &StaticBox::setLabel)
		.def_property("label", &StaticBox::getLabel, &StaticBox::setLabel);

	py::class_t<BookCtrlBase, Layout>(m, "BookCtrlBase")
		.def("getPage", &BookCtrlBase::getPage, "n"_a = -1)
		.def("getPageCount", &BookCtrlBase::getPageCount)
		.def("setPageText", &BookCtrlBase::setPageText)
		.def("getPageText", &BookCtrlBase::getPageText)
		.def_property("index", &BookCtrlBase::getSelection, &BookCtrlBase::setSelection);

	py::class_t<Notebook, BookCtrlBase>(m, "Notebook")
		.def_init(py::init<int, pyobj, pyobj, pyobj>(), wxstyle, styles, className, style);

	py::class_t<Listbook, BookCtrlBase>(m, "Listbook")
		.def_init(py::init<int, pyobj, pyobj, pyobj>(), wxstyle, styles, className, style);
}
