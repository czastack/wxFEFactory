#pragma once
#include "pyutils.h"
#include "fefactory_api.h"
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
		py::print(m_key);
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

	void setMaxSize(int width, int height)
	{
		m_elem->SetMaxSize(wxSize(width, height));
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

	bool hasStyle(pyobj &key)
	{
		if (py::isinstance<py::list>(m_style))
		{
			for (auto &e : m_style)
			{
				if (e.contains(key))
				{
					return true;
				}
			}

			return false;
		}
		return m_style.contains(key);
	}

	bool hasStyle(wxcstr key)
	{
		return hasStyle(py::str(key));
	}

	wxSize getStyleSize() {
		return wxSize(
			getStyle(STYLE_WIDTH, wxDefaultSize.GetWidth()),
			getStyle(STYLE_HEIGHT, wxDefaultSize.GetHeight())
		);
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

	void applyStyleSize()
	{
		m_elem->SetSize(getStyleSize());
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

	void applyStyle()
	{
		if (py::isinstance<py::list>(m_style))
		{
			for (auto &e : m_style)
			{
				applyStyle(py::reinterpret_borrow<py::object>(e));
			}
		}
		else
		{
			applyStyle(m_style);
		}
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

	static wxVector<Layout*> LAYOUTS;

	/**
	* 应用样式
	*/
	void applyStyle(pycref style)
	{
		if (style.is_none())
			return;

		for (auto &e : style)
		{
			wxcstr name = e.cast<wxString>();
			if (name == STYLE_BACKGROUND)
			{
				setBackground(parseColor(getStyle(STYLE_BACKGROUND, wxNoneString), m_elem->GetBackgroundColour().GetRGB()));
			}
			else if (name == STYLE_COLOR)
			{
				setForeground(parseColor(getStyle(STYLE_COLOR, wxNoneString), m_elem->GetForegroundColour().GetRGB()));
			}
			else if (name == STYLE_FONTSIZE)
			{
				wxFont font = m_elem->GetFont();
				font.SetPointSize(getStyle(STYLE_FONTSIZE, wxNORMAL_FONT->GetPointSize()));
				m_elem->SetFont(font);
			}
			else if (name == STYLE_FONT)
			{
				// 字体
				auto data = py::dict(getStyle(STYLE_FONT));
				wxFont font = m_elem->GetFont();

				// 字重
				wxcstr weightStr = pyDictGet(data, wxT("weight"), wxNoneString);
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
				wxcstr styleStr = pyDictGet(data, wxT("style"), wxNoneString);
				if (styleStr != wxNoneString)
				{
					font.SetStyle(
						styleStr == wxT("normal") ? wxFONTSTYLE_NORMAL :
						styleStr == wxT("italic") ? wxFONTSTYLE_ITALIC :
						styleStr == wxT("slant") ? wxFONTSTYLE_SLANT :
						font.GetStyle()
					);
				}

				font.SetUnderlined(pyDictGet(data, wxT("underline"), false));
				font.SetFaceName(pyDictGet(data, wxT("face"), wxNoneString));

				m_elem->SetFont(font);
			}
			else {
				applyStyle(name);
			}
		}
	}

	virtual bool applyStyle(wxcstr name)
	{
		return false;
	}
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

	virtual void reLayout()
	{

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