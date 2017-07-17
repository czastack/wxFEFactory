#pragma once
#include "pyutils.h"
#include "fefactory_api.h"
#include "functions.h"
#include "utils/color.h"
#include "myapp.h"


#define STYLE_WIDTH          wxT("width")
#define STYLE_HEIGHT         wxT("height")
#define STYLE_MAXWIDTH       wxT("maxWidth")
#define STYLE_MAXHEIGHT      wxT("maxHeight")
#define STYLE_MINWIDTH       wxT("minWidth")
#define STYLE_MINHEIGHT      wxT("minHeight")
#define STYLE_BACKGROUND     wxT("background")
#define STYLE_COLOR          wxT("color")
#define STYLE_FONTSIZE       wxT("fontSize")
#define STYLE_FONT           wxT("font")
#define STYLE_LEFT           wxT("left")
#define STYLE_RIGHT          wxT("right")
#define STYLE_BOTTOM         wxT("bottom")
#define STYLE_TOP            wxT("top")
#define STYLE_EXPAND         wxT("expand")
#define STYLE_FLEX           wxT("flex")
#define STYLE_PADDING        wxT("padding")
#define STYLE_SHOWPADDING    wxT("showPadding")
#define STYLE_ALIGN          wxT("align")
#define STYLE_VERTICALALIGN  wxT("verticalAlign")
#define STYLE_TEXTALIGN      wxT("textAlign")
#define STYLE_FLEXDIRECTION  wxT("flexDirection")

/**
styles {
	width,
	height,
	background,
	color,
	fontSize,
	left,
	right,
	bottom,
	top,
	margin,
	padding,
	flex,
	verticalAlign: ['top', 'bottom', 'center'],
	align: ['left', 'right', 'center'],
}
*/

class Layout;

class View
{
public:
	View(pycref key, pycref className, pycref style)
		:m_key(key), m_class(className), m_style(style)
	{

	}

	View(wxWindow* elem)
		:m_key(None), m_class(None), m_style(None), m_elem(elem)
	{

	}

	virtual ~View() {
		// py::print(m_key);
	}

	virtual void bindElem(wxWindow *pElem)
	{
		m_elem = pElem;
	}

	void __init()
	{
		m_elem->SetClientData(this);
		addToParent();
	}

	void addToParent();

	void setSize(int width, int height)
	{
		m_elem->SetSize(wxSize(width, height));
	}

	void setPosition(int left, int right)
	{
		m_elem->SetPosition(wxPoint(left, right));
	}

	void setForeground(uint rgb)
	{
		m_elem->SetForegroundColour(wxColor(rgb));
	}

	void setBackground(uint rgb)
	{
		m_elem->SetBackgroundColour(wxColor(rgb));
	}

	void setHelpText(wxcstr text)
	{
		m_elem->SetHelpText(text);
	}

	bool getEnabaled()
	{
		return ptr()->IsEnabled();
	}

	bool setEnabaled(bool enabled=true)
	{
		return ptr()->Enable(enabled);
	}

	void setContextMenu(ContextMenu &menu)
	{
		m_elem->Bind(wxEVT_CONTEXT_MENU, &View::onPopMenu, this);
		m_elem->Bind(wxEVT_MENU, &View::onContextMenu, this);
		m_contextmenu = py::cast(menu);
	}

	void onPopMenu(wxContextMenuEvent& event)
	{
		if (m_contextmenu)
		{
			m_elem->PopupMenu(py::cast<ContextMenu*>(m_contextmenu)->ptr());
		}
	}

	void onContextMenu(wxCommandEvent& event)
	{
		if (m_contextmenu)
		{
			py::cast<ContextMenu*>(m_contextmenu)->onSelect(py::cast(this), event.GetId());
		}
	}

	pyobj getTypeName() {
		pyobj self = py::cast(this);
		return py::getattr(self.get_type(), "__name__");
	}

	pycref getClassName()
	{
		return m_class;
	}

	pycref getKey()
	{
		return m_key;
	}

	Layout* getParent()
	{
		auto elemParent = m_elem->GetParent();
		return elemParent ? (Layout*)elemParent->GetClientData() : nullptr;
	}

	operator wxWindow*()
	{
		return m_elem;
	}

	template <typename EventTag>
	void bindEvt(const EventTag& eventType, pyobj &fn)
	{
		if (!fn.is_none())
		{
			fn.inc_ref();
			((wxEvtHandler*)m_elem)->Bind(eventType, [fn, this](auto event) {
				handlerEvent(fn, event);
			});
		}
	}

	template <typename EventType>
	void handlerEvent(pycref fn, EventType event)
	{
		pycref ret = pyCall(fn, py::cast(this));
		if (!PyObject_IsTrue(ret.ptr()))
		{
			event.Skip();
		}
	}

	static int parseColor(wxcstr color, uint defval = 0)
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

	static Layout* getActiveLayout()
	{
		return LAYOUTS.empty() ? nullptr : LAYOUTS.back();
	}

	static Layout* safeActiveLayout()
	{
		Layout *layout = getActiveLayout();
		if (!layout)
		{
			throw py::value_error("构造时出错，没有父元素");
		}
		return layout;
	}

	static wxWindow* safeActiveWindow();


