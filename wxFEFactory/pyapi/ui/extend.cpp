#include <wx/wx.h>
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


	ui.attr("EVT_KEYHOOK") = py::int_((wxEventType)EVT_KEYHOOK);
}