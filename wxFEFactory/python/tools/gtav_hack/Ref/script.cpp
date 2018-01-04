#include "script.h"

class NativeContext
{
public:
	void* m_pReturn;
	UINT32 m_nArgCount;
	void* m_pArgs;

	UINT32 m_nDataCount;
};


HANDLE g_hThreadEvent;
NativeContext* p_ctx = NULL;
typedef void(_cdecl * NativeCall)(NativeContext * pNativeContext);

extern "C" _declspec(dllexport) bool script_call(NativeContext *ctx)
{
	p_ctx = ctx;
	DWORD status = WaitForSingleObject(g_hThreadEvent, 2000);
	return status == WAIT_OBJECT_0;
	/*int try_count = 20;
	while (--try_count)
	{
		Sleep(20);
		if (!p_ctx)
		{
			break;
		}
	}*/
}

void ScriptMain()
{
	g_hThreadEvent = CreateEvent(NULL, FALSE, FALSE, NULL);


	while (true)
	{
		if (p_ctx)
		{
			NativeContext* ctx = p_ctx;
			ctx->m_nArgCount -= 1;
			auto args = (DWORD64*)ctx->m_pArgs;
			DWORD64 hash = args[ctx->m_nArgCount];

			nativeInit(hash);
			for (size_t i = 0; i < ctx->m_nArgCount; ++i)
			{
			nativePush64(args[i]);
			}

			PUINT64 result = nativeCall();
			for (size_t i = 0; i < 4; i++)
			{
				((PUINT64)ctx->m_pReturn)[i] = result[i];
			}
			p_ctx = NULL;
			SetEvent(g_hThreadEvent);
		}

		WAIT(0);
	}
}
