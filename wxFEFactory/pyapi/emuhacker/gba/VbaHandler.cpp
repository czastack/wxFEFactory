#ifdef __WXMSW__

#include "VbaHandler.h"
#include "utils/utils.h"

bool VbaHandler::attach(){
	HWND hWnd = NULL;
	EnumWindows(EnumVBAWindowProc, reinterpret_cast<LPARAM>(&hWnd));
	bool bResult = attachByWindowHandle(hWnd);

	if (bResult) {
		VBA_PtrStruct table;
		rawRead(MAP_ADDR, &table, sizeof(table));
		for (int i = 0; i < lengthof(mPtrTable); ++i)
		{
			mPtrTable[i] = table[i].dwPointer;
		}
	}

	return bResult;
}

BOOL CALLBACK VbaHandler::EnumVBAWindowProc(HWND hWnd, LPARAM lParam)
{
	static CONST TCHAR szName[] = TEXT("VisualBoyAdvance");
	static CONST DWORD cchNameLength = sizeof(szName) / sizeof(szName[0]);

	static CONST DWORD cchNameSpeedLength = (DWORD)"VisualBoyAdvance-nnn%"_len;

	TCHAR szWindowName[cchNameSpeedLength];
	DWORD cchWindowName;
	BOOL  bContinue = TRUE;

	cchWindowName = GetWindowText(hWnd, szWindowName, cchNameSpeedLength);
	if (cchWindowName >= cchNameLength - 1)
	{
		if (wcsncmp(szWindowName, szName, cchNameLength - 1) == 0)
		{
			if (cchWindowName >= cchNameLength)
			{
				if (szWindowName[cchNameLength - 1] == TEXT('-'))
					bContinue = FALSE;
			}
			else
			{
				bContinue = FALSE;
			}
		}
	}

	if (bContinue == FALSE)
	{
		*reinterpret_cast<HWND *>(lParam) = hWnd;
	}

	return bContinue;
}


#endif