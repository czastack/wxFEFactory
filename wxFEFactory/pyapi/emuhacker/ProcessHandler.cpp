#ifdef _WIN32

#include "ProcessHandler.h"
#include "types.h"
#include <psapi.h>
#include <iostream>


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
		mProcess = OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION, FALSE, dwProcessId);
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
addr_t ProcessHandler::getProcessBaseAddress()
{
	HMODULE     baseModule;
	DWORD       bytesRequired;

	if (EnumProcessModules(mProcess, &baseModule, sizeof(baseModule), &bytesRequired))
	{
		return (addr_t)baseModule;
	}

	return 0;
}

addr_t ProcessHandler::getModuleHandle(LPCTSTR name)
{
	DWORD cbNeeded;
	HMODULE hMods[256];

	if (EnumProcessModulesEx(mProcess, hMods, sizeof(hMods), &cbNeeded, LIST_MODULES_ALL))
	{
		for (int i = 0; i < (cbNeeded / sizeof(HMODULE)); i++)
		{
			TCHAR szModName[64];
			if (GetModuleBaseName(mProcess, hMods[i], szModName, sizeof(szModName)))
			{
				if (wcscmp(name, szModName) == 0)
				{
					return (addr_t)hMods[i];
				}
			}
		}
	}
	return 0;
}

addr_t ProcessHandler::write_function(LPCVOID buf, size_t size)
{
	addr_t fnAddr = alloc_memory(size);
	if (fnAddr == NULL)
	{
		std::cout << "Alloc function failed" << std::endl;
		return 0;
	}

	if (!rawWrite(fnAddr, buf, size))
	{
		std::cout << "Write function failed" << std::endl;
		return 0;
	}
	return fnAddr;
}

addr_t ProcessHandler::alloc_memory(size_t size)
{
	return (addr_t)VirtualAllocEx(mProcess, NULL, size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
}

void ProcessHandler::free_memory(addr_t addr)
{
	VirtualFreeEx(mProcess, (LPVOID)addr, 0, MEM_RELEASE);
}

DWORD ProcessHandler::remote_call(addr_t addr, LONG_PTR arg)
{
	HANDLE hThread = CreateRemoteThread(mProcess, NULL, 0, (PTHREAD_START_ROUTINE)addr, (LPVOID)arg, 0, NULL);

	if (!hThread)
	{
		std::cout << "CreateRemoteThread failed: " << GetLastError() << std::endl;
		return 0;
	}

	WaitForSingleObject(hThread, INFINITE);

	DWORD code;
	GetExitCodeThread(hThread, &code);

	CloseHandle(hThread);
	return code;
}

#endif