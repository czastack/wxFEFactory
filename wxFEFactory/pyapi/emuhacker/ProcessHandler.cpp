#ifdef _WIN32

#include "ProcessHandler.h"
#include "types.h"
#include <tchar.h>
#include <psapi.h>
#include <iostream>


bool Is64Bit_OS()
{
	typedef void (WINAPI *LPFN_PGNSI)(LPSYSTEM_INFO);

	SYSTEM_INFO si = { 0 };
	LPFN_PGNSI pGNSI = (LPFN_PGNSI)GetProcAddress(GetModuleHandle(_T("kernel32.dll")), "GetNativeSystemInfo");
	if (pGNSI == NULL)
	{
		return FALSE;
	}
	pGNSI(&si);
	if (si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64 ||
		si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_IA64)
	{
		return true;
	}
	return false;
}


bool ProcessHandler::m_is64os = Is64Bit_OS();


ProcessHandler::ProcessHandler():m_process(nullptr), m_raw_addr(false)
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
	if(m_process)
	{
		CloseHandle(m_process);
		m_process = nullptr;
	}
}

bool ProcessHandler::attach_window(CSTR className, CSTR windowName){
	return attach_handle(FindWindow(className, windowName));
}

bool ProcessHandler::attach_handle(HWND hWnd){
	if(IsWindow(hWnd))
	{
		DWORD	dwProcessId;
		close();
		GetWindowThreadProcessId(hWnd, &dwProcessId);
		m_process = OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION, FALSE, dwProcessId);
		m_is32process = is32Process();
		return m_process != nullptr;
	}
	return false;
}

bool ProcessHandler::isValid()
{
	if (m_process)
	{
		DWORD code;
		GetExitCodeProcess(m_process, &code);
		return code == STILL_ACTIVE;
	}
	return false;
}

bool ProcessHandler::is32Process()
{
	if (!m_is64os)
	{
		return true;
	}

	typedef BOOL(WINAPI *LPFN_ISWOW64PROCESS) (HANDLE, PBOOL);
	LPFN_ISWOW64PROCESS fnIsWow64Process = (LPFN_ISWOW64PROCESS)GetProcAddress(GetModuleHandleW(L"kernel32"), "IsWow64Process");
	if (NULL != fnIsWow64Process)
	{
		BOOL bIsWow64 = FALSE;
		fnIsWow64Process(m_process, &bIsWow64);
		if (bIsWow64)
		{
			return true;
		}
	}
	return false;
}

bool ProcessHandler::raw_read(addr_t addr, LPVOID buffer, size_t size)
{
	return ReadProcessMemory(m_process, (LPVOID)addr, buffer, size, NULL) != 0;
}

bool ProcessHandler::raw_write(addr_t addr, LPCVOID buffer, size_t size)
{
	return WriteProcessMemory(m_process, (LPVOID)addr, buffer, size, NULL) != 0;
}

bool ProcessHandler::read(addr_t addr, LPVOID buffer, size_t size){
	if(isValid())
	{
		if (!m_raw_addr) {
			addr = address_map(addr);
		}
		if (addr) {
			return raw_read(addr, buffer, size);
		}
	}
	return false;
}

bool ProcessHandler::write(addr_t addr, LPCVOID buffer, size_t size){
	if(isValid())
	{
		if (!m_raw_addr) {
			addr = address_map(addr);
		}
		if (addr) {
			return raw_write(addr, buffer, size);
		}
	}
	return false;
}


struct EnumWindowsArg
{
	HWND    hwndWindow;     // 窗口句柄
	DWORD   dwProcessID;    // 进程ID
};
///< 枚举窗口回调函数
BOOL CALLBACK EnumWindowsProc(HWND hwnd, LPARAM lParam)
{
	EnumWindowsArg *pArg = (EnumWindowsArg *)lParam;
	DWORD  dwProcessID = 0;
	// 通过窗口句柄取得进程ID
	::GetWindowThreadProcessId(hwnd, &dwProcessID);
	if (dwProcessID == pArg->dwProcessID)
	{
		pArg->hwndWindow = hwnd;
		// 找到了返回FALSE
		return FALSE;
	}
	// 没找到，继续找，返回TRUE
	return TRUE;
}

bool ProcessHandler::bring_target_top()
{
	EnumWindowsArg ewa;
	ewa.dwProcessID = getProcessId();
	ewa.hwndWindow = NULL;
	::EnumWindows(EnumWindowsProc, (LPARAM)&ewa);
	if (ewa.hwndWindow)
	{
		return ::SetForegroundWindow(ewa.hwndWindow) && ::BringWindowToTop(ewa.hwndWindow);
	}
	return false;
}

/**
 * Get MainModuleAddress
 */
addr_t ProcessHandler::getProcessBaseAddress()
{
	HMODULE     baseModule = 0;
	DWORD       bytesRequired;

	if (EnumProcessModules(m_process, &baseModule, sizeof(baseModule), &bytesRequired))
	{
		return (addr_t)baseModule;
	}

	return 0;
}

addr_t ProcessHandler::getModuleHandle(LPCTSTR name)
{
	DWORD cbNeeded;
	HMODULE hMods[256];

	if (EnumProcessModulesEx(m_process, hMods, sizeof(hMods), &cbNeeded, LIST_MODULES_ALL))
	{
		for (int i = 0; i < (cbNeeded / sizeof(HMODULE)); i++)
		{
			TCHAR szModName[64];
			if (GetModuleBaseName(m_process, hMods[i], szModName, sizeof(szModName)))
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

addr_t ProcessHandler::alloc_memory(size_t size, DWORD protect)
{
	return (addr_t)VirtualAllocEx(m_process, NULL, size, MEM_COMMIT | MEM_RESERVE, protect);
}

void ProcessHandler::free_memory(addr_t addr)
{
	VirtualFreeEx(m_process, (LPVOID)addr, 0, MEM_RELEASE);
}

addr_t ProcessHandler::write_function(LPCVOID buf, size_t size)
{
	addr_t fnAddr = alloc_memory(size, PAGE_EXECUTE_READWRITE);
	if (!fnAddr || !raw_write(fnAddr, buf, size))
	{
		// std::cout << "Write failed" << std::endl;
		return 0;
	}
	return fnAddr;
}

addr_t ProcessHandler::alloc_data(LPCVOID buf, size_t size)
{
	addr_t addr = alloc_memory(size);
	if (!addr || !raw_write(addr, buf, size))
	{
		// std::cout << "Write failed" << std::endl;
		return 0;
	}
	return addr;
}

DWORD ProcessHandler::remote_call(addr_t addr, LONG_PTR arg)
{
	HANDLE hThread = CreateRemoteThread(m_process, NULL, 0, (PTHREAD_START_ROUTINE)addr, (LPVOID)arg, 0, NULL);

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

ProcAddressHelper* ProcessHandler::getProcAddressHelper(addr_t module)
{
	LONG e_lfanew;
	DWORD VirtualAddress;
	// IMAGE_NT_HEADERS64 nth;
	IMAGE_EXPORT_DIRECTORY ides;

	raw_read(module + offsetof(IMAGE_DOS_HEADER, e_lfanew), &e_lfanew, sizeof(LONG));
	size_t offsetVirtualAddress = m_is32process ?
		offsetof(IMAGE_NT_HEADERS32, OptionalHeader) + offsetof(IMAGE_OPTIONAL_HEADER32, DataDirectory)
			+ offsetof(IMAGE_DATA_DIRECTORY, VirtualAddress) :
		offsetof(IMAGE_NT_HEADERS64, OptionalHeader) + offsetof(IMAGE_OPTIONAL_HEADER64, DataDirectory)
			+ offsetof(IMAGE_DATA_DIRECTORY, VirtualAddress);
	raw_read(module + e_lfanew + offsetVirtualAddress, &VirtualAddress, sizeof(DWORD));
	raw_read(module + VirtualAddress, &ides, sizeof(IMAGE_EXPORT_DIRECTORY));
	
	return new ProcAddressHelper(this, &ides, module);
}

addr_t ProcessHandler::find_bytes(BYTE *data, addr_t data_size, addr_t start, addr_t end, int ordinal)
{
	const DWORD PAGE_SIZE = 4096;
	bool finded = false;
	BYTE page[PAGE_SIZE];
	addr_t cur_addr = start;

	BYTE *page_end = page + PAGE_SIZE - data_size;
	BYTE *page_cursor = page;
	int i; // data内偏移量
	int ord = 0; // 找到的数据序号


	while (cur_addr < end) {
		read(cur_addr, page, PAGE_SIZE);
		for (page_cursor = page; page_cursor < page_end; ++page_cursor)
		{
			for (i = 0; i < data_size; ++i) {
				if (page_cursor[i] != data[i])
				{
					break;
				}
			}
			if (i == data_size)
			{
				++ord;
				if (ord == ordinal)
				{
					finded = true;
					break;
				}
			}
		}
		if (finded) {
			break;
		}
		cur_addr += PAGE_SIZE;
	}
	
	if (finded)
	{
		return cur_addr + (page_cursor - page);
	}

	return -1;
}


ProcAddressHelper::ProcAddressHelper(ProcessHandler * handler, LPVOID pides, addr_t module):
	m_handler(handler), m_module(module)
{
	m_pides = new IMAGE_EXPORT_DIRECTORY;
	memcpy(m_pides, pides, sizeof(IMAGE_EXPORT_DIRECTORY));
}

ProcAddressHelper::~ProcAddressHelper()
{
	if (m_pides)
	{
		delete m_pides;
	}
}

addr_t ProcAddressHelper::getProcAddress(LPCSTR funcname)
{
	size_t namesize = strlen(funcname);
	char *namebuf = (char*)malloc(namesize + 1);
	namebuf[namesize] = NULL;

	// 按函数名查找函数地址
	IMAGE_EXPORT_DIRECTORY &ides = *(PIMAGE_EXPORT_DIRECTORY)m_pides;
	addr_t namePtrAddr = m_module + ides.AddressOfNames;
	DWORD nameAddr;
	addr_t result = NULL;
	for (unsigned i = 0; i < ides.NumberOfNames; i++)
	{
		m_handler->raw_read(namePtrAddr, &nameAddr, sizeof(DWORD));
		m_handler->raw_read(m_module + nameAddr, namebuf, namesize);

		if (strcmp(namebuf, funcname) == 0)
		{
			WORD origin;
			DWORD func;
			m_handler->raw_read(m_module + ides.AddressOfNameOrdinals + i * sizeof(WORD), &origin, sizeof(WORD));
			m_handler->raw_read(m_module + ides.AddressOfFunctions + origin * sizeof(DWORD), &func, sizeof(DWORD));
			result = m_module + func;
			break;
		}
		namePtrAddr += sizeof(DWORD);
	}
	free(namebuf);
	return result;
}

#endif