#include <wx/wx.h>
#include "layoutbase.h"


wxVector<Layout*> View::LAYOUTS;

View::View(pycref className, pycref style)
	:m_class(className), m_style(style)
{
	if (py::isinstance<py::str>(m_class) && m_class.contains(" "))
	{
		m_class = m_class.attr("split")(" ");
	}
	Layout* pLayout = getActiveLayout();
	if (pLayout)
	{
		// 检测样式表
		auto styles_list = pLayout->getStylesList();
		if (styles_list)
		{
			for (auto e : *styles_list)
			{
				testStyles(py::reinterpret_borrow<py::object>(e));
			};
		}
	}
}

View::~View() {
	m_event_table.clear();
	m_event_table.release();
	if (m_contextmenu)
	{
		m_contextmenu.dec_ref();
		m_contextmenu.release();
	}
}

void View::addToParent() {
	Layout* pLayout = getActiveLayout();
	if (pLayout)
	{
		pLayout->add(*this);
	}
}

int View::parseColor(wxcstr color, uint defval)
{
	u32 rgb = defval;
	if (!color.IsEmpty())
	{
		color.substr(1).ToULong(&rgb, 16);
		if (color.size() == 4)
		{
			Color c;
			c.fromHalf(rgb);
			c.c6.swapBR();
			rgb = c;
		}
	}
	return rgb;
}

wxWindow * View::getActiveWindow()
{
	Layout *layout = getActiveLayout();
	return layout ? layout->ptr() : nullptr;
}

wxWindow* View::safeActiveWindow()
{
	Layout *layout = getActiveLayout();
	return layout ? layout->ptr() : wxGetApp().GetTopWindow();
}

void View::addStyle(pyobj style)
{
	pyobj tmp;
	if (py::isinstance<py::list>(m_style))
	{
		// 追加
		tmp = m_style;
	}
	else {
		// 新列表
		py::list tmpList = py::list();
		if (!m_style.is_none())
		{
			tmpList.append(m_style);
		}
		tmp = tmpList;
	}
	py::list tmpList = tmp.cast<py::list>();
	if (py::isinstance<py::list>(style))
	{
		tmpList.attr("extend")(style);
	}
	else
	{
		tmpList.append(style);
	}
	m_style = tmpList;
}

pyobj View::getStyle(wxcstr key)
{
	if (py::isinstance<py::list>(m_style))
	{
		static auto reversed = py::module::import("builtins").attr("reversed");
		auto tmp = reversed(m_style);
		pyobj pykey = py::str(key);
		PyObject* ret;

		for (auto &e : tmp)
		{
			ret = PyDict_GetItem(e.ptr(), pykey.ptr());
			if (ret)
			{
				return py::reinterpret_borrow<py::object>(ret);
			}
		}
		return None;
	}
	return pyDictGet(m_style, key);
}

bool View::hasStyle(pyobj & key)
{
	if (py::isinstance<py::list>(m_style))
	{
		for (auto &e : m_style)
		{
			if (e != None && e.contains(key))
			{
				return true;
			}
		}

		return false;
	}
	return m_style != None && m_style.contains(key);
}

/**
* 尝试应用样式表
*/

void View::testStyles(pycref styles)
{
	pycref typecase = pyDictGet(styles, wxT("type"), None);
	pycref classcase = pyDictGet(styles, wxT("class"), None);

	pyobj style = pyDictGet(typecase, getTypeName());
	if (!style.is_none())
	{
		addStyle(style);
	}
	if (py::isinstance<py::list>(m_class))
	{
		for (auto &e : m_class)
		{
			style = pyDictGet(classcase, py::reinterpret_borrow<py::object>(e));
			if (!style.is_none())
			{
				addStyle(style);
			}
		}
	}
	else
	{
		style = pyDictGet(classcase, m_class);
		if (!style.is_none())
		{
			addStyle(style);
		}
	}
}

void View::applyStyle()
{
	pyobj style;

	style = getStyle(STYLE_BACKGROUND);
	if (style != None)
	{
		if (py::isinstance<py::str>(style))
		{
			setBackground(parseColor(style.cast<wxString>(), m_elem->GetBackgroundColour().GetRGB()));
		}
		else {
			setBackground(style.cast<int>());
		}
	}

	style = getStyle(STYLE_COLOR);
	if (style != None)
	{
		if (py::isinstance<py::str>(style))
		{
			setForeground(parseColor(style.cast<wxString>(), m_elem->GetForegroundColour().GetRGB()));
		}
		else {
			setForeground(style.cast<int>());
		}
	}

	style = getStyle(STYLE_FONTSIZE);
	if (style != None)
	{
		wxFont font = m_elem->GetFont();
		font.SetPointSize(style.cast<int>());
		m_elem->SetFont(font);
	}

	style = getStyle(STYLE_FONT);
	if (style != None)
	{
		wxFont font = m_elem->GetFont();

		// 字重
		wxcstr weightStr = pyDictGet(style, wxT("weight"), wxNoneString);
		if (weightStr != wxNoneString)
		{
			font.SetWeight(
				weightStr == wxT("normal") ? wxFONTWEIGHT_NORMAL :
				weightStr == wxT("light") ? wxFONTWEIGHT_LIGHT :
				weightStr == wxT("bold") ? wxFONTWEIGHT_BOLD :
				font.GetWeight()
			);
		}

		// 字体样式
		wxcstr styleStr = pyDictGet(style, wxT("style"), wxNoneString);
		if (styleStr != wxNoneString)
		{
			font.SetStyle(
				styleStr == wxT("normal") ? wxFONTSTYLE_NORMAL :
				styleStr == wxT("italic") ? wxFONTSTYLE_ITALIC :
				styleStr == wxT("slant") ? wxFONTSTYLE_SLANT :
				font.GetStyle()
			);
		}

		font.SetUnderlined(pyDictGet(style, wxT("underline"), false));
		font.SetFaceName(pyDictGet(style, wxT("face"), wxNoneString));

		m_elem->SetFont(font);
	}

	if (hasStyle(STYLE_MINWIDTH) || hasStyle(STYLE_MINHEIGHT))
	{
		wxSize size = m_elem->GetMinSize();
		style = getStyle(STYLE_MINWIDTH);
		if (style != None)
			size.SetWidth(style.cast<int>());
		style = getStyle(STYLE_MINHEIGHT);
		if (style != None)
			size.SetHeight(style.cast<int>());
		m_elem->SetMinSize(size);
	}

	if (hasStyle(STYLE_MAXWIDTH) || hasStyle(STYLE_MAXHEIGHT))
	{
		wxSize size = m_elem->GetMaxSize();
		style = getStyle(STYLE_MAXWIDTH);
		if (style != None)
			size.SetWidth(style.cast<int>());
		style = getStyle(STYLE_MAXHEIGHT);
		if (style != None)
			size.SetHeight(style.cast<int>());
		m_elem->SetMaxSize(size);
	}
}

void View::setContextMenu(ContextMenu & menu)
{
	m_elem->Bind(wxEVT_CONTEXT_MENU, &View::onPopMenu, this);
	m_elem->Bind(wxEVT_MENU, &View::onContextMenu, this);
	m_contextmenu = py::cast(menu);
}

void View::onPopMenu(wxContextMenuEvent & event)
{
	if (m_contextmenu)
	{
		m_elem->PopupMenu(py::cast<ContextMenu*>(m_contextmenu)->ptr());
	}
}

void View::onContextMenu(wxCommandEvent & event)
{
	if (m_contextmenu)
	{
		py::cast<ContextMenu*>(m_contextmenu)->onSelect(py::cast(this), event.GetId());
	}
}

Layout* View::getParent()
{
	auto elemParent = m_elem->GetParent();
	void *parent = elemParent ? (Layout*)elemParent->GetClientData() : nullptr;
	if (parent)
	{
		if (Item::isInstance(parent))
		{
			parent = ((Item*)parent)->getView();
		}
	}
	return (Layout*)parent;
}

bool View::handleEvent(wxEvent & event)
{
	py::object event_list = pyDictGet(m_event_table, py::int_(event.GetEventType()));

	py::object callback;
	py::object ret;

	if (!event_list.is_none())
	{
		for (auto e : event_list)
		{
			callback = py::reinterpret_borrow<py::object>(e);
			if (isPyDict(callback))
			{
				if (callback.contains("arg_event"))
				{
					ret = pyCall(callback["callback"], this, &event);
				}
			}
			else {
				ret = pyCall(callback, this);
			}
			if (!PyObject_IsTrue(ret.ptr()))
			{
				if (ret.ptr() == Py_False)
				{
					return false;
				}
				event.Skip();
			}
		}
	}
	return true;
}

void Layout::add(View & child) {
	m_children.append(py::cast(&child));
	child.applyStyle();
	doAdd(child);
}

pyobj Layout::__enter__() {
	LAYOUTS.push_back(this);
	m_elem->Freeze();

	if (tmp_styles_list == nullptr)
	{
		tmp_styles_list = new wxVector<PyObject*>;
	}
	
	Layout *parent = getParent();

	if (!parent)
	{
		void *data = m_elem->GetClientData();
		if (data != this)
		{
			// 大概率当前是AuiManager
			parent = (Layout *)data;
		}
	}

	bool only_self = false; // 父元素的临时列表还没释放，本次只要检查自己的
	if (parent && parent->tmp_styles_list)
	{
		for (auto e : *parent->tmp_styles_list)
		{
			tmp_styles_list->push_back(e);
		}
		only_self = true;
	}

	parent = this;
	while (parent) {
		if (!parent->m_styles.is_none())
		{
			if (py::isinstance<py::list>(parent->m_styles))
			{
				for (auto &e : parent->m_styles)
				{
					if (!e.is_none())
						tmp_styles_list->push_back(e.ptr());
				}
			}
			else if (!parent->m_styles.is_none())
			{
				tmp_styles_list->push_back(parent->m_styles.ptr());
			}
		}

		if (only_self)
			break;

		parent = parent->getParent();
	}

	return py::cast(this);
}

void Layout::__exit__(py::args & args) {
	LAYOUTS.pop_back();
	m_elem->Thaw();

	// 释放临时样式表
	delete tmp_styles_list;
	tmp_styles_list = nullptr;
}

void Layout::setStyles(pycref styles)
{
	m_styles = styles;

	if (!styles.is_none())
	{
		for (auto &child : m_children)
		{
			py::cast<View*>(child)->testStyles(styles);
		}
	}
	reLayout();
}

void Item::__init()
{
	m_view.ptr()->SetClientData(this);
	py::cast(this).inc_ref();

	Layout* pLayout = View::getActiveLayout();
	if (pLayout)
	{
		pLayout->doAdd(m_view);
	}
}
