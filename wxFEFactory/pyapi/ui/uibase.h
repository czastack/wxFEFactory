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
protected:
	wxWindow *m_elem;
	pyobj m_style;
	pyobj m_class;
	pyobj m_contextmenu;
	py::dict m_event_table;

	static wxVector<Layout*> LAYOUTS;

public:
	View(pycref className, pycref style);

	View(wxWindow* elem) : View(None, None) { m_elem = elem; }

	virtual ~View();

	wxWindow *ptr() const
	{
		return m_elem;
	}

	virtual void bindElem(wxWindow *pElem)
	{
		m_elem = pElem;
	}

	void __init();

	void addToParent();

	void setForeground(uint rgb)
	{
		m_elem->SetForegroundColour(wxColor(rgb));
	}

	uint getForeground()
	{
		return m_elem->GetForegroundColour().GetRGB();
	}

	void setBackground(uint rgb)
	{
		m_elem->SetBackgroundColour(wxColor(rgb));
	}

	uint getBackground()
	{
		return m_elem->GetBackgroundColour().GetRGB();
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

	View& show(bool show_=true)
	{
		ptr()->Show(show_);
		return *this;
	}

	bool isShow()
	{
		return ptr()->IsShown();
	}

	void destroy()
	{
		ptr()->Destroy();
	}

	void setContextMenu(ContextMenu &menu);

	void onPopMenu(wxContextMenuEvent& event);

	void onContextMenu(wxCommandEvent& event);

	void refresh()
	{
		m_elem->Refresh();
	}

	pyobj getTypeName() {
		pyobj self = py::cast(this);
		return py::getattr(self.get_type(), "__name__");
	}

	pycref getClassName()
	{
		return m_class;
	}

	Layout* getParent();

	operator wxWindow*()
	{
		return m_elem;
	}

	bool hasEventHandler(const wxEvent& event)
	{
		py::int_ eventKey((int)event.GetEventType());
		return m_event_table.contains(eventKey);
	}

	/**
	 * pass_event 是否传递event实例作为callback参数
	 */
	template <typename EventTag>
	void bindEvt(const EventTag& eventType, pycref fn, bool reset = false, bool wxbind = true, bool pass_event = false);

	void handleEvent(pycref fn, wxEvent &event)
	{
		pycref ret = pyCall(fn, this);
		if (!PyObject_IsTrue(ret.ptr()))
		{
			event.Skip();
		}
	}

	bool handleEvent(wxEvent &event);

	void View::_handleEvent(wxEvent & event) { handleEvent(event); }

	template <typename EventTag>
	void removeEvt(const EventTag& eventType, pycref fn)
	{
		py::object event_list = pyDictGet(m_event_table, py::int_((int)eventType));

		if (!event_list.is_none())
		{
			event_list.attr("remove")(fn);
		}
	}

	template <typename EventType>
	void addPendingEvent(wxEventTypeTag<EventType> etype)
	{
		EventType event(etype, m_elem->GetId());
		m_elem->wxEvtHandler::AddPendingEvent(event);
	}

	/**
	 * 会传wxKeyEvent实例过去，需要手动Skip
	 */
	void setOnKeyDown(pycref fn)
	{
		bindEvt(wxEVT_KEY_DOWN, fn, false, true, true);
	}

	void setOnFileDrop(pycref ondrop)
	{
		m_elem->SetDropTarget(new FileDropListener(ondrop));
	}

	void setOnTextDrop(pycref ondrop)
	{
		m_elem->SetDropTarget(new TextDropListener(ondrop));
	}

	void setOnDoubleClick(pycref fn)
	{
		bindEvt(wxEVT_LEFT_DCLICK, fn);
	}

	void setOnClick(pycref fn)
	{
		bindEvt(wxEVT_LEFT_DOWN, fn);
	}

	void setOnDestroy(pycref fn)
	{
		bindEvt(wxEVT_DESTROY, fn);
	}

	static int parseColor(wxcstr color, uint defval = 0);

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

	static wxWindow* getActiveWindow();

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

	friend void init_layout(py::module &m);
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
	Layout(pycref styles = None, Args ...args) : View(args...), m_styles(styles), tmp_styles_list(nullptr)
	{

	}

	Layout(Layout &proxyed) :
		View(proxyed.m_elem),
		m_children(proxyed.m_children), m_styles(None),
		tmp_styles_list(nullptr)
	{

	}

	virtual ~Layout() {
		m_children.attr("clear")();
		m_children.release();
	}

	void add(View &child);

	virtual void doAdd(View &child) {}

	virtual pyobj __enter__();

	virtual void __exit__(py::args &args);

	void setStyles(pycref styles);

	auto getStylesList()
	{
		return tmp_styles_list;
	}

	virtual void reLayout() {}

	void removeChild(View &child);

	void clearChildren();

	View* findFocus();

	friend void init_layout(py::module &m);
protected:
	py::list m_children;
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

	void __init();

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


template<typename EventTag>
void View::bindEvt(const EventTag & eventType, pycref fn, bool reset, bool wxbind, bool pass_event)
{
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

			if (wxbind)
			{
				((wxEvtHandler*)m_elem)->Bind(eventType, &View::_handleEvent, this);
			}
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
}
