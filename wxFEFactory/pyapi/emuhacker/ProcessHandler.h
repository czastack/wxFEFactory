#pragma once
#include "types.h"
#include <windows.h>

typedef size_t addr_t;
typedef wchar_t* STR;
typedef const wchar_t* CSTR;


class ProcessHandler
{
protected:
	HANDLE		mProcess;
	static bool m_is64os;
	bool        m_is32process; // 目标是32位进程

public:
	ProcessHandler();
	virtual ~ProcessHandler();

	virtual bool attach() { return false; }
	virtual addr_t prepareAddr(addr_t addr, size_t size) {
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
	bool attachByWindowName(CSTR className, CSTR windowName);

	/*
	 * attach the process whose main window is the specified window
	 * the handle will be automatically closed, unless it is detached
	 */
	bool attachByWindowHandle(HWND hWnd);

	/*
	 * return value is TRUE, if this object has attached to a valid process handle
	 */
	bool isValid();

	bool is32Process();
	auto getProcess() { return mProcess; }
	DWORD getProcessId() { return ::GetProcessId(mProcess); }

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

	UINT64 readUint(addr_t addr, size_t size)
	{
		UINT64 data = 0;
		read(addr, &data, size);
		return data;
	}

	bool writeUint(addr_t addr, UINT64 data, size_t size)
	{
		return write(addr, &data, size);
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
	addr_t ProcessHandler::readLastAddr(addr_t addr, const ListType &offsets) {
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
	bool ProcessHandler::ptrsRead(addr_t addr, const ListType &offsets, size_t size, LPVOID buffer) {
		addr = readLastAddr(addr, offsets);
		return addr && read(addr, buffer, size);
	}

	/**
	* 多级指针写入数据
	*/
	template<typename ListType>
	bool ProcessHandler::ptrsWrite(addr_t addr, const ListType &offsets, size_t size, LPCVOID buffer) {
		addr = readLastAddr(addr, offsets);
		return addr && write(addr, buffer, size);
	}

	addr_t getProcessBaseAddress();

	addr_t getModuleHandle(LPCTSTR name);

	addr_t write_function(LPCVOID buf, size_t size);

	addr_t alloc_memory(size_t size);
	void free_memory(addr_t addr);

	DWORD remote_call(addr_t addr, LONG_PTR arg);
};