	void setStyle(pyobj &style) {
		m_style = style;

		applyStyle();
		if (hasStyle(STYLE_WIDTH) || hasStyle(STYLE_HEIGHT))
		{
			applyStyleSize();
		}
	}

	void addStyle(pyobj style)
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

	pyobj getStyle(wxcstr key)
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

	template<class T>
	T getStyle(wxcstr key, T defval)
	{
		if (py::isinstance<py::list>(m_style))
		{
			pyobj &&ret = getStyle(key);
			return ret.is_none() ? defval : ret.cast<T>();
		}
		else
		{
			return pyDictGet(m_style, key, defval);
		}
	}

	bool hasStyle(pyobj &key)
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

	bool hasStyle(wxcstr key)
	{
		return hasStyle(py::str(key));
	}

	/**
	* 尝试应用样式表
	*/
	void testStyles(pyobj &typecase, pyobj &classcase)
	{
		pyobj style = pyDictGet(typecase, getTypeName());
		if (!style.is_none())
		{
			addStyle(style);
		}
		style = pyDictGet(classcase, getClassName());
		if (!style.is_none())
		{
			addStyle(style);
		}
	}

	virtual void applyStyle()
	{
		/*if (py::isinstance<py::list>(m_style))
		{
			for (auto &e : m_style)
			{
				applyStyle(py::reinterpret_borrow<py::object>(e));
			}
		}
		else
		{
			applyStyle(m_style);
		}*/

		pyobj style;

		style = getStyle(STYLE_BACKGROUND);
		if (style != None)
		{
			setBackground(parseColor(style.cast<wxString>(), m_elem->GetBackgroundColour().GetRGB()));
		}

		style = getStyle(STYLE_COLOR);
		if (style != None)
		{
			setForeground(parseColor(style.cast<wxString>(), m_elem->GetForegroundColour().GetRGB()));
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

	wxSize getStyleSize() {
		if (m_style == None)
		{
			return wxDefaultSize;
		}
		return wxSize(
			getStyle(STYLE_WIDTH, wxDefaultSize.GetWidth()),
			getStyle(STYLE_HEIGHT, wxDefaultSize.GetHeight())
		);
	}

	void applyStyleSize()
	{
		m_elem->SetSize(getStyleSize());
	}

	wxWindow *ptr()
	{
		return m_elem;
	}

	friend void initLayout(py::module &m);

protected:
	wxWindow *m_elem;
	pyobj m_style;
	pyobj m_key;
	pyobj m_class;
	pyobj m_contextmenu;

	static wxVector<Layout*> LAYOUTS;
};

wxVector<Layout*> View::LAYOUTS;


class Control : public View
{
public:
	using View::View;

private:
};


class Layout : public View
{
public:
	template <class... Args>
	Layout(pycref styles = None, Args ...args) : View(args...), m_styles(styles)
	{

	}

	Layout(Layout &proxyed) :
		View(proxyed.m_elem),
		m_children(proxyed.m_children), m_named_children(proxyed.m_named_children), m_styles(None)
	{

	}

	void add(View &child) {
		m_children.append(py::cast(&child));
	}

	virtual void onAdd(View &child) {}

	virtual pyobj __enter__() {
		LAYOUTS.push_back(this);
		return py::cast(this);
	}

	virtual void __exit__(py::args &args) {
		LAYOUTS.pop_back();

		// 检测样式表

		Layout *parent = this;
		wxVector<pyobj*> styles_list;
		while (parent) {
			if (!parent->m_styles.is_none())
			{
				styles_list.push_back(&parent->m_styles);
			}
			parent = parent->getParent();
		}
		auto it = styles_list.rbegin();
		while (it != styles_list.rend())
		{
			pyobj typecase = pyDictGet(**it, wxT("type"), None);
			pyobj classcase = pyDictGet(**it, wxT("class"), None);
			++it;

			for (auto &child : m_children)
			{
				py::cast<View*>(child)->testStyles(typecase, classcase);
			}
		}
		for (auto &e : m_children)
		{
			View &child = *py::cast<View*>(e);

			if (!child.getKey().is_none())
			{
				m_named_children[child.getKey()] = py::cast(&child);
			}
			child.applyStyle();
			onAdd(child);
		}
	}

	pyobj __getattr__(pyobj key)
	{
		return pyDictGet(m_named_children, key);
	}

	void setStyles(py::dict styles)
	{
		m_styles = styles;
		py::dict typecase = pyDictGet(styles, wxT("type"), None);
		py::dict classcase = pyDictGet(styles, wxT("class"), None);

		if (!typecase.is_none() || classcase.is_none())
		{
			for (auto &child : m_children)
			{
				py::cast<View*>(child)->testStyles(typecase, classcase);
			}
		}
		reLayout();
	}

	virtual void reLayout() {}

	void addNamed(pycref key, pycref child)
	{
		m_named_children[key] = child;
	}

	void removeChild(View &child)
	{
		m_elem->RemoveChild(child);
	}

	friend void initLayout(py::module &m);
protected:
	py::list m_children;
	py::dict m_named_children;
	pyobj m_styles;
};


void View::addToParent() {
	Layout* pLayout = getActiveLayout();
	if (pLayout)
	{
		pLayout->add(*this);
	}
}

wxWindow* View::safeActiveWindow()
{
	Layout *layout = getActiveLayout();
	return layout ? layout->ptr() : wxGetApp().GetTopWindow();
}