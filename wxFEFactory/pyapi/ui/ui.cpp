#include <wx/wx.h>
#include "ui.h"
#include "thread.h"
#include "console.h"
#include "wx/myapp.h"
#include "utils/HistorySet.hpp"

extern class ConsoleHandler console;


auto Console__get_history(ConsoleHandler* self)
{
	return PyListFromArray(*(wxArrayString*)self->getHistory());
}


namespace pybind11 {
	namespace detail {
		ENUM_CASTER(wxStandardID);
	}
}


using namespace py::literals;

UiModule::UiModule(pybind11::module &module) :
	module(module),
	ui(module.def_submodule("ui")),

	parent("parent"_a),
	id("id"_a),
	label("label"_a),
	pos("pos"_a),
	size("size"_a),
	style("style"_a),
	validator("validator"_a),
	name("name"_a),
	event("event"_a),
	value("value"_a),
	text("text"_a),
	title("title"_a),
	show("show"_a),
	item("item"_a),
	items("items"_a),
	choices("choices"_a),
	window("window"_a),
	colour("colour"_a),
	data("data"_a),

	late_v(NULL, NULL), // 延迟初始化的arg_v
	id_v(id = (int)wxID_ANY),
	label_v(label = wxEmptyString),
	pos_v(late_v),
	size_v(late_v),
	style_0(style = 0),
	validator_v(late_v),
	name_v(name = wxEmptyString)
{
	init_ui();
	init_image();
	init_controls();
	init_containers();
	init_menu();
	init_frames();
	init_aui();
	init_datacontrols();
	init_events();
}

void UiModule::init_ui()
{
	py::class_<ConsoleHandler>(ui, "Console")
		.def("bind_elem", &ConsoleHandler::bindElem)
		.def("get_history", Console__get_history);

	py::class_<PyThread>(ui, "Thread")
		.def(py::init<pyobj, DWORD>(), "fn"_a, "delay"_a = 0)
		.def("Run", &PyThread::Run);


	py::setattr(module, "console", py::cast(&console));


	py::class_<wxSize>(ui, "Size")
		.def(py::init<>())
		.def(py::init<int, int>(), "x"_a, "y"_a)
		.def_readwrite("x", &wxSize::x)
		.def_readwrite("y", &wxSize::y);

	py::class_<wxPoint>(ui, "Point")
		.def(py::init<>())
		.def(py::init<int, int>(), "x"_a, "y"_a)
		.def_readwrite("x", &wxPoint::x)
		.def_readwrite("y", &wxPoint::y);

	py::class_<wxFont>(ui, "Font")
		.def(py::init<>())
		.def("SetWeight", (void (wxFont::*)(wxFontWeight)) & wxFont::SetWeight)
		.def("SetStyle", (void (wxFont::*)(wxFontStyle)) & wxFont::SetStyle)
		.def("SetUnderlined", &wxFont::SetUnderlined)
		.def("SetFaceName", &wxFont::SetFaceName)
		.def("SetPointSize", &wxFont::SetPointSize)
		;

	py::class_<wxArrayInt>(ui, "ArrayInt");

	py::class_<wxValidator>(ui, "Validator");

#define ENUM_VAL(name) value(#name, wx##name)

	py::enum_<wxItemKind>(ui, "ItemKind")
		.ENUM_VAL(ITEM_SEPARATOR)
		.ENUM_VAL(ITEM_NORMAL)
		.ENUM_VAL(ITEM_CHECK)
		.ENUM_VAL(ITEM_RADIO)
		.ENUM_VAL(ITEM_DROPDOWN)
		.ENUM_VAL(ITEM_MAX)
		.export_values();

	py::enum_<wxDirection>(ui, "Direction")
		.ENUM_VAL(LEFT)
		.ENUM_VAL(RIGHT)
		.ENUM_VAL(UP)
		.ENUM_VAL(DOWN)
		.ENUM_VAL(TOP)
		.ENUM_VAL(BOTTOM)
		.ENUM_VAL(NORTH)
		.ENUM_VAL(SOUTH)
		.ENUM_VAL(WEST)
		.ENUM_VAL(EAST)
		.ENUM_VAL(ALL)
		.ENUM_VAL(DIRECTION_MASK)
		.export_values();

	py::enum_<wxFontStyle>(ui, "FontStyle")
		.ENUM_VAL(FONTSTYLE_NORMAL)
		.ENUM_VAL(FONTSTYLE_ITALIC)
		.ENUM_VAL(FONTSTYLE_SLANT)
		.export_values();

	py::enum_<wxFontWeight>(ui, "FontWeight")
		.ENUM_VAL(FONTWEIGHT_INVALID)
		.ENUM_VAL(FONTWEIGHT_THIN)
		.ENUM_VAL(FONTWEIGHT_EXTRALIGHT)
		.ENUM_VAL(FONTWEIGHT_LIGHT)
		.ENUM_VAL(FONTWEIGHT_NORMAL)
		.ENUM_VAL(FONTWEIGHT_MEDIUM)
		.ENUM_VAL(FONTWEIGHT_SEMIBOLD)
		.ENUM_VAL(FONTWEIGHT_BOLD)
		.ENUM_VAL(FONTWEIGHT_EXTRABOLD)
		.ENUM_VAL(FONTWEIGHT_HEAVY)
		.ENUM_VAL(FONTWEIGHT_EXTRAHEAVY)
		.ENUM_VAL(FONTWEIGHT_MAX)
		.export_values();

	py::enum_<wxMouseButton>(ui, "MouseButton")
		.ENUM_VAL(MOUSE_BTN_ANY)
		.ENUM_VAL(MOUSE_BTN_NONE)
		.ENUM_VAL(MOUSE_BTN_LEFT)
		.ENUM_VAL(MOUSE_BTN_MIDDLE)
		.ENUM_VAL(MOUSE_BTN_RIGHT)
		.ENUM_VAL(MOUSE_BTN_AUX1)
		.ENUM_VAL(MOUSE_BTN_AUX2)
		.ENUM_VAL(MOUSE_BTN_MAX);

	// 延迟赋值特殊类型的默认参数
	pos_v = pos = wxDefaultPosition;
	size_v = size = wxDefaultSize;
	validator_v = validator = wxDefaultValidator;

	py::setattr(ui, "DefaultPosition", py::cast(wxDefaultPosition));
	py::setattr(ui, "DefaultSize", py::cast(wxDefaultSize));
	py::setattr(ui, "DefaultValidator", py::cast(wxDefaultValidator));

	py::class_<wxMouseState>(ui, "MouseState")
		.def("ButtonIsDown", &wxMouseState::ButtonIsDown, "but"_a)
		.def_readwrite("m_x", &wxMouseState::m_x)
		.def_readwrite("m_y", &wxMouseState::m_y);

	py::class_<wxEvtHandler>(ui, "EvtHandler")
		.def("GetClientData", &wxEvtHandler::GetClientData)
		.def("SetClientData", &wxEvtHandler::SetClientData, data)
		.def("GetHost", [](wxWindow* self) -> py::object {
			PyObject* ptr = reinterpret_cast<PyObject*>(self->GetClientData());
			if (ptr) {
				return py::reinterpret_borrow<py::object>(ptr);
			}
			return None;
		})
		.def("SetHost", [](wxWindow* self, pycref host) {
			self->SetClientData(host.ptr());
		}, "host"_a);


	py::class_<wxApp>(ui, "App")
		.def("GetTopWindow", &wxApp::GetTopWindow);

	py::class_<wxWindow, wxEvtHandler>(ui, "Window")
		.def(py::init<>())
		.def(py::init<wxWindow*, wxWindowID, const wxPoint&, const wxSize&, long, const wxString&>(),
			parent, id, pos_v, size_v, style_0, name = (const char*)wxPanelNameStr)
		.def("GetForegroundColour", &wxWindow::GetForegroundColour)
		.def("SetForegroundColour", &wxWindow::SetForegroundColour, colour)
		.def("GetBackgroundColour", &wxWindow::GetBackgroundColour)
		.def("SetBackgroundColour", &wxWindow::SetBackgroundColour, colour)
		.def("GetWindowStyle", &wxWindow::GetWindowStyle)
		.def("SetWindowStyle", &wxWindow::SetWindowStyle, style)
		.def("GetSize", py::overload_cast<>(&wxWindow::GetSize, py::const_))
		.def("SetSize", py::overload_cast<int, int>(&wxWindow::SetSize), "width"_a, "height"_a)
		.def("GetSizer", &wxWindow::GetSizer)
		.def("SetSizer", &wxWindow::SetSizer, "sizer"_a, "deleteOld"_a = true)
		.def("GetFont", &wxWindow::GetFont)
		.def("SetFont", &wxWindow::SetFont, "font"_a)
		.def("GetId", &wxWindow::GetId)
		.def("SetId", &wxWindow::SetId, "winid"_a)
		.def("IsEnabled", &wxWindow::IsEnabled)
		.def("Enable", &wxWindow::Enable, "enable"_a=true)
		.def("GetLabel", &wxWindow::GetLabel)
		.def("SetLabel", &wxWindow::SetLabel, label)
		.def("Show", &wxWindow::Show, "show"_a=true)
		.def("IsShown", &wxWindow::IsShown)
		.def("Hide", &wxWindow::Hide)
		.def("Destroy", &wxWindow::Destroy)
		.def("Refresh", &wxWindow::Refresh)
		.def("Freeze", &wxWindow::Freeze)
		.def("Thaw", &wxWindow::Thaw)
		.def("SetToolTip", py::overload_cast<const wxString&>(&wxWindow::SetToolTip))
		.def("Reparent", &wxWindow::Reparent)
		.def("Layout", &wxWindow::Layout)
		.def("AddPendingEvent", &wxWindow::wxEvtHandler::AddPendingEvent, event)
		.def("RegisterHotKey", &wxWindow::RegisterHotKey, "hotkeyId"_a, "modifiers"_a, "keycode"_a)
		.def("UnregisterHotKey", &wxWindow::UnregisterHotKey, "hotkeyId"_a)
		.def("Bind", [](wxWindow* self, wxEventType eventType, pycref fn, int winid, int lastId, size_t userData)
		{
			self->Bind(wxEventTypeTag<wxEvent>(eventType), PyFunctor(fn), winid, lastId, (wxObject*)userData);
		}, "eventType"_a, "fn"_a, "winid"_a=(int)wxID_ANY, "lastId"_a=(int)wxID_ANY, "userData"_a=NULL)
		;

	ui.def("GetDisplaySize", &wxGetDisplaySize)
		.def("GetDisplayPPI", &wxGetDisplayPPI)
		.def("GetKeyState", wxGetKeyState)
		.def("GetMouseState", wxGetMouseState)
		.def("GetApp", &wxGetApp);
}


std::unordered_map<PyObject*, wxArrayString> UiModule::m_choices_cache;
bool UiModule::m_choices_cache_on = false;

wxArrayString UiModule::get_choices(pycref choices)
{
	if (m_choices_cache_on) {
		auto it = m_choices_cache.find(choices.ptr());
		if (it != m_choices_cache.end())
		{
			return it->second;
		}
		wxArrayString& array = m_choices_cache.emplace(std::pair<PyObject*, wxArrayString>(choices.ptr(), {})).first->second;
		wxArrayAddAll(array, choices);
		return array;
	}
	else
	{
		return py::cast<wxArrayString>(choices);
	}
}