#include <wx/wx.h>
#include "../pyutils.h"
#include "../functions.h"
#include "events.h"

void init_events(py::module & m)
{
	using namespace py::literals;

	WXK_ADD;
	// °´¼üÊÂ¼þ
	py::class_<wxEvent>(m, "Event")
		.def("Skip", &wxEvent::Skip, "skip"_a = true)
		.def_property("id", &wxEvent::GetId, &wxEvent::SetId);

	py::class_<wxKeyEvent, wxEvent>(m, "KeyEvent")
		.def("GetKeyCode", &wxKeyEvent::GetKeyCode)
		.def("GetModifiers", [](wxKeyEvent *event) {return event->GetModifiers(); event->ResumePropagation(1); });
}
