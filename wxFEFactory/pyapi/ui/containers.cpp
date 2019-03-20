#include <wx/wx.h>
#include "containers.h"


/**
 * 获取布局参数
 */

void SizerLayout::getBoxArg(View & child, int * pWeight, int * pFlag, int * pPadding)
{
	int flag = 0;
	if (child.getStyle(STYLE_EXPAND, false))
	{
		flag |= wxEXPAND;
	}

	int padding_flag = child.getStyle(STYLE_SHOWPADDING, 0);

	if (padding_flag != 0)
	{
		if (padding_flag == 1)
		{
			flag |= wxALL;
		}
		else
		{
			if (padding_flag & 0b1000)
				flag |= wxTOP;
			if (padding_flag & 0b0100)
				flag |= wxRIGHT;
			if (padding_flag & 0b0010)
				flag |= wxBOTTOM;
			if (padding_flag & 0b0001)
				flag |= wxLEFT;
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
		if (align == wxT("left"))
		{
			flag |= wxALIGN_LEFT;
		}
		else if (align == wxT("right"))
		{
			flag |= wxALIGN_RIGHT;
		}
		else if (align == wxT("center"))
		{
			flag |= wxALIGN_CENTER_HORIZONTAL;
		}
		else {
			log_message(wxString::Format(wxT("%s: %s not available"), STYLE_ALIGN, align));
		}
	}
	*pFlag = flag;
	*pWeight = child.getStyle(STYLE_WEIGHT, 0);
	*pPadding = child.getStyle(STYLE_PADDING, 5);
}

void SizerLayout::doAdd(View & child)
{
	int weight, flag, padding;
	getBoxArg(child, &weight, &flag, &padding);
	m_elem->GetSizer()->Add(child, weight, flag, padding);
}

void SplitterWindow::__exit__(py::args & args)
{
	int len = m_children.size();
	if (len > 2)
	{
		log_message("SplitterWindow 不支持大于2个子元素");
		return;
	}
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
	Layout::__exit__(args);
}


void BookCtrlBase::doAdd(View & child)
{
	Item *item = (Item*)child.ptr()->GetClientData();
	if (Item::isInstance(item))
	{
		// 替换回原指针
		child.ptr()->SetClientData(&child);

		wxcstr caption = PyDictGet(item->m_kwargs, wxT("caption"), wxNoneString);
		ctrl().AddPage(child, caption);

		py::cast(item).dec_ref();
	}
	/*else
	{
		log_message(wxString::Format("Child of %s must be Item.", "Notebook"));
	}*/
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
	auto evt_reset = "reset"_a = true;

	py::class_t<Vertical, Layout>(m, "Vertical")
		.def(py::init<pyobj, pyobj, pyobj>(), styles, className, style);

	py::class_t<Horizontal, Layout>(m, "Horizontal")
		.def(py::init<pyobj, pyobj, pyobj>(), styles, className, style);

	py::class_t<GridLayout, Layout>(m, "GridLayout")
		.def(py::init<int, int, int, int, pyobj, pyobj, pyobj>(),
			"rows"_a = 0, "cols"_a = 2, "vgap"_a = 0, "hgap"_a = 0,
			styles, className, style);

	py::class_t<FlexGridLayout, Layout>(m, "FlexGridLayout")
		.def(py::init<int, int, int, int, pyobj, pyobj, pyobj>(),
			"rows"_a = 0, "cols"_a = 2, "vgap"_a = 0, "hgap"_a = 0,
			styles, className, style)
		.def("AddGrowableRow", &FlexGridLayout::AddGrowableRow, "index"_a, "weight"_a = 0)
		.def("RemoveGrowableRow", &FlexGridLayout::RemoveGrowableRow, "index"_a)
		.def("AddGrowableCol", &FlexGridLayout::AddGrowableCol, "index"_a, "weight"_a = 0)
		.def("RemoveGrowableCol", &FlexGridLayout::RemoveGrowableCol, "index"_a)
		.def_property("flexDirection", &FlexGridLayout::GetFlexibleDirection, &FlexGridLayout::SetFlexibleDirection);

	py::class_t<ScrollView, Layout>(m, "ScrollView")
		.def(py::init<bool, pyobj, pyobj, pyobj>(),
			"horizontal"_a = false, styles, className, style);

	py::class_t<SplitterWindow, Layout>(m, "SplitterWindow")
		.def(py::init<bool, int, pyobj, pyobj, pyobj>(),
			"horizontal"_a = false, "sashpos"_a = 0, styles, className, style);

	py::class_t<StaticBox, Layout>(m, "StaticBox")
		.def(py::init<wxcstr, pyobj, pyobj, pyobj>(),
			"label"_a, styles, className, style);

	py::class_t<BookCtrlBase, Layout>(m, "BookCtrlBase")
		.def("getPage", &BookCtrlBase::getPage, "n"_a = -1)
		.def("getPageCount", &BookCtrlBase::getPageCount)
		.def("setPageText", &BookCtrlBase::setPageText)
		.def("getPageText", &BookCtrlBase::getPageText)
		.def("setOnPageChange", &BookCtrlBase::setOnPageChange, "fn"_a, evt_reset)
		.def_property("index", &BookCtrlBase::getSelection, &BookCtrlBase::setSelection);

	py::class_t<Notebook, BookCtrlBase>(m, "Notebook")
		.def(py::init<int, pyobj, pyobj, pyobj>(), wxstyle, styles, className, style);

	py::class_t<Listbook, BookCtrlBase>(m, "Listbook")
		.def(py::init<int, pyobj, pyobj, pyobj>(), wxstyle, styles, className, style);
}
