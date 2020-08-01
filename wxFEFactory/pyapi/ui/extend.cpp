#include <wx/wx.h>
#include <wx/dnd.h>
#include "ui.h"
#include "keyhook/keyhook.h"


class ParamEvent : public wxThreadEvent
{
public:
	ParamEvent(wxEventType eventType, WXWPARAM wParam, WXLPARAM lParam)
		: wxThreadEvent(eventType), wParam(wParam), lParam(lParam) {}

	WXWPARAM wParam;
	WXLPARAM lParam;
};


wxDECLARE_EVENT(EVT_KEYHOOK, ParamEvent);


class KeyHookManager
{
public:
	KeyHookManager(wxEvtHandler* handler) : m_handler(handler) {}
	virtual ~KeyHookManager()
	{
		unsetHook();
	}

	void setHook(DWORD dwThreadId, bool onKeyUp);
	void unsetHook();

protected:
	friend class KeyHookThread;
	static HMODULE hookDll;
	static HHOOK(*SetHook)(DWORD ownerThreadID, DWORD targetThreadID, bool onKeyUp);
	static void (*UnsetHook)();

	wxEvtHandler* m_handler;
};


class KeyHookThread : public wxThread
{
private:
	KeyHookManager* m_owner = nullptr;
	DWORD dwThreadId;
	bool onKeyUp;
public:
	KeyHookThread(KeyHookManager* owner, DWORD dwThreadId, bool onKeyUp) :
		m_owner(owner), dwThreadId(dwThreadId), onKeyUp(onKeyUp) {}

	void* Entry() override;
};

wxDEFINE_EVENT(EVT_KEYHOOK, ParamEvent);

void* KeyHookThread::Entry()
{
	MSG msg;
	PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);
	if (m_owner->SetHook(GetCurrentThreadId(), dwThreadId, onKeyUp))
	{
		while (GetMessage(&msg, NULL, 0, 0) > 0)
		{
			if (WM_HOOK_KEY == msg.message)
			{
				wxQueueEvent(m_owner->m_handler, new ParamEvent(EVT_KEYHOOK, msg.wParam, msg.lParam));
			}

			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
		m_owner->UnsetHook();
	}
	return nullptr;
}


HMODULE KeyHookManager::hookDll = nullptr;
decltype(KeyHookManager::SetHook) KeyHookManager::SetHook = nullptr;
decltype(KeyHookManager::UnsetHook) KeyHookManager::UnsetHook = nullptr;

void KeyHookManager::setHook(DWORD dwThreadId, bool onKeyUp)
{
	if (!hookDll)
	{
		hookDll = LoadLibrary(wxT("keyhook.dll"));
		if (!hookDll)
		{
			py::print(wxT("ÎÞ·¨¼ÓÔØkeyhook.dll"));
			return;
		}
		SetHook = (decltype(SetHook))GetProcAddress(hookDll, "SetHook");
		UnsetHook = (decltype(UnsetHook))GetProcAddress(hookDll, "UnsetHook");
	}
	auto pThread = new KeyHookThread(this, dwThreadId, onKeyUp);
	pThread->Run();
}

void KeyHookManager::unsetHook()
{
	if (hookDll)
	{
		UnsetHook();
	}
}


class PyFileDropTarget: public wxFileDropTarget {
public:
	/* Inherit the constructors */
	using wxFileDropTarget::wxFileDropTarget;

	bool OnDropFiles(wxCoord x, wxCoord y, const wxArrayString& filenames) wxOVERRIDE {
		PYBIND11_OVERLOAD_PURE(bool, wxFileDropTarget, OnDropFiles, x, y, filenames);
	}
};


class PyTextDropTarget : public wxTextDropTarget {
public:
	/* Inherit the constructors */
	using wxTextDropTarget::wxTextDropTarget;

	bool OnDropText(wxCoord x, wxCoord y, wxcstr text) wxOVERRIDE {
		PYBIND11_OVERLOAD_PURE(bool, wxTextDropTarget, OnDropText, x, y, text);
	}
};


int start_text_drag(wxWindow *window, wxcstr text)
{
	wxTextDataObject data(text);
	wxDropSource dragSource(window, wxDROP_ICON(dnd_copy),
		wxDROP_ICON(dnd_move),
		wxDROP_ICON(dnd_none));
	dragSource.SetData(data);
	wxDragResult result = dragSource.DoDragDrop();
	return (int)result;
}


void UiModule::init_extend()
{
	using namespace py::literals;

	py::class_<ParamEvent, wxEvent>(ui, "ParamEvent")
		.def_readwrite("wParam", &ParamEvent::wParam)
		.def_readwrite("lParam", &ParamEvent::lParam);

	py::class_<KeyHookManager>(ui, "KeyHookManager")
		.def(py::init<wxEvtHandler*>(), "handler"_a)
		.def("setHook", &KeyHookManager::setHook, "thread_id"_a, "onkeyup"_a=false)
		.def("unsetHook", &KeyHookManager::unsetHook);

	py::class_<NODELETE(wxFileDropTarget), wxDropTarget, PyFileDropTarget>(ui, "FileDropTarget")
		.def(py::init<>())
		.def("OnDropFiles", &wxFileDropTarget::OnDropFiles, "x"_a, "y"_a, "filenames"_a);

	py::class_<NODELETE(wxTextDropTarget), wxDropTarget, PyTextDropTarget>(ui, "TextDropTarget")
		.def(py::init<>())
		.def("OnDropText", &wxTextDropTarget::OnDropText, "x"_a, "y"_a, "text"_a);

	ui.def("start_text_drag", &start_text_drag, "window"_a, "text"_a);

	ui.attr("EVT_KEYHOOK") = py::int_((wxEventType)EVT_KEYHOOK);
}