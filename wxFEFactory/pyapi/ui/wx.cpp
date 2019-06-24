#include <wx/wx.h>
#include <wx/aui/aui.h>
#include <wx/aui/auibook.h>
#include "wx/aui/auibar.h"
#include <wx/aui/tabmdi.h>
#include <wx/button.h>
#include <wx/clrpicker.h>
#include <wx/event.h>
#include <wx/filepicker.h>
#include <wx/listbase.h>
#include <wx/listbook.h>
#include <wx/listctrl.h>
#include <wx/mdi.h>
#include <wx/menu.h>
#include <wx/propgrid/propgrid.h>
#include <wx/propgrid/property.h>
#include <wx/rearrangectrl.h>
#include <wx/spinctrl.h>
#include <wx/splitter.h>
#include <wx/srchctrl.h>
#include <wx/statline.h>
#include <wx/stattext.h>
#include <wx/textctrl.h>
#include <wx/tglbtn.h>
#include <wx/toolbar.h>
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
 * 选项转换
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
		/*template <> class type_caster<wxSize> {
		public:
			bool load(handle src, bool) {
				auto temp = py::reinterpret_borrow<sequence>(src);
				value.x = temp[0].cast<int>();
				value.y = temp[1].cast<int>();
				return true;
			}

			static handle cast(const wxSize& src, return_value_policy, handle) {
				py::tuple result(2);
				result[0] = src.x;
				result[0] = src.y;
				return result;
			}

			PYBIND11_TYPE_CASTER(wxSize, (_)("wxSize"));
		protected:
			bool success = false;
		};*/

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


		/**
		 * wxTreeItemId
		 */
		template <> class type_caster<wxTreeItemId> {
		public:
			bool load(handle src, bool) {
				value.m_pItem = (void*)(size_t)src.cast<pybind11::int_>();
				return true;
			}

			static handle cast(const wxTreeItemId &src, return_value_policy /* policy */, handle /* parent */) {
				return PyLong_FromUnsignedLongLong((size_t)src.GetID());
			}

			PYBIND11_TYPE_CASTER(wxTreeItemId, (_)("wxTreeItemId"));
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

	py::class_<wxFont>(m, "Point")
		.def(py::init<>())
		.def("SetWeight", (void (wxFont::*)(wxFontWeight)) &wxFont::SetWeight)
		.def("SetStyle", (void (wxFont::*)(wxFontStyle)) &wxFont::SetStyle)
		.def("SetUnderlined", &wxFont::SetUnderlined)
		.def("SetFaceName", &wxFont::SetFaceName)
		.def("SetPointSize", &wxFont::SetPointSize)
		;

	py::class_<wxArrayInt>(m, "ArrayInt");

	// wxWindow
#define PACK(...) __VA_ARGS__

#define _WINDOW_INIT(_ext_t, _ext_a, _ext_t1, _ext_a2, _style, _name) \
	def(py::init<wxWindow*, wxWindowID, _ext_t const wxPoint&, const wxSize&, long, _ext_t1 const wxString&>(),\
		parent, id, _ext_a pos, size, _style, _ext_a2 name=_name)
#define WINDOW_INIT_STYLE(_style, _name) _WINDOW_INIT(, , , , _style, _name)
#define WINDOW_INIT_EXT(ext_t, ext_a, _style, _name) _WINDOW_INIT(PACK(ext_t,), PACK(ext_a,), , , _style, _name)
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
		.def("GetFont", &wxWindow::GetFont)
		.def("SetFont", &wxWindow::SetFont, "font"_a)
		.def("GetId", &wxWindow::GetId)
		.def("SetId", &wxWindow::SetId, "winid"_a)
		.def("Show", &wxWindow::Show)
		.def("Hide", &wxWindow::Hide)
		.def("Reparent", &wxWindow::Reparent)
		.def("GetClientData", &wxWindow::GetClientData)
		.def("SetClientData", &wxWindow::SetClientData, "data"_a)
		.def("Layout", &wxWindow::Layout)
		// .def("Bind", (void (wxWindow::*)(const wxEventTypeTag<wxCommandEvent>&, const PyFunctor&, int winid, int lastId, wxObject * userData)) &wxWindow::Bind,
		//	"eventType"_a, "fn"_a, "winid"_a=wxID_ANY, "lastId"_a=wxID_ANY, "userData"_a=NULL)
		.def("AddPendingEvent", &wxWindow::wxEvtHandler::AddPendingEvent, "event"_a)
		.def("RegisterHotKey", &wxWindow::RegisterHotKey, "hotkeyId"_a, "modifiers"_a, "keycode"_a)
		.def("UnregisterHotKey", &wxWindow::UnregisterHotKey, "hotkeyId"_a)
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

#define STATIC_CONTROL_INIT(ext_t, ext_a, _name) WINDOW_INIT_EXT(ext_t, ext_a, style_0, _name)
#define CONTROL_INIT_STYLE(ext_t, ext_a, _style, _name) \
	_WINDOW_INIT(PACK(ext_t,), PACK(ext_a,), PACK(const wxValidator&,), PACK(validator,), _style, _name)
#define CONTROL_INIT_SIMPLE(_style, _name) _WINDOW_INIT(, , PACK(const wxValidator&,), PACK(validator,), _style, _name)
#define CONTROL_INIT(ext_t, ext_a, _name) CONTROL_INIT_STYLE(ext_t, ext_a, style_0, _name)

	py::class_<wxControl, wxWindow>(m, "Control");

	py::class_<wxButton, wxControl>(m, "Button")
		.CONTROL_INIT(const wxString&, label, wxButtonNameStr);

	py::class_<wxBitmapButton, wxButton>(m, "BitmapButton")
		.CONTROL_INIT(const wxBitmap&, label, wxButtonNameStr);

	py::class_<wxToggleButton, wxControl>(m, "ToggleButton")
		.CONTROL_INIT(const wxString&, label, wxCheckBoxNameStr)
		.def("GetValue", &wxToggleButton::GetValue)
		.def("SetValue", &wxToggleButton::SetValue, value);

	py::class_<wxStaticBitmap, wxControl>(m, "StaticBitmap")
		.STATIC_CONTROL_INIT(const wxGDIImage&, label, wxStaticBitmapNameStr);

	py::class_<wxStaticText, wxControl>(m, "StaticText")
		.STATIC_CONTROL_INIT(const wxString&, label, wxStaticTextNameStr);

	py::class_<wxStaticLine, wxControl>(m, "StaticLine")
		.WINDOW_INIT(wxStaticLineNameStr);

	// py::class_<wxTextEntry>(m, "TextEntry");

	py::class_<wxTextCtrl, wxControl>(m, "TextCtrl")
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

	py::class_<wxSearchCtrl, wxControl>(m, "SearchCtrl")
		.CONTROL_INIT(const wxString&, value=wxEmptyString, wxSearchCtrlNameStr)
		.def("ShowSearchButton", &wxSearchCtrl::ShowSearchButton, show=true)
		.def("ShowCancelButton", &wxSearchCtrl::ShowCancelButton, show=true)
		.def("GetValue", &wxSearchCtrl::GetValue)
		.def("SetValue", &wxSearchCtrl::SetValue, value)
		;

	py::class_<wxSpinCtrl, wxControl>(m, "SpinCtrl")
		._WINDOW_INIT(PACK(const wxString&,), PACK(value = wxEmptyString,), PACK(int, int, int,), PACK("min"_a=0, "max"_a=100, "initial"_a=0,),
			style=wxSP_ARROW_KEYS, wxT("wxSpinCtrl"))
		;

	py::class_<wxColourPickerCtrl, wxControl>(m, "ColourPickerCtrl")
		.CONTROL_INIT(const wxColour&, "col"_a=*wxBLACK, wxColourPickerCtrlNameStr)
		.def("GetColour", &wxColourPickerCtrl::GetColour)
		.def("SetColour", (void (wxColourPickerCtrl::*)(const wxColour& col)) &wxColourPickerCtrl::SetColour, "col"_a)
		;

	py::class_<wxItemContainerImmutable>(m, "ItemContainerImmutable")
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
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, const wxArrayString&, long, const wxValidator&, const wxString&>(),
			parent, id, pos, size, choices, style_0, validator, name = wxListBoxNameStr)
		;

	py::class_<wxCheckListBox, wxListBox>(m, "CheckListBox")
		.def("IsChecked", &wxCheckListBox::IsChecked, item)
		.def("Check", &wxCheckListBox::Check, item, "check"_a=true)
		.def("GetCheckedItems", &wxCheckListBox::GetCheckedItems)
		;

	py::class_<wxRearrangeList, wxCheckListBox>(m, "RearrangeList")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, const wxArrayInt&, const wxArrayString&, long, const wxValidator&, const wxString&>(),
			parent, id, pos, size, "order"_a, items, style_0, validator, name = wxRearrangeListNameStr)
	;

	py::class_<wxChoice, wxControlWithItems>(m, "Choice")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, const wxArrayString&, long, const wxValidator&, const wxString&>(),
			parent, id, pos, size, choices, style_0, validator, name = wxChoiceNameStr)
		;

	py::class_<wxComboBox, wxControlWithItems>(m, "ComboBox")
		.def(py::init<wxWindow*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, const wxArrayString&, long, const wxValidator&, const wxString&>(),
			parent, id, value, pos, size, choices, style_0, validator, name=wxComboBoxNameStr)
		.def("GetValue", &wxComboBox::GetValue)
		.def("SetValue", &wxComboBox::SetValue, value)
		.def("AutoComplete", (bool (wxComboBox::*)(const wxArrayString &choices)) &wxComboBox::AutoComplete, choices)
		;


	py::class_<wxFilePickerCtrl, wxControl>(m, "FilePickerCtrl")
		.CONTROL_INIT_STYLE(
			PACK(const wxString&, const wxString&, const wxString&),
			PACK("path"_a=wxEmptyString, "message"_a=wxFileSelectorPromptStr, "wildcard"_a=wxFileSelectorDefaultWildcardStr),
			style=wxFLP_DEFAULT_STYLE, wxFilePickerCtrlNameStr)
		.def("GetPath", &wxFilePickerCtrl::GetPath)
		.def("SetPath", &wxFilePickerCtrl::SetPath, "path"_a)
		;


	py::class_<wxDirPickerCtrl, wxControl>(m, "DirPickerCtrl")
		.CONTROL_INIT_STYLE(
			PACK(const wxString&, const wxString&),
			PACK("path"_a = wxEmptyString, "message"_a=wxFileSelectorPromptStr), style = wxDIRP_DEFAULT_STYLE, wxDirPickerCtrlNameStr)
		.def("GetPath", &wxDirPickerCtrl::GetPath)
		.def("SetPath", &wxDirPickerCtrl::SetPath, "path"_a)
		;


	py::class_<wxTreeCtrl, wxControl>(m, "TreeCtrl")
		.CONTROL_INIT_SIMPLE(style=wxTR_HAS_BUTTONS | wxTR_SINGLE, wxTreeCtrlNameStr)
		.def("AssignImageList", &wxTreeCtrl::AssignImageList)
		.def("AddRoot", &wxTreeCtrl::AddRoot, text, "image"_a = -1, "selectedImage"_a = -1, "data"_a = None)
		.def("InsertItem", (wxTreeItemId (wxTreeCtrl::*)(const wxTreeItemId&, size_t, const wxString&, int, int, wxTreeItemData *))
			&wxTreeCtrl::InsertItem, parent, "pos"_a, text, "image"_a = -1, "selectedImage"_a = -1, "data"_a = None)
		.def("GetItemData", &wxTreeCtrl::GetItemData, item)
		.def("Delete", &wxTreeCtrl::Delete, item)
		.def("DeleteChildren", &wxTreeCtrl::DeleteChildren, item)
		.def("DeleteAllItems", &wxTreeCtrl::DeleteAllItems)
		.def("Expand", &wxTreeCtrl::Expand, item)
		.def("ExpandAllChildren", &wxTreeCtrl::ExpandAllChildren, item)
		.def("ExpandAll", &wxTreeCtrl::ExpandAll)
		.def("Collapse", &wxTreeCtrl::Collapse, item)
		.def("CollapseAllChildren", &wxTreeCtrl::CollapseAllChildren, item)
		.def("CollapseAll", &wxTreeCtrl::CollapseAll)
		.def("CollapseAndReset", &wxTreeCtrl::CollapseAndReset, item)
		.def("Toggle", &wxTreeCtrl::Toggle, item)
		.def("Unselect", &wxTreeCtrl::Unselect)
		.def("UnselectAll", &wxTreeCtrl::UnselectAll)
		.def("SelectItem", &wxTreeCtrl::SelectItem, item, "select"_a=true)
		.def("SelectChildren", &wxTreeCtrl::SelectChildren, parent)
		.def("ToggleItemSelection", &wxTreeCtrl::ToggleItemSelection, item)
		.def("GetCount", &wxTreeCtrl::GetCount)
		.def("GetIndent", &wxTreeCtrl::GetIndent)
		.def("SetIndent", &wxTreeCtrl::SetIndent)
		.def("GetSpacing", &wxTreeCtrl::GetSpacing)
		.def("SetSpacing", &wxTreeCtrl::SetSpacing)
		;


	// containers
	py::class_<wxSizer>(m, "Sizer")
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
		.def("GetFlexibleDirection", &wxFlexGridSizer::GetFlexibleDirection)
		.def("SetFlexibleDirection", &wxFlexGridSizer::SetFlexibleDirection, "direction"_a)
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

	py::class_<wxBookCtrlBase, wxControl>(m, "BookCtrlBase")
		.def("AddPage", &wxBookCtrlBase::AddPage, "page"_a, text, "bSelect"_a=false, "imageId"_a=-1)
		.def("GetPageCount", &wxBookCtrlBase::GetPageCount)
		.def("GetSelection", &wxBookCtrlBase::GetSelection)
		.def("SetSelection", &wxBookCtrlBase::SetSelection, "n"_a)
		.def("SetPageText", &wxBookCtrlBase::SetPageText, "n"_a, text)
		.def("GetPageText", &wxBookCtrlBase::GetPageText, "n"_a);

	py::class_<wxNotebook, wxBookCtrlBase>(m, "Notebook")
		.WINDOW_INIT(wxNotebookNameStr);

	py::class_<wxListbook, wxBookCtrlBase>(m, "Listbook")
		.WINDOW_INIT(wxEmptyString);

	// frames

	py::class_<wxTopLevelWindow, wxWindow>(m, "TopLevelWindow")
		.def("GetTitle", &wxTopLevelWindow::GetTitle)
		.def("SetTitle", &wxTopLevelWindow::SetTitle, title)
		.def("SetIcon", &wxTopLevelWindow::SetIcon, "icon"_a)
		.def("Destroy", &wxFrame::Destroy)
		;

	py::class_<wxFrame, wxTopLevelWindow>(m, "Frame")
		.WINDOW_INIT_EXT(const wxString&, title, style=wxDEFAULT_FRAME_STYLE, wxFrameNameStr)
		.def("SetMenuBar", &wxFrame::SetMenuBar)
		.def("GetMenuBar", &wxFrame::GetMenuBar)
		.def("GetStatusBar", &wxFrame::GetStatusBar)
		.def("SetStatusBar", &wxFrame::SetStatusBar)
		.def("SetStatusText", &wxFrame::SetStatusText, text, "number"_a=0)
		.def("SetStatusWidths", &wxFrame::SetStatusWidths, "n"_a, "widths_field"_a)
		.def("PushStatusText", &wxFrame::PushStatusText, text, "number"_a=0)
		.def("PopStatusText", &wxFrame::PopStatusText, "number"_a=0)
		.def("SetStatusBarPane", &wxFrame::SetStatusBarPane, "n"_a)
		.def("GetStatusBarPane", &wxFrame::GetStatusBarPane)
		;

	py::class_<wxMDIParentFrame, wxFrame>(m, "MDIParentFrame")
		.WINDOW_INIT_EXT(const wxString&, title, style=wxDEFAULT_FRAME_STYLE | wxVSCROLL | wxHSCROLL, wxFrameNameStr)
		;

	py::class_<wxMDIChildFrame, wxFrame>(m, "MDIChildFrame")
		.def(py::init<wxMDIParentFrame*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, title, pos, size, style=wxDEFAULT_FRAME_STYLE, name=wxFrameNameStr)
		;

	py::class_<wxDialog, wxTopLevelWindow>(m, "Dialog")
		.WINDOW_INIT_EXT(const wxString&, title, style=wxDEFAULT_DIALOG_STYLE, wxDialogNameStr)
		.def("IsModal", &wxDialog::IsModal)
		.def("EndModal", &wxDialog::EndModal, "retCode"_a)
		;
	
	// menu
	py::class_<wxMenu>(m, "Menu")
		.def(py::init<int>(), style)
		.def(py::init<const wxString&, int>(), title, style)
		.def("AppendSubMenu", &wxMenu::AppendSubMenu)
		.def("Append", (wxMenuItem* (wxMenu::*)(int, const wxString&, const wxString&, wxItemKind)) &wxMenu::Append)
		.def("Remove", (wxMenuItem* (wxMenu::*)(wxMenuItem *)) &wxMenu::Remove)
		.def("AppendSeparator", &wxMenu::AppendSeparator)
		.def("GetMenuItemCount", &wxMenu::GetMenuItemCount)
		.def("GetTitle", &wxMenu::GetTitle)
		;
	
	
	py::class_<wxMenuBar, wxWindow>(m, "MenuBar")
		.def(py::init<>())
		.def(py::init<long>(), style)
		// .def(py::init<size_t, wxMenu *[], const wxString[], long>(), "n"_a, "menus"_a, "titles"_a, style_0)
		.def("Append", &wxMenuBar::Append, "menu"_a, title)
		.def("Insert", &wxMenuBar::Insert, "pos"_a, "menu"_a, title)
		.def("Remove", &wxMenuBar::Remove)
		;
	
	
	py::class_<wxMenuItem>(m, "MenuItem")
		.def("GetItemLabel", &wxMenuItem::GetItemLabel)
		.def("SetItemLabel", &wxMenuItem::SetItemLabel)
		.def("GetId", &wxMenuItem::GetId)
		.def("IsCheck", &wxMenuItem::IsCheck)
		.def("Check", &wxMenuItem::Check, "bDoEnable"_a=true)
		.def("Enable", &wxMenuItem::Enable, "bDoCheck"_a=true)
		;

	// bars
	py::class_<wxToolBar, wxControl>(m, "ToolBar")
		.WINDOW_INIT_STYLE(style=wxTB_DEFAULT_STYLE, wxToolBarNameStr)
		.def("AddTool", (wxToolBarToolBase* (wxToolBar::*)(int, const wxString&, const wxBitmap&, const wxString&, wxItemKind))
			&wxToolBar::AddTool, "toolid"_a, "label"_a, "bitmap"_a, "shortHelp"_a = wxEmptyString, "kind"_a = wxITEM_NORMAL)
		.def("AddControl", &wxToolBar::AddControl, "control"_a, label)
		.def("InsertControl", &wxToolBar::InsertControl, "pos"_a, "control"_a, label)
		.def("AddSeparator", &wxToolBar::AddSeparator)
		.def("Realize", &wxToolBar::Realize)
		.def("ClearTools", &wxToolBar::ClearTools)
		.def("FindById", &wxToolBar::FindById)
		.def("GetToolPos", &wxToolBar::GetToolPos)
		.def("SetToolBitmapSize", &wxToolBar::SetToolBitmapSize)
		;

	py::class_<wxAuiToolBar, wxControl>(m, "AuiToolBar")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long>(),
			parent, id, pos, size, style=wxAUI_TB_DEFAULT_STYLE)
		.def("AddTool", (wxAuiToolBarItem* (wxAuiToolBar::*)(int, const wxString&, const wxBitmap&, const wxString&, wxItemKind))
			&wxAuiToolBar::AddTool, "toolid"_a, "label"_a, "bitmap"_a, "shortHelp"_a = wxEmptyString, "kind"_a = wxITEM_NORMAL)
		.def("AddControl", &wxAuiToolBar::AddControl, "control"_a, label)
		.def("AddSeparator", &wxAuiToolBar::AddSeparator)
		.def("Realize", &wxAuiToolBar::Realize)
		.def("ClearTools", &wxAuiToolBar::ClearTools)
		.def("GetToolPos", &wxAuiToolBar::GetToolPos)
		.def("SetToolBitmapSize", &wxAuiToolBar::SetToolBitmapSize)
		;
	
	py::class_<wxStatusBar, wxControl>(m, "StatusBar")
		.def(py::init<wxWindow*, wxWindowID, long, const wxString&>(),
			parent, id, style=wxSTB_DEFAULT_STYLE, name=wxStatusBarNameStr)
		.def("GetStatusText", &wxStatusBar::GetStatusText, "number"_a=0)
		.def("SetStatusText", &wxStatusBar::SetStatusText, text, "number"_a=0)
		.def("SetFieldsCount", &wxStatusBar::SetFieldsCount, "number"_a=1, "widths"_a)
		.def("SetStatusWidths", &wxStatusBar::SetStatusWidths, "number"_a=1, "widths"_a)
		.def("GetStatusWidth", &wxStatusBar::GetStatusWidth, "n"_a)
		.def("PopStatusText", &wxStatusBar::PopStatusText, "number"_a=0)
		.def("PushStatusText", &wxStatusBar::PushStatusText, text, "number"_a=0)
		;

	// datacontrols

	py::class_<wxPropertyGrid, wxControl>(m, "PropertyGrid")
		.WINDOW_INIT(wxPropertyGridNameStr)
		.def("GetSelection", &wxPropertyGrid::GetSelection)
		// TODO
		// .def("SetPropertyValue", &wxPropertyGrid::SetPropertyValue)
		.def("SetExtraStyle", &wxPropertyGrid::SetExtraStyle, "exStyle"_a)
		.def("SetCaptionBackgroundColour", &wxPropertyGrid::SetCaptionBackgroundColour, "col"_a)
		.def("SetMarginColour", &wxPropertyGrid::SetMarginColour, "col"_a)
		.def("Append", &wxPropertyGrid::Append)
		.def("GetPropertyByName", (wxPGProperty* (wxPropertyGrid::*)( const wxString& name ) const) &wxPropertyGrid::GetPropertyByName);
	
	
	py::class_<wxPGProperty>(m, "PGProperty")
		.def("GetName", &wxPGProperty::GetName)
		.def("GetLabel", &wxPGProperty::GetLabel)
		.def("GetValue", &wxPGProperty::GetValue)
		.def("SetHelpString", &wxPGProperty::SetHelpString)
		.def("SetAttribute", &wxPGProperty::SetAttribute, name, value)
		.def("SetFlagRecursively", &wxPGProperty::SetFlagRecursively, "flag"_a, "set"_a);

	py::class_<wxPropertyCategory, wxPGProperty>(m, "PropertyCategory")
		.def(py::init<const wxString &, const wxString &>(), "label"_a, name=wxPG_LABEL);

	py::class_<wxStringProperty, wxPGProperty>(m, "StringProperty")
		.def(py::init<const wxString &, const wxString &, const wxString &>(),
			"label"_a = wxPG_LABEL, name = wxPG_LABEL, value = wxEmptyString);

	py::class_<wxIntProperty, wxPGProperty>(m, "IntProperty")
		.def(py::init<const wxString &, const wxString &, long>(),
			"label"_a = wxPG_LABEL, name = wxPG_LABEL, value = 0L);

	py::class_<wxUIntProperty, wxPGProperty>(m, "UIntProperty")
		.def(py::init<const wxString &, const wxString &, long>(),
			"label"_a = wxPG_LABEL, name = wxPG_LABEL, value = 0L);

	py::class_<wxFloatProperty, wxPGProperty>(m, "FloatProperty")
		.def(py::init<const wxString &, const wxString &, double>(),
			"label"_a = wxPG_LABEL, name = wxPG_LABEL, value = 0.0);

	py::class_<wxBoolProperty, wxPGProperty>(m, "BoolProperty")
		.def(py::init<const wxString &, const wxString &, bool>(),
			"label"_a = wxPG_LABEL, name = wxPG_LABEL, value = false);

	py::class_<wxEnumProperty, wxPGProperty>(m, "EnumProperty")
		.def(py::init<const wxString &, const wxString &, const wxArrayString &, const wxArrayInt &, int>(),
			"label"_a, name, "labels"_a = wxArrayString(), "values"_a = wxArrayInt(), value = 0)
		.def(py::init<>());

	py::class_<wxFlagsProperty, wxPGProperty>(m, "FlagsProperty")
		.def(py::init<const wxString&, const wxString&, const wxArrayString&, const wxArrayInt&, int>(),
			"label"_a, name, "labels"_a, "values"_a = wxArrayInt(), value = 0)
		.def(py::init<>());

	py::class_<wxLongStringProperty, wxPGProperty>(m, "LongStringProperty")
		.def(py::init<const wxString &, const wxString &, const wxString &>(),
			"label"_a = wxPG_LABEL, name = wxPG_LABEL, value = wxEmptyString);

	py::class_<wxArrayStringProperty, wxPGProperty>(m, "ArrayStringProperty")
		.def(py::init<const wxString &, const wxString &, const wxArrayString &>(),
			"label"_a = wxPG_LABEL, name = wxPG_LABEL, value = wxArrayString());


	py::class_<wxPGPropertyFlags>(m, "PGPropertyFlags");

	py::class_<wxVariant>(m, "Variant")
		.def("GetType", &wxVariant::GetType)
		.def("GetLong", &wxVariant::GetLong)
		.def("GetString", &wxVariant::GetString)
		.def("GetBool", &wxVariant::GetBool)
		.def("GetArrayString", &wxVariant::GetArrayString);

	// ListView
	py::class_<wxListView, wxControl>(m, "ListView")
		.CONTROL_INIT_SIMPLE(style=wxLC_REPORT, wxListCtrlNameStr)
		.def("AppendColumn", &wxListView::AppendColumn, "heading"_a, "format"_a, "width"_a=-1)
		.def("GetItemCount", &wxListView::GetItemCount)
		.def("InsertItem", (long (wxListView::*)(const wxListItem& info)) &wxListView::InsertItem, "info"_a)
		.def("InsertItem", (long (wxListView::*)(long index, const wxString& label, int imageIndex)) &wxListView::InsertItem,
			"index"_a, "label"_a, "imageId"_a = -1)
		.def("SetItem", (bool (wxListView::*)(wxListItem& info)) &wxListView::SetItem)
		.def("SetItem", (bool (wxListView::*)(long, int, const wxString&, int)) &wxListView::SetItem,
			"index"_a, "col"_a, "label"_a, "imageId"_a = -1)
		.def("GetFirstSelected", &wxListView::GetFirstSelected)
		.def("GetNextSelected", &wxListView::GetNextSelected)
		.def("GetItemCount", &wxListView::GetItemCount)
		.def("GetColumnCount", &wxListView::GetColumnCount)
		.def("EnableCheckBoxes", &wxListView::EnableCheckBoxes)
		.def("IsItemChecked", &wxListView::IsItemChecked, item)
		.def("IsSelected", &wxListView::IsSelected, item)
		.def("CheckItem", &wxListView::CheckItem, item, "check"_a)
		.def("Select", &wxListView::Select, item, "select"_a)
		.def("GetFocusedItem", &wxListView::GetFocusedItem)
		.def("Focus", &wxListView::Focus, "index"_a)
		;

	py::class_<wxListItem>(m, "ListItem")
		.def_readwrite("m_mask", &wxListItem::m_mask)
		.def_readwrite("m_itemId", &wxListItem::m_itemId)
		.def_readwrite("m_col", &wxListItem::m_col)
		.def_readwrite("m_text", &wxListItem::m_text)
		.def_readwrite("m_itemId", &wxListItem::m_itemId);
	
	// aui
	py::class_<wxAuiManager>(m, "AuiManager")
		.def(py::init<wxWindow*, unsigned int>(),
			"managedWnd"_a = NULL, "flags"_a = wxAUI_MGR_DEFAULT)
		.def("UnInit", &wxAuiManager::UnInit)
		.def("Update", &wxAuiManager::Update)
		.def("AddPane", (bool (wxAuiManager::*)(wxWindow*, const wxAuiPaneInfo&)) &wxAuiManager::AddPane, window, "paneInfo"_a)
		.def("AddPane", (bool (wxAuiManager::*)(wxWindow*, int, const wxString&))
			&wxAuiManager::AddPane, window, "direction"_a = wxLEFT, "caption"_a = wxEmptyString)
		.def("GetPane", (wxAuiPaneInfo& (wxAuiManager::*)(wxWindow*)) &wxAuiManager::GetPane, window)
		.def("GetPane", (wxAuiPaneInfo& (wxAuiManager::*)(const wxString&)) &wxAuiManager::GetPane, name)
		;
	
	py::class_<wxAuiPaneInfo>(m, "AuiPaneInfo")
		.def(py::init<>())
		.def("Name", &wxAuiPaneInfo::Name)
		.def("Top", &wxAuiPaneInfo::Top)
		.def("Right", &wxAuiPaneInfo::Right)
		.def("Bottom", &wxAuiPaneInfo::Bottom)
		.def("Left", &wxAuiPaneInfo::Left)
		.def("Center", &wxAuiPaneInfo::Center)
		.def("Caption", &wxAuiPaneInfo::Caption)
		.def("CloseButton", &wxAuiPaneInfo::CloseButton)
		.def("MaximizeButton", &wxAuiPaneInfo::MaximizeButton)
		.def("MinimizeButton", &wxAuiPaneInfo::MinimizeButton)
		.def("CaptionVisible", &wxAuiPaneInfo::CaptionVisible)
		.def("Row", &wxAuiPaneInfo::Row)
		.def("Hide", &wxAuiPaneInfo::Hide)
		/* .def_readwrite("name", &wxAuiPaneInfo::name)
		.def_readwrite("caption", &wxAuiPaneInfo::caption)
		.def_readwrite("icon", &wxAuiPaneInfo::icon)
		.def_readwrite("state", &wxAuiPaneInfo::state)
		.def_readwrite("dock_direction", &wxAuiPaneInfo::dock_direction)
		.def_readwrite("dock_layer", &wxAuiPaneInfo::dock_layer)
		.def_readwrite("dock_row", &wxAuiPaneInfo::dock_row)
		.def_readwrite("dock_pos", &wxAuiPaneInfo::dock_pos)
		.def_readwrite("dock_proportion", &wxAuiPaneInfo::dock_proportion) */
		;

	py::class_<wxAuiMDIParentFrame, wxFrame>(m, "AuiMDIParentFrame")
		.WINDOW_INIT_EXT(const wxString&, title, style=wxDEFAULT_FRAME_STYLE | wxVSCROLL | wxHSCROLL, wxFrameNameStr)
		.def("GetNotebook", &wxAuiMDIParentFrame::GetNotebook)
		;

	py::class_<wxAuiMDIChildFrame, wxFrame>(m, "AuiMDIChildFrame")
		.def(py::init<wxAuiMDIParentFrame*, wxWindowID, const wxString&, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, title, pos, size, style=wxDEFAULT_FRAME_STYLE, name = wxFrameNameStr)
		;


	py::class_<wxAuiNotebook, wxControl>(m, "AuiNotebook")
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long>(),
			parent, id, pos, size, style=wxAUI_NB_DEFAULT_STYLE)
		.def("GetSelection", &wxAuiNotebook::GetSelection)
		.def("SetSelection", &wxAuiNotebook::SetSelection)
		.def("GetPageCount", &wxAuiNotebook::GetPageCount)
		.def("GetPage", &wxAuiNotebook::GetPage)
		.def("DeletePage", &wxAuiNotebook::DeletePage)
		.def("AddPage", (bool (wxAuiNotebook::*)(wxWindow*, const wxString&, bool, const wxBitmap&)) &wxAuiNotebook::AddPage,
			"page"_a, "caption"_a, "select"_a = false, "bitmap"_a = wxNullBitmap)
		;
	

	// evnents
	py::class_<wxEvent>(m, "Event")
		.def("Skip", &wxEvent::Skip, "skip"_a = true)
		.def("GetId", &wxEvent::GetId)
		.def_property("id", &wxEvent::GetId, &wxEvent::SetId)
		.def("ResumePropagation", &wxKeyEvent::ResumePropagation);

	// 按键事件
	py::class_<wxKeyEvent, wxEvent>(m, "KeyEvent")
		.def("GetKeyCode", &wxKeyEvent::GetKeyCode)
		.def("GetModifiers", &wxKeyEvent::GetModifiers);

	// 树控件事件
	py::class_<wxTreeEvent, wxEvent>(m, "TreeEvent")
		.def("GetItem", &wxTreeEvent::GetItem);

	py::class_<wxCommandEvent, wxEvent>(m, "CommandEvent");

	py::class_<wxPropertyGridEvent, wxCommandEvent>(m, "PropertyGridEvent")
		.def("GetPropertyName", &wxPropertyGridEvent::GetPropertyName);

	py::class_<wxListEvent, wxEvent>(m, "ListEvent")
		.def("GetKeyCode", &wxListEvent::GetKeyCode)
		.def("GetIndex", &wxListEvent::GetIndex)
		.def("GetColumn", &wxListEvent::GetColumn);

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