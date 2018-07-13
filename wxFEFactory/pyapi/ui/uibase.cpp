#include <wx/wx.h>
#include "uibase.h"
#include "drop.hpp"


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

void View::__init()
{
	m_elem->SetClientData(this);
	addToParent();
}

void View::addToParent() {
	Layout* pLayout = getActiveLayout();
	if (pLayout)
	{
		pLayout->add(*this);
	}
}

void View::setOnFileDrop(pycref ondrop)
{
	m_elem->SetDropTarget(new FileDropListener(ondrop));
}

void View::setOnTextDrop(pycref ondrop)
{
	m_elem->SetDropTarget(new TextDropListener(ondrop));
}

void View::startTextDrag(wxcstr text, pycref callback)
{
	wxTextDataObject data(text);
	wxDropSource dragSource(ptr(), wxDROP_ICON(dnd_copy),
		wxDROP_ICON(dnd_move),
		wxDROP_ICON(dnd_none));
	dragSource.SetData(data);
	wxDragResult result = dragSource.DoDragDrop(wxDrag_AllowMove);
	if (!callback.is_none()) {
		pyCall(callback, this, (int)result);
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
		pyobj pykey = py::str(key);
		PyObject* ret;

		for (auto &e : py::handle((PyObject*)&PyReversed_Type)(m_style))
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
			if (!e.is(None) && e.contains(key))
			{
				return true;
			}
		}

		return false;
	}
	return !m_style.is(None) && m_style.contains(key);
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
	if (!style.is(None))
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
	if (!style.is(None))
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
	if (!style.is(None))
	{
		wxFont font = m_elem->GetFont();
		font.SetPointSize(style.cast<int>());
		m_elem->SetFont(font);
	}

	style = getStyle(STYLE_FONT);
	if (!style.is(None))
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
		if (!style.is(None))
			size.SetWidth(style.cast<int>());
		style = getStyle(STYLE_MINHEIGHT);
		if (!style.is(None))
			size.SetHeight(style.cast<int>());
		m_elem->SetMinSize(size);
	}

	if (hasStyle(STYLE_MAXWIDTH) || hasStyle(STYLE_MAXHEIGHT))
	{
		wxSize size = m_elem->GetMaxSize();
		style = getStyle(STYLE_MAXWIDTH);
		if (!style.is(None))
			size.SetWidth(style.cast<int>());
		style = getStyle(STYLE_MAXHEIGHT);
		if (!style.is(None))
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

bool View::_bindEvt(int eventType, pycref fn, bool reset, bool pass_event)
{
	bool wxbind = false;
	if (!fn.is_none())
	{
		py::int_ eventKey((int)eventType);
		py::object event_list;

		if (m_event_table.contains(eventKey))
		{
			event_list = m_event_table[eventKey];

			if (reset)
			{
				event_list.attr("clear")();
			}
		}
		else
		{
			event_list = py::list();
			m_event_table[eventKey] = event_list;
			wxbind = true;
		}
		if (pass_event && !isPyDict(fn))
		{
			py::dict arg;
			arg["callback"] = fn;
			arg["arg_event"] = py::bool_(true);
			event_list.attr("append")(arg);
		}
		else {
			event_list.attr("append")(fn);
		}
	}
	return wxbind;
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
				if (pyDictGet(callback, "arg_event", false))
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
	m_children.append(&child);
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

void Layout::removeChild(View & child)
{
	m_elem->RemoveChild(child);
	m_children.attr("remove")(child);
}

void Layout::clearChildren()
{
	for (auto child: m_elem->GetChildren())
	{
		m_elem->RemoveChild(child);
	}
	m_children.attr("clear")();
}

View * Layout::findFocus()
{
	auto pChild = m_elem->FindFocus();
	return pChild ? (View*)pChild->GetClientData() : nullptr;
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


void init_uibase(py::module & m)
{
	using namespace py::literals;

	auto view = py::class_<View>(m, "View")
		.def("isShow", &View::isShow)
		.def("show", &View::show, "show"_a = true)
		.def("destroy", &View::destroy)
		.def("refresh", &View::refresh)
		.def("setToolTip", &View::setToolTip)
		.def("setContextMenu", &View::setContextMenu)
		.def("setOnKeyDown", &View::setOnKeyDown)
		.def("setOnFileDrop", &View::setOnFileDrop)
		.def("setOnTextDrop", &View::setOnTextDrop)
		.def("startTextDrag", &View::startTextDrag, "text"_a, "callback"_a=None)
		.def("setOnLeftDown", [](View &self, pycref fn) { self.bindEvt(wxEVT_LEFT_DOWN, fn, true, true); })
		.def("setOnLeftUp", [](View &self, pycref fn) { self.bindEvt(wxEVT_LEFT_UP, fn, true, true); })
		.def("setOnRightDown", [](View &self, pycref fn) { self.bindEvt(wxEVT_RIGHT_DOWN, fn, true, true); })
		.def("setOnRightUp", [](View &self, pycref fn) { self.bindEvt(wxEVT_RIGHT_UP, fn, true, true); })
		.def("setOnDoubleClick", [](View &self, pycref fn) { self.bindEvt(wxEVT_LEFT_DCLICK, fn, true, true); })
		.def("setOnDestroy", &View::setOnDestroy)
		.def("freeze", [](View &self) { return self.ptr()->Freeze(); })
		.def("thaw", [](View &self) { return self.ptr()->Thaw(); })
		.def_static("get_active_layout", &View::getActiveLayout)
		.def_readwrite("style", &View::m_style)
		.def_readwrite("className", &View::m_class)
		.def_property("enabled", &View::getEnabaled, &View::setEnabaled)
		.def_property("background", &View::getBackground, &View::setBackground)
		.def_property("color", &View::getForeground, &View::setForeground)
		.def_property("id",
			[](View &self) { return self.ptr()->GetId(); },
			[](View &self, int id) { self.ptr()->SetId(id); }
		)
		.def_property_readonly("parent", &View::getParent);

	py::class_<Control, View>(m, "Control");

	py::class_<Layout, View>(m, "Layout")
		.def("__enter__", &Layout::__enter__)
		.def("__exit__", &Layout::__exit__)
		.def("styles", &Layout::setStyles)
		.def("removeChild", &Layout::removeChild)
		.def("clearChildren", &Layout::clearChildren)
		.def("reLayout", &Layout::reLayout)
		.def("findFocus", &Layout::findFocus)
		.def_readonly("children", &Layout::m_children);
}