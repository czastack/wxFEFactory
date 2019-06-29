#include <wx/wx.h>
#include <wx/event.h>
#include <wx/button.h>
#include <wx/aui/aui.h>
#include <wx/listbase.h>
#include <wx/listbook.h>
#include <wx/listctrl.h>
#include <wx/spinctrl.h>
#include <wx/srchctrl.h>
#include <wx/tglbtn.h>
#include <wx/treectrl.h>
#include <wx/clrpicker.h>
#include <wx/filepicker.h>
#include <wx/propgrid/propgrid.h>
#include <wx/propgrid/property.h>
#include "ui.h"

void UiModule::init_events()
{
	using namespace py::literals;

	py::class_<wxEvent>(ui, "Event")
		.def("Skip", &wxEvent::Skip, "skip"_a = true)
		.def("GetId", &wxEvent::GetId)
		.def_property("id", &wxEvent::GetId, &wxEvent::SetId)
		.def("ResumePropagation", &wxKeyEvent::ResumePropagation);

	// 按键事件
	py::class_<wxKeyEvent, wxEvent>(ui, "KeyEvent")
		.def("GetKeyCode", &wxKeyEvent::GetKeyCode)
		.def("GetModifiers", &wxKeyEvent::GetModifiers);


	py::class_<wxCommandEvent, wxEvent>(ui, "CommandEvent");

	// 树控件事件
	py::class_<wxTreeEvent, wxCommandEvent>(ui, "TreeEvent")
		.def("GetItem", &wxTreeEvent::GetItem);


	py::class_<wxPropertyGridEvent, wxCommandEvent>(ui, "PropertyGridEvent")
		.def("GetPropertyName", &wxPropertyGridEvent::GetPropertyName);

	py::class_<wxListEvent, wxCommandEvent>(ui, "ListEvent")
		.def("GetKeyCode", &wxListEvent::GetKeyCode)
		.def("GetIndex", &wxListEvent::GetIndex)
		.def("GetColumn", &wxListEvent::GetColumn);

	py::class_<wxCloseEvent, wxEvent>(ui, "CloseEvent")
		.def(py::init<wxEventType, int>(), "type"_a = wxEVT_NULL, "winid"_a = 0);

	auto wx = ui.ptr();
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
