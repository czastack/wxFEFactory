#include "Trainer.h"
// #include "../Classes/CPlayer.h"
#include "..\ScriptHook\ScriptHook\NativeInvoke.h"
#include <math.h>

// Pull in all our scripting functions/types
using namespace Scripting;

/*
void DisplayLog(char *format, ...)
{
	char text[512] = { NULL };

	va_list args;
	va_start(args, format);
	vsprintf_s(text, sizeof(text), format, args);
	va_end(args);

	LogInfo(text);
	PrintStringWithLiteralStringNow("STRING", text, 5000, 1);
}*/

HANDLE g_hThreadEvent;
NativeContext* p_ctx = NULL;
typedef void(_cdecl * NativeCall)(NativeContext * pNativeContext);

extern "C" _declspec(dllexport) void script_call(NativeContext *ctx)
{
	p_ctx = ctx;
	WaitForSingleObject(g_hThreadEvent, 2000);
}

Trainer::Trainer()
{
	SetName("Trainer");
	g_hThreadEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
}


Trainer::~Trainer()
{
	if (g_hThreadEvent)
	{
		CloseHandle(g_hThreadEvent);
		g_hThreadEvent = NULL;
	}
}


void Trainer::RunScript()
{
	while(IsThreadAlive())
	{
		if (p_ctx)
		{
			NativeContext* ctx = p_ctx;
			p_ctx = NULL;
			auto args = (DWORD*)ctx->m_pArgs;
			ctx->m_nArgCount -= 1;
			DWORD dwFunc = args[ctx->m_nArgCount];

			((NativeCall)dwFunc)(ctx);
			SetEvent(g_hThreadEvent);
		}

		Wait(100);
	}
}
