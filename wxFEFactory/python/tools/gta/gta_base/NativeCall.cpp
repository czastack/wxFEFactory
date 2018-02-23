class CVector3
{
public:
	float fX;
	float fY;
	float fZ;
};

class Vector4
{
public:
	float fX;
	float fY;
	float fZ;
	float fW;
};

int a = sizeof(IVNativeCallContext);

class IVNativeCallContext
{
public:
	void * m_pReturn;              // 00-04
	unsigned int m_nArgCount;      // 04-08
	void * m_pArgs;                // 08-0C
};

typedef void(_cdecl * NativeCall)(IVNativeCallContext * pNativeContext);

class NativeContext : public IVNativeCallContext
{
public:
	// Configuration
	enum
	{
		MaxNativeParams = 16,
		ArgSize = 4,
	};

	// Anything temporary that we need
	unsigned int m_TempStack[MaxNativeParams];
};

void native_call(NativeContext *ctx)
{
	DWORD* args = (DWORD*)ctx->m_pArgs;
	DWORD dwFunc = *args;
	DWORD dwThis = *(args + 1);
	ctx->m_nArgCount -= 2;
	int i = 0;
	DWORD arg, result;

	for (int i = ctx->m_nArgCount + 1; i > 1; --i)
	{
		arg = *(args + i);
		_asm push arg
	}

	if (dwThis)
	{
		_asm mov ecx, dwThis
	}
	
	_asm {
		call    dwFunc
		mov     result, eax
	}
	if (!dwThis)
	{
		DWORD clear_stack = ctx->m_nArgCount << 2;
		_asm add esp, clear_stack
	}
	*(DWORD*)(ctx->m_pReturn) = result;
}