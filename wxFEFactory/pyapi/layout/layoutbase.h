#pragma once
#include "../pyutils.h"
#include "../fefactory_api.h"
#include "../functions.h"
#include "utils/color.h"
#include "myapp.h"
#include "menu.h"
#include "drop.hpp"


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
	View(pycref key, pycref className, pycref style);

	View(wxWindow* elem)
		:View(None, None, None)
	{
		m_elem = elem;
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

	/**
	 * 在Layout的onAdd中__exit__先被调用，返回false将不被onAdd(child)
	 */
	bool beforeAdded()
	{
		if (!m_added)
		{
			m_added = true;
			return true;
		}
		return false;
	}

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

	View& setToolTip(wxcstr text)
	{
		m_elem->SetToolTip(text);
		return *this;
	}

	bool getEnabaled()
	{
		return ptr()->IsEnabled();
	}

	bool setEnabaled(bool enabled=true)
	{
		return ptr()->Enable(enabled);
	}

	wxString getLabel()
	{
		return m_elem->GetLabel();
	}

	void setLabel(wxcstr label)
	{
		m_elem->SetLabel(label);
	}

	View& show(bool show_)
	{
		ptr()->Show(show_);
		return *this;
	}

	bool isShow()
	{
		return ptr()->IsShown();
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

	Layout* getParent();

	operator wxWindow*()
	{
		return m_elem;
	}

	template <typename EventTag>
	void bindEvt(const EventTag& eventType, pycref fn)
	{
		if (!fn.is_none())
		{
			fn.inc_ref();
			((wxEvtHandler*)m_elem)->Bind(eventType, [fn, this](auto &event) {
				handleEvent(fn, event);
			});
		}
	}

	void handleEvent(pycref fn, wxEvent &event)
	{
		pycref ret = pyCall(fn, this);
		if (!PyObject_IsTrue(ret.ptr()))
		{
			event.Skip();
		}
	}

	template <typename EventType>
	void addPendingEvent(wxEventTypeTag<EventType> etype)
	{
		EventType event(etype, m_elem->GetId());
		m_elem->wxEvtHandler::AddPendingEvent(event);
	}

	/**
	 * 不推荐使用，现在不支持移除事件
	 * 会传wxKeyEvent实例过去，需要手动Skip
	 */
	void setOnKeyDown(pycref fn)
	{
		if (!fn.is_none())
		{
			fn.inc_ref();
			((wxEvtHandler*)m_elem)->Bind(wxEVT_KEY_DOWN, [fn, this](auto &event) {
				pyCall(fn, this, &event);
			});
		}
	}

	void setOnFileDrop(pycref ondrop)
	{
		m_elem->SetDropTarget(new FileDropListener(ondrop));
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

	void addStyle(pyobj style);

	pyobj getStyle(wxcstr key);

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

	bool hasStyle(pyobj &key);

	bool hasStyle(wxcstr key)
	{
		return hasStyle(py::str(key));
	}

	/**
	* 尝试应用样式表
	*/
	void testStyles(pycref styles);

	virtual void applyStyle();

	wxSize getStyleSize() {
		if (m_style.is_none())
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

	friend void init_layout(py::module &m);

protected:
	wxWindow *m_elem;
	pyobj m_style;
	pyobj m_key;
	pyobj m_class;
	pyobj m_contextmenu;
	bool m_added = false;

	static wxVector<Layout*> LAYOUTS;
};


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

	virtual void doAdd(View &child) {}

	virtual pyobj __enter__();

	virtual void __exit__(py::args &args);

	pyobj __getattr__(pyobj key)
	{
		return pyDictGet(m_named_children, key);
	}

	void setStyles(pycref styles);

	auto getStylesList()
	{
		return tmp_styles_list;
	}

	virtual void reLayout() {}

	void addNamed(pycref key, pycref child)
	{
		m_named_children[key] = child;
	}

	void removeChild(View &child)
	{
		m_elem->RemoveChild(child);
		m_children.attr("remove")(child);
	}

	View* findFocus()
	{
		auto pChild = m_elem->FindFocus();
		return pChild ? (View*)pChild->GetClientData() : nullptr;
	}

	friend void init_layout(py::module &m);
protected:
	py::list m_children;
	py::dict m_named_children;
	pyobj m_styles;
	wxVector<PyObject*> *tmp_styles_list;
};


class Item
{
public:
	Item(View &view, py::kwargs &kwargs) :
		m_view(view), m_kwargs(kwargs)
	{
	}

	void __init()
	{
		m_view.ptr()->SetClientData(this);
		py::cast(this).inc_ref();
	}

	View* getView()
	{
		return &m_view;
	}

	static bool isInstance(void *ptr)
	{

		return isPyDict(((Item*)ptr)->m_kwargs) && ((Item*)ptr)->m_view.ptr();
	}

	pyobj m_kwargs;
	View &m_view;
};