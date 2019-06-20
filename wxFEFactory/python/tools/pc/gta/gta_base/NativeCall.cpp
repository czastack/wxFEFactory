#include <stdio.h>

class NativeCallContext
{
public:
	void * m_pReturn;              // 00-04
	unsigned int m_nArgCount;      // 04-08
	void * m_pArgs;                // 08-0C
};

typedef void(_cdecl * NativeCall)(NativeCallContext * pNativeContext);

class NativeContext : public NativeCallContext
{
public:
	// Configuration
	enum
	{
		MaxNativeParams = 32,
		ArgSize = 4,
	};

	// Anything temporary that we need
	unsigned int m_TempStack[MaxNativeParams];
};

/**
 * dwThis: 0表示cdecl, 1表示stdcall, 其他表示thiscall
 */
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

	if (dwThis > 1)
	{
		_asm mov ecx, dwThis
	}

	_asm {
		call    dwFunc
		mov     result, eax
	}
	if (dwThis == 0)
	{
		DWORD clear_stack = ctx->m_nArgCount << 2;
		_asm add esp, clear_stack
	}
	*(DWORD*)(ctx->m_pReturn) = result;
}

int main(int argc, char **argv)
{
	// 断点
	return (int)native_call;
}


/*
00141000 55                   push        ebp
00141001 8B EC                mov         ebp,esp
00141003 83 EC 0C             sub         esp,0Ch
00141006 56                   push        esi
    34:     DWORD* args = (DWORD*)ctx->m_pArgs;
00141007 8B 75 08             mov         esi,dword ptr [ctx]
0014100A 57                   push        edi
0014100B 8B 56 08             mov         edx,dword ptr [esi+8]
    35:     DWORD dwFunc = *args;
0014100E 8B 02                mov         eax,dword ptr [edx]
    36:     DWORD dwThis = *(args + 1);
00141010 8B 7A 04             mov         edi,dword ptr [edx+4]
    37:     ctx->m_nArgCount -= 2;
00141013 83 46 04 FE          add         dword ptr [esi+4],0FFFFFFFEh
00141017 8B 4E 04             mov         ecx,dword ptr [esi+4]
    38:     int i = 0;
    39:     DWORD arg, result;
    40:
    41:     for (int i = ctx->m_nArgCount + 1; i > 1; --i)
0014101A 41                   inc         ecx
0014101B 89 45 F4             mov         dword ptr [ebp-0Ch],eax
0014101E 89 7D F8             mov         dword ptr [dwThis],edi
00141021 83 F9 01             cmp         ecx,1
00141024 7E 0F                jle         native_call+35h (0141035h)
    42:     {
    43:         arg = *(args + i);
00141026 8B 04 8A             mov         eax,dword ptr [edx+ecx*4]
00141029 89 45 FC             mov         dword ptr [arg],eax
    44:         _asm push arg
0014102C FF 75 FC             push        dword ptr [arg]
0014102F 49                   dec         ecx
00141030 83 F9 01             cmp         ecx,1
00141033 7F F1                jg          native_call+26h (0141026h)
    45:     }
    46:
    47:     if (dwThis > 1)
00141035 83 FF 01             cmp         edi,1
00141038 76 03                jbe         native_call+3Dh (014103Dh)
    48:     {
    49:         _asm mov ecx, dwThis
0014103A 8B 4D F8             mov         ecx,dword ptr [dwThis]
    50:     }
    51:
    52:     _asm {
    53:         call    dwFunc
0014103D FF 55 F4             call        dword ptr [dwFunc]
    54:         mov     result, eax
00141040 89 45 08             mov         dword ptr [ctx],eax
    55:     }
    56:     if (dwThis == 0)
00141043 85 FF                test        edi,edi
00141045 75 0C                jne         native_call+53h (0141053h)
    57:     {
    58:         DWORD clear_stack = ctx->m_nArgCount << 2;
00141047 8B 46 04             mov         eax,dword ptr [esi+4]
0014104A C1 E0 02             shl         eax,2
0014104D 89 45 F4             mov         dword ptr [dwFunc],eax
    59:         _asm add esp, clear_stack
00141050 03 65 F4             add         esp,dword ptr [clear_stack]
    60:     }
    61:     *(DWORD*)(ctx->m_pReturn) = result;
    62: }
00141053 8B 0E                mov         ecx,dword ptr [esi]
00141055 8B 45 08             mov         eax,dword ptr [result]
00141058 5F                   pop         edi
00141059 5E                   pop         esi
0014105A 89 01                mov         dword ptr [ecx],eax
0014105C 8B E5                mov         esp,ebp
0014105E 5D                   pop         ebp
0014105F C3                   ret
    66:     return (int)native_call;
00141060 B8 00 10 14 00       mov         eax,offset native_call (0141000h)
    67: }
00141065 C3                   ret
*/