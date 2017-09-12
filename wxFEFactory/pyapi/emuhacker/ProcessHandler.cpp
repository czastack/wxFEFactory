#ifdef __WXMSW__

#include "ProcessHandler.h"
#include "types.h"
#include <psapi.h>

ProcessHandler::ProcessHandler():mProcess(nullptr)
{
	HANDLE	hProcess;
	HANDLE	hToken;
	LUID	id;

	hProcess = GetCurrentProcess();
	if(OpenProcessToken(hProcess, TOKEN_ADJUST_PRIVILEGES, &hToken))
	{
		if(LookupPrivilegeValue(NULL, SE_DEBUG_NAME, &id))
		{
			TOKEN_PRIVILEGES	TPEnableDebug;
			TPEnableDebug.PrivilegeCount = 1;
			TPEnableDebug.Privileges[0].Luid = id;
			TPEnableDebug.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;

			AdjustTokenPrivileges(hToken, FALSE, &TPEnableDebug, 0, NULL, NULL);
		}
		CloseHandle(hToken);
	}
	CloseHandle(hProcess);
}

ProcessHandler::~ProcessHandler()
{
	close();
}

void ProcessHandler::close(){
	if(mProcess)
	{
		CloseHandle(mProcess);
		mProcess = nullptr;
	}
}

bool ProcessHandler::attachByWindowName(CSTR className, CSTR windowName){
	return attachByWindowHandle(FindWindow(className, windowName));
}

bool ProcessHandler::attachByWindowHandle(HWND hWnd){
	if(IsWindow(hWnd))
	{
		DWORD	dwProcessId;
		close();
		GetWindowThreadProcessId(hWnd, &dwProcessId);
		mProcess = OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION, FALSE, dwProcessId);
		return mProcess != nullptr;
	}
	return false;
}

bool ProcessHandler::isValid()
{
	if (mProcess)
	{
		DWORD code;
		GetExitCodeProcess(mProcess, &code);
		return code == STILL_ACTIVE;
	}
	return false;
}

bool ProcessHandler::rawRead(addr_t addr, LPVOID buffer, size_t size)
{
	return ReadProcessMemory(mProcess, (LPVOID)addr, buffer, size, NULL) != 0;
}

bool ProcessHandler::rawWrite(addr_t addr, LPCVOID buffer, size_t size)
{
	return WriteProcessMemory(mProcess, (LPVOID)addr, buffer, size, NULL) != 0;
}

bool ProcessHandler::read(addr_t addr, LPVOID buffer, size_t size){
	if(isValid())
	{
		addr = prepareAddr(addr, size);
		if (addr) {
			return rawRead(addr, buffer, size);
		}
	}
	return false;
}

bool ProcessHandler::write(addr_t addr, LPCVOID buffer, size_t size){
	if(isValid())
	{
		addr = prepareAddr(addr, size);
		if (addr) {
			return rawWrite(addr, buffer, size);
		}
	}
	return false;
}

/**
 * Get MainModuleAddress
 */
addr_t ProcessHandler::GetProcessBaseAddress()
{
	HMODULE     baseModule;
	DWORD       bytesRequired;

	if (EnumProcessModules(mProcess, &baseModule, sizeof(baseModule), &bytesRequired))
	{
		return (addr_t)baseModule;
	}

	return 0;
}

#endif