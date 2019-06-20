#include <wx/wx.h>
#include <wx/aui/auibook.h>
#include <wx/button.h>
#include <wx/clrpicker.h>
#include <wx/event.h>
#include <wx/filepicker.h>
#include <wx/listbase.h>
#include <wx/listbook.h>
#include <wx/mdi.h>
#include <wx/propgrid/propgrid.h>
#include <wx/rearrangectrl.h>
#include <wx/spinctrl.h>
#include <wx/splitter.h>
#include <wx/srchctrl.h>
#include <wx/statline.h>
#include <wx/stattext.h>
#include <wx/textctrl.h>
#include <wx/tglbtn.h>
#include <wx/treectrl.h>
#include "../pyutils.h"
#include "../functions.h"



class PyFunctor
{
public:
	PyFunctor(pycref fn) : fn(fn) {};

	void operator()(wxEvent& event) {
		PyCall(fn, event);
	}

	pyobj fn;
};


/**
 * Ñ¡Ïî×ª»»
 */
class ChoicesCaster
{
public:
	static wxArrayString getChoices(pycref choices);

	static void start_cache()
	{
		m_choices_cache_on = true;
	}

	static void end_cache()
	{
		m_choices_cache_on = false;
		m_choices_cache.clear();
	}
protected:
	static std::unordered_map<PyObject*, wxArrayString> m_choices_cache;
	static bool m_choices_cache_on;
};

std::unordered_map<PyObject*, wxArrayString> ChoicesCaster::m_choices_cache;
bool ChoicesCaster::m_choices_cache_on = false;

wxArrayString ChoicesCaster::getChoices(pycref choices)
{
	if (m_choices_cache_on) {
		auto it = m_choices_cache.find(choices.ptr());
		if (it != m_choices_cache.end())
		{
			return it->second;
		}
		wxArrayString &array = m_choices_cache.emplace(std::pair<PyObject*, wxArrayString>(choices.ptr(), {})).first->second;
		wxArrayAddAll(array, choices);
		return array;
	}
	else
	{
		return py::cast<wxArrayString>(choices);
	}
}


namespace pybind11 {
	namespace detail {

		// wxSize
		template <> class type_caster<wxSize> {
		public:
			bool load(handle src, bool) {
				auto temp = py::sequence(src, true);
				value.x = temp[0].cast<int>();
				value.y = temp[1].cast<int>();
				return true;
			}

			static handle cast(const wxSize& src, return_value_policy /* policy */, handle /* parent */) {
				py::tuple result(2);
				result[0] = src.x;
				result[0] = src.y;
				return result;
			}

			PYBIND11_TYPE_CASTER(wxSize, (_)("wxSize"));
		protected:
			bool success = false;
		};

		// PyFunctor
		template <> class type_caster<PyFunctor> {
		public:
			bool load(handle src, bool) {
				value.fn = reinterpret_steal<object>(src);
				return true;
			}

			static handle cast(const PyFunctor& src, return_value_policy /* policy */, handle /* parent */) {
				return src.fn;
			}

			PYBIND11_TYPE_CASTER(PyFunctor, (_)("PyFunctor"));
		protected:
			bool success = false;
		};
	}
}

void init_ui(py::module& m)
{
	using namespace py::literals;
	auto wx = m.ptr();

	auto parent = "parent"_a;
	auto id = "id"_a;
	auto label = "label"_a = wxEmptyString;
	auto pos = "pos"_a = wxDefaultPosition;
	auto size = "size"_a = wxDefaultSize;
	auto style = "style"_a;
	auto style_0 = style = 0;
	auto validator = "validator"_a = wxDefaultValidator;
	auto name = "name"_a;

	auto event = "event"_a;
	auto value = "value"_a;
	auto text = "text"_a;
	auto title = "title"_a;
	auto show = "show"_a;

	auto item = "item"_a;
	auto items = "items"_a;
	auto choices = "choices"_a;
	auto pos = "pos"_a;

	auto window = "window"_a;

	py::class_<wxSize>(m, "Size")
		.def(py::init<>())
		.def(py::init<int, int>(), "x"_a, "y"_a)
		.def_readwrite("x", &wxSize::x)
		.def_readwrite("y", &wxSize::y);

	py::class_<wxPoint>(m, "Point")
		.def(py::init<>())
		.def(py::init<int, int>(), "x"_a, "y"_a)
		.def_readwrite("x", &wxPoint::x)
		.def_readwrite("y", &wxPoint::y);

	py::class_<wxArrayInt>(m, "ArrayInt");

	// wxWindow

#define WINDOW_INIT_STYLE(style, _name) def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),\
	parent, id, pos, size, style, name=_name)
#define WINDOW_INIT(_name) WINDOW_INIT_STYLE(style_0, _name)

	py::class_<wxWindow>(m, "Window")
		.def(py::init<>())
		.WINDOW_INIT(wxPanelNameStr)
		.def("GetForegroundColour", &wxWindow::GetForegroundColour)
		.def("SetForegroundColour", &wxWindow::SetForegroundColour, "color"_a)
		.def("GetBackgroundColour", &wxWindow::GetBackgroundColour)
		.def("SetBackgroundColour", &wxWindow::SetBackgroundColour, "color"_a)
		.def("GetWindowStyle", &wxWindow::GetWindowStyle)
		.def("SetWindowStyle", &wxWindow::SetWindowStyle, style)
		.def("GetSize", (wxSize (wxWindow::*)() const) &wxWindow::GetSize)
		.def("SetSize", (void (wxWindow::*)(int width, int height)) &wxWindow::SetSize, "width"_a, "height"_a)
		.def("GetSizer", &wxWindow::GetSizer)
		.def("SetSizer", &wxWindow::SetSizer, "sizer"_a, "deleteOld"_a=true)
		.def("GetId", &wxWindow::GetId)
		.def("SetId", &wxWindow::SetId, "winid"_a)
		.def("GetClientData", &wxWindow::GetClientData)
		.def("SetClientData", &wxWindow::SetClientData, "data"_a)
		.def("Layout", &wxWindow::Layout)
		.def("Bind", (void (wxWindow::*)(const wxEventType&, const PyFunctor&, int winid, int lastId, wxObject * userData)) &wxWindow::Bind,
			"eventType"_a, "fn"_a, "winid"_a=wxID_ANY, "lastId"_a=wxID_ANY, "userData"_a=NULL)
		.def("AddPendingEvent", &wxWindow::AddPendingEvent, "event"_a)
		.def("GetHost", [](wxWindow *self) -> py::object {
			PyObject *ptr = reinterpret_cast<PyObject*>(self->GetClientData());
			if (ptr) {
				return py::reinterpret_borrow<py::object>(ptr);
			}
			return None;
		})
		.def("SetHost", [](wxWindow *self, pycref host) {
			self->SetClientData(host.ptr());
		}, "host"_a)
		;

	// controls

#define STATIC_CONTROL_INIT(ext_t, ext_a, _name) def(py::init<wxWindow*, wxWindowID, ext_t, const wxPoint&, const wxSize&, long, const wxString&>(),\
	parent, id, ext_a, pos, size, style_0, name = _name)
#define CONTROL_INIT(ext_t, ext_a, _name) def(py::init<wxWindow*, wxWindowID, ext_t, const wxPoint&, const wxSize&, long, const wxValidator&, const wxString&>(),\
	parent, id, ext_a, pos, size, style_0, validator, name = _name)

#define GROUP(x) x

	// py::class_<wxControl, wxWindow>(m, "Control");

	py::class_<wxButton, wxWindow>(m, "Button")
		.CONTROL_INIT(const wxString&, label, wxButtonNameStr);

	py::class_<wxBitmapButton, wxButton>(m, "BitmapButton")
		.CONTROL_INIT(const wxBitmap&, label, wxButtonNameStr);

	py::class_<wxToggleButton, wxWindow>(m, "ToggleButton")
		.CONTROL_INIT(const wxString&, label, wxCheckBoxNameStr)
		.def("GetValue", &wxToggleButton::GetValue)
		.def("SetValue", &wxToggleButton::SetValue, value);

	py::class_<wxStaticBitmap, wxWindow>(m, "StaticBitmap")
		.STATIC_CONTROL_INIT(const wxGDIImage&, label, wxStaticBitmapNameStr);

	py::class_<wxStaticText, wxWindow>(m, "StaticText")
		.STATIC_CONTROL_INIT(const wxString&, label, wxStaticTextNameStr);

	py::class_<wxStaticLine, wxWindow>(m, "StaticLine")
		.WINDOW_INIT(wxStaticLineNameStr);

	// py::class_<wxTextEntry>(m, "TextEntry");

	py::class_<wxTextCtrl, wxWindow>(m, "TextCtrl")
		.CONTROL_INIT(const wxString&, value=wxEmptyString, wxTextCtrlNameStr)
		.def("GetValue", &wxTextCtrl::GetValue)
		.def("SetValue", &wxTextCtrl::SetValue, value)
		.def("AppendText", &wxTextCtrl::AppendText, text)
		.def("WriteText", &wxTextCtrl::WriteText, text)
		.def("Clear", &wxTextCtrl::Clear)
		.def("SelectAll", &wxTextCtrl::SelectAll)
		.def("GetSelection", [](wxTextCtrl *self) {
			long from, to;
			py::tuple result(2);
			self->GetSelection(&from, &to);
			result[0] = from;
			result[1] = to;
			return result;
		})
		.def("SetSelection", &wxTextCtrl::SetSelection)
		;

	py::class_<wxSearchCtrl, wxWindow>(m, "SearchCtrl")
		.CONTROL_INIT(const wxString&, value=wxEmptyString, wxSearchCtrlNameStr)
		.def("ShowSearchButton", &wxSearchCtrl::ShowSearchButton, show=true)
		.def("ShowCancelButton", &wxSearchCtrl::ShowCancelButton, show=true)
		.def("GetValue", &wxSearchCtrl::GetValue)
		.def("SetValue", &wxSearchCtrl::SetValue, value)
		;

	py::class_<wxSpinCtrl, wxWindow>(m, "SpinCtrl")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, int, int, int, const wxString&>(),
			parent, id, value, pos, size, style=wxSP_ARROW_KEYS, "min"_a, "max"_a=100, "initial"_a=0, name=wxT("wxSpinCtrl"))
		;

	py::class_<wxColourPickerCtrl, wxWindow>(m, "ColourPickerCtrl")
		.CONTROL_INIT(const wxColour&, "col"_a=*wxBLACK, wxColourPickerCtrlNameStr)
		.def("GetColour", &wxColourPickerCtrl::GetColour)
		.def("SetColour", (void (wxColourPickerCtrl::*)(const wxColour& col)) &wxColourPickerCtrl::SetColour, "col"_a)
		;

	py::class_<wxItemContainerImmutable, >(m, "ItemContainerImmutable")
		.def("GetSelection", &wxItemContainerImmutable::GetSelection)
		.def("SetSelection", &wxItemContainerImmutable::SetSelection, "n"_a)
		.def("GetCount", &wxItemContainerImmutable::GetCount)
		.def("GetString", &wxItemContainerImmutable::GetString, "n"_a)
		.def("SetString", &wxItemContainerImmutable::SetString, "n"_a, "s"_a)
		;

	py::class_<wxItemContainer, wxItemContainerImmutable>(m, "ItemContainer")
		.def("Append", (int (wxItemContainer::*)(const wxString &item)) &wxItemContainer::Append, item)
		.def("Append", (int (wxItemContainer::*)(const wxArrayString &item)) &wxItemContainer::Append, items)
		.def("Insert", (int (wxItemContainer::*)(const wxString &item, unsigned int pos)) &wxItemContainer::Insert, item, pos)
		.def("Insert", (int (wxItemContainer::*)(const wxArrayString &items, unsigned int pos)) &wxItemContainer::Insert, item, pos)
		.def("Set", (void (wxItemContainer::*)(const wxArrayString &items)) &wxItemContainer::Set, item)
		.def("Clear", &wxItemContainer::Clear)
		.def("Delete", &wxItemContainer::Delete)
		;

	py::class_<wxControlWithItems, wxControl, wxItemContainer>(m, "ControlWithItems")
		;

	py::class_<wxListBox, wxControlWithItems>(m, "ListBox")
		.CONTROL_INIT(const wxArrayString&, choices, wxListBoxNameStr)
		;

	py::class_<wxCheckListBox, wxListBox>(m, "CheckListBox")
		.def("IsChecked", &wxCheckListBox::IsChecked, item)
		.def("Check", &wxCheckListBox::Check, item, "check"_a=true)
		.def("GetCheckedItems", &wxCheckListBox::GetCheckedItems)
		;

	py::class_<wxRearrangeList, wxCheckListBox>(m, "RearrangeList")
		.CONTROL_INIT(GROUP(const wxArrayInt&, const wxArrayString&), GROUP("order"_a, items), wxRearrangeListNameStr)
	;

	py::class_<wxChoice, wxControlWithItems>(m, "Choice")
		.CONTROL_INIT(const wxArrayString&, choices, wxChoiceNameStr)
		;

	py::class_<wxComboBox, wxControlWithItems>(m, "ComboBox")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, const wxArrayString&, long, const wxValidator&, const wxString&>(),
			parent, id, value, pos, size, choices, style_0, validator, name=wxComboBoxNameStr)
		.def("GetValue", &wxComboBox::GetValue)
		.def("SetValue", &wxComboBox::SetValue, value)
		.def("AutoComplete", (bool (wxComboBox::*)(const wxArrayString &choices)) &wxComboBox::AutoComplete, choices)
		;

	py::class_<wxRadioBox, wxItemContainerImmutable>(m, "RadioBox")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, const wxArrayString&, int, long, const wxValidator&, const wxString&>(),
			parent, id, title, pos, size, choices, "majorDim"_a=0, style=wxRA_SPECIFY_COLS, validator, name=wxRadioBoxNameStr)
		;

	// containers
	py::class_<wxSizer, wxWindow>(m, "Sizer")
		.def(py::init<>())
		.def("Add", (wxSizerItem* (wxSizer::*)(wxWindow *, int, int, int, wxObject*)) &wxSizer::Add,
			window, "proportion"_a = 0, "flag"_a = 0, "border"_a = 0, "userData"_a = NULL)
		.def("Add", (wxSizerItem* (wxSizer::*)(wxSizerItem *)) &wxSizer::Add, "item"_a)
		.def("InsertSpacer", &wxSizer::InsertSpacer, "index"_a, "size"_a)
		.def("Layout", &wxSizer::Layout)
		.def("FitInside", &wxSizer::FitInside, window);

	py::class_<wxSizerItem>(m, "SizerItem")
		.def(py::init<wxWindow *, int, int, int, wxObject*>(),
			window, "proportion"_a = 0, "flag"_a = 0, "border"_a = 0, "userData"_a = NULL)
		.def(py::init<wxSizer *, int, int, int, wxObject*>(),
			"sizer"_a, "proportion"_a = 0, "flag"_a = 0, "border"_a = 0, "userData"_a = NULL)
		.def(py::init<int, int, int, int, int, wxObject*>(),
			"width"_a, "height"_a, "proportion"_a = 0, "flag"_a = 0, "border"_a = 0, "userData"_a = NULL)
		;

	py::class_<wxBoxSizer, wxSizer>(m, "BoxSizer")
		.def(py::init<int>(), "orient"_a = NULL);

	py::class_<wxGridSizer, wxSizer>(m, "GridSizer")
		.def(py::init<int, int, int>(), "cols"_a, "vgap"_a, "hgap"_a)
		.def(py::init<int, int, int, int>(), "rows"_a, "cols"_a, "vgap"_a, "hgap"_a);

	py::class_<wxFlexGridSizer, wxGridSizer>(m, "FlexGridSizer")
		.def(py::init<int, int, int>(), "cols"_a, "vgap"_a, "hgap"_a)
		.def(py::init<int, int, int, int>(), "rows"_a, "cols"_a, "vgap"_a, "hgap"_a)
		.def("AddGrowableRow", &wxFlexGridSizer::AddGrowableRow, "idx"_a, "proportion"_a = 0)
		.def("RemoveGrowableRow", &wxFlexGridSizer::RemoveGrowableRow, "idx"_a)
		.def("AddGrowableCol", &wxFlexGridSizer::AddGrowableCol, "idx"_a, "proportion"_a = 0)
		.def("RemoveGrowableCol", &wxFlexGridSizer::RemoveGrowableCol, "idx"_a)
		.def("GetFlexibleDirection", &wxFlexGridSizer::GetFlexibleDirection, "direction"_a)
		.def("SetFlexibleDirection", &wxFlexGridSizer::SetFlexibleDirection)
		;

	py::class_<wxPanel, wxWindow>(m, "Panel")
		.WINDOW_INIT_STYLE(style=wxTAB_TRAVERSAL | wxNO_BORDER, wxPanelNameStr);

	py::class_<wxStaticBox, wxWindow>(m, "StaticBox")
		.STATIC_CONTROL_INIT(const wxString&, label, wxStaticBoxNameStr);

	py::class_<wxScrolledWindow, wxWindow>(m, "ScrolledWindow")
		.WINDOW_INIT_STYLE(style=wxScrolledWindowStyle, wxPanelNameStr)
		.def("SetScrollRate", &wxScrolledWindow::SetScrollRate, "xstep"_a, "ystep"_a);

	py::class_<wxSplitterWindow, wxWindow>(m, "SplitterWindow")
		.WINDOW_INIT_STYLE(style=wxSP_3D, wxT("splitter"))
		.def("Initialize", &wxSplitterWindow::Initialize, window)
		.def("SplitHorizontally", &wxSplitterWindow::SplitHorizontally, "window1"_a, "window2"_a, "sashPosition"_a = 0)
		.def("SplitVertically", &wxSplitterWindow::SplitVertically, "window1"_a, "window2"_a, "sashPosition"_a = 0);

	py::class_<wxBookCtrlBase, wxWindow>(m, "BookCtrlBase")
		.def("AddPage", &wxBookCtrlBase::AddPage, "page"_a, text, "bSelect"_a=false, "imageId"_a=-1)
		.def("GetPageCount", &wxBookCtrlBase::GetPageCount)
		.def("GetSelection", &wxBookCtrlBase::GetSelection)
		.def("SetSelection", &wxBookCtrlBase::SetSelection, "n"_a)
		.def("SetPageText", &wxBookCtrlBase::SetPageText, "n"_a, text)
		.def("GetPageText", &wxBookCtrlBase::GetPageText, "n"_a);

	py::class_<wxNotebook, wxWindow>(m, "Notebook")
		.WINDOW_INIT(wxNotebookNameStr);





	// evnents
#define EVENT_TYPE(name) PyObject_SetAttrString(wx, #name, PyLong_FromLong(wx##name.operator const wxEventType& ()))
	// Command events
	EVENT_TYPE(EVT_BUTTON);
	EVENT_TYPE(EVT_CHECKBOX);
	EVENT_TYPE(EVT_CHOICE);
	EVENT_TYPE(EVT_LISTBOX);
	EVENT_TYPE(EVT_LISTBOX_DCLICK);
	EVENT_TYPE(EVT_CHECKLISTBOX);
	EVENT_TYPE(EVT_MENU);
	EVENT_TYPE(EVT_SLIDER);
	EVENT_TYPE(EVT_RADIOBOX);
	EVENT_TYPE(EVT_RADIOBUTTON);

	// Used
	EVENT_TYPE(EVT_AUINOTEBOOK_PAGE_CHANGED);
	EVENT_TYPE(EVT_AUINOTEBOOK_PAGE_CLOSE);
	EVENT_TYPE(EVT_BUTTON);
	EVENT_TYPE(EVT_CHAR);
	EVENT_TYPE(EVT_CHECKBOX);
	EVENT_TYPE(EVT_CHOICE);
	EVENT_TYPE(EVT_CLOSE_WINDOW);
	EVENT_TYPE(EVT_COLOURPICKER_CHANGED);
	EVENT_TYPE(EVT_COMBOBOX);
	EVENT_TYPE(EVT_COMBOBOX_DROPDOWN);
	EVENT_TYPE(EVT_COMMAND_TOOL_CLICKED);
	EVENT_TYPE(EVT_CONTEXT_MENU);
	EVENT_TYPE(EVT_DESTROY);
	EVENT_TYPE(EVT_DIRPICKER_CHANGED);
	EVENT_TYPE(EVT_FILEPICKER_CHANGED);
	EVENT_TYPE(EVT_HOTKEY);
	EVENT_TYPE(EVT_KEY_DOWN);
	EVENT_TYPE(EVT_LEFT_DCLICK);
	EVENT_TYPE(EVT_LEFT_DOWN);
	EVENT_TYPE(EVT_LEFT_UP);
	EVENT_TYPE(EVT_LIST_COL_CLICK);
	EVENT_TYPE(EVT_LIST_COL_RIGHT_CLICK);
	EVENT_TYPE(EVT_LIST_ITEM_ACTIVATED);
	EVENT_TYPE(EVT_LIST_ITEM_CHECKED);
	EVENT_TYPE(EVT_LIST_ITEM_DESELECTED);
	EVENT_TYPE(EVT_LIST_ITEM_SELECTED);
	EVENT_TYPE(EVT_LIST_ITEM_UNCHECKED);
	EVENT_TYPE(EVT_LISTBOOK_PAGE_CHANGED);
	EVENT_TYPE(EVT_LISTBOX);
	EVENT_TYPE(EVT_MENU);
	EVENT_TYPE(EVT_NOTEBOOK_PAGE_CHANGED);
	EVENT_TYPE(EVT_PG_CHANGING);
	EVENT_TYPE(EVT_PG_HIGHLIGHTED);
	EVENT_TYPE(EVT_PG_SELECTED);
	EVENT_TYPE(EVT_RADIOBOX);
	EVENT_TYPE(EVT_RIGHT_DOWN);
	EVENT_TYPE(EVT_RIGHT_UP);
	EVENT_TYPE(EVT_SEARCH_CANCEL);
	EVENT_TYPE(EVT_SEARCH);
	EVENT_TYPE(EVT_SPINCTRL);
	EVENT_TYPE(EVT_TEXT);
	EVENT_TYPE(EVT_TEXT_ENTER);
	EVENT_TYPE(EVT_TEXT_PASTE);
	EVENT_TYPE(EVT_TOGGLEBUTTON);
	EVENT_TYPE(EVT_TREE_ITEM_ACTIVATED);
}