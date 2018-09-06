#include <stdio.h>
#include <windows.h>


void native_call(int type) {
    auto sub_567E60 = (int (__thiscall *)(DWORD *self, int a2, float a3, float a4, char a5, char a6, int a7))0x567E60;
    auto sub_4CB0E0 = (signed int (__thiscall *)(void *self, int a2, int a3, int a4))0x4CB0E0;

    DWORD self = *(DWORD*)(*(DWORD*)(0x007912A0) + 0x424);
    DWORD v31 = 4 * 1;
    DWORD self2 = *(DWORD *)(v31 + *(DWORD *)(self + 76));

    int v4 = sub_567E60(*(DWORD **)(self2 + 120), 109, -1.0, -1.0, 1, 2, 0);
    if (v4)
    {
        DWORD v32 = (*(int(__thiscall **)(void *self, signed int, int, int, int, signed int))(*(DWORD*)self2 + 172))
            ((void*)self2, type, *(DWORD *)(v4 + 64), *(DWORD *)(v4 + 60), *(DWORD *)(v4 + 64), 1);
        (*(void(__thiscall **)(int, int, DWORD))(*(DWORD *)v32 + 224))(v32, v4, 0);
        sub_4CB0E0((void*)v4, v32, 0xBF800000, 0xBF800000);
    }
}

int main(int argc, char **argv)
{
    return (int)native_call;
}