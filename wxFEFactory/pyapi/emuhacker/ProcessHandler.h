#pragma once
#include "types.h"
#include <windows.h>

typedef size_t addr_t;
typedef wchar_t* STR;
typedef const wchar_t* CSTR;


class ProcessHandler
{
protected:
	HANDLE		m_process;
	addr_t      m_funcGetProcAddress;
	static bool m_is64os;
	bool        m_is32process; // 目标是32位进程

public:
	ProcessHandler();
	virtual ~ProcessHandler();

	virtual bool attach() { return false; }
	virtual addr_t address_map(addr_t addr, size_t size) {
		return addr;
	};

	/*
	 * close the handle
	 */
	void close();

	/**
	 * find the first process whose main window has the specified class and window name,
	 * the handle will be automatically closed, unless it is detached
	 */
	bool attach_window(CSTR className, CSTR windowName);

	/*
	 * attach the process whose main window is the specified window
	 * the handle will be automatically closed, unless it is detached
	 */
	bool attach_handle(HWND hWnd);

	/*
	 * return value is TRUE, if this object has attached to a valid process handle
	 */
	bool isValid();

	bool is32Process();
	auto getProcess() { return m_process; }
	DWORD getProcessId() { return ::GetProcessId(m_process); }

	int getPtrSize() { return m_is32process ? 4 : 8; }

	bool rawRead(addr_t addr, LPVOID buffer, size_t size);
	bool rawWrite(addr_t addr, LPCVOID buffer, size_t size);

	bool read(addr_t addr, LPVOID buffer, size_t size);
	bool write(addr_t addr, LPCVOID buffer, size_t size);

	bool add(addr_t addr, int value)
	{
		u32 origin = read<u32>(addr);
		origin += value;
		return write(addr, origin);
	}

	size_t readUint(addr_t addr, size_t size)
	{
		size_t data = 0;
		read(addr, &data, size);
		return data;
	}

	bool writeUint(addr_t addr, size_t data, size_t size)
	{
		return write(addr, &data, size);
	}

	INT64 readInt(addr_t addr, size_t size)
	{
		INT64 data = (INT64)readUint(addr, size);
		switch (size)
		{
		case 1:
			data = (char)data;
			break;
		case 2:
			data = (short)data;
			break;
		case 4:
			data = (int)data;
			break;
		default:
			break;
		}
		return data;
	}

	bool writeInt(addr_t addr, INT64 data, size_t size)
	{
		return writeUint(addr, data & ((1 << (size << 3)) - 1), size);
	}

	/**
	 * 读取数据到数组
	 */
	template<size_t size, typename TYPE>
	bool read(addr_t addr, TYPE(&arr)[size]) {
		return read(addr, arr, size * sizeof(TYPE));
	}

	/**
	 * 写入数组中的数据
	 */
	template<size_t size, typename TYPE>
	bool write(addr_t addr, TYPE(&arr)[size]) {
		return write(addr, arr, size * sizeof(TYPE));
	}

	/**
	 * 读取数据
	 */
	template<typename TYPE>
	bool read(addr_t addr, TYPE &buff) {
		return read(addr, &buff, sizeof(TYPE));
	}

	/**
	 * 写入数据
	 */
	template<typename ValueType>
	bool write(addr_t addr, const ValueType &buff) {
		return write(addr, &buff, sizeof(ValueType));
	}

	/**
	 * 读取数据
	 */
	template<typename ValueType=u8>
	ValueType read(addr_t addr) {
		ValueType data;
		read(addr, data);
		return data;
	}

	addr_t readAddr(addr_t addr)
	{
#ifdef _WIN64
		if (m_is32process)
		{
			addr &= 0xFFFFFFFF;
		}
#endif

		if (!read(addr, &addr,
#ifdef _WIN64
			m_is32process ? sizeof(u32) :
#endif
			sizeof(addr)))
		{
			return 0;
		}

		return addr;
	}

	bool ptrRead(addr_t addr, u32 offset, size_t size, LPVOID buffer) {
		addr = readAddr(addr);
		if (addr)
			return read(addr + offset, buffer, size);
		return false;
	}
	bool ptrWrite(addr_t addr, u32 offset, size_t size, LPCVOID buffer) {
		addr = readAddr(addr);
		if (addr)
			return write(addr + offset, buffer, size);
		return false;
	}

	template<typename ListType>
	addr_t readLastAddr(addr_t addr, const ListType &offsets) {
		for (auto const offset : offsets) {
			addr = readAddr(addr);
			if (!addr)
				return 0;

			addr += offset;
		}
		return addr;
	}

	/**
	 * 多级指针读取数据
	 */
	template<typename ListType>
	bool ptrsRead(addr_t addr, const ListType &offsets, size_t size, LPVOID buffer) {
		addr = readLastAddr(addr, offsets);
		return addr && read(addr, buffer, size);
	}

	/**
	 * 多级指针写入数据
	 */
	template<typename ListType>
	bool ptrsWrite(addr_t addr, const ListType &offsets, size_t size, LPCVOID buffer) {
		addr = readLastAddr(addr, offsets);
		return addr && write(addr, buffer, size);
	}

	addr_t getProcessBaseAddress();

	addr_t getModuleHandle(LPCTSTR name);

	addr_t alloc_memory(size_t size, DWORD protect = PAGE_READWRITE);
	void free_memory(addr_t addr);

	addr_t write_function(LPCVOID buf, size_t size);
	addr_t alloc_data(LPCVOID buf, size_t size);

	DWORD remote_call(addr_t addr, LONG_PTR arg);
	class ProcAddressHelper* getProcAddressHelper(addr_t module);
};


class ProcAddressHelper
{
private:
	ProcessHandler * m_handler;
	LPVOID m_pides;
	addr_t m_module;
public:
	ProcAddressHelper(ProcessHandler *handler, LPVOID pides, addr_t module);
	~ProcAddressHelper();
	addr_t getProcAddress(LPCSTR funcname);
};