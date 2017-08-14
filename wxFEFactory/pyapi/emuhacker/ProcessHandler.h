#pragma once
#include "types.h"
#include <windows.h>

typedef size_t addr_t;
typedef wchar_t* STR;
typedef const wchar_t* CSTR;


class ProcessHandler
{
private:
	HANDLE		mProcess;

public:
	bool        m_addr_is32 = true; // 目标是32位地址

	ProcessHandler();
	virtual ~ProcessHandler();

	virtual bool attach() { return false; }
	virtual addr_t prepareAddr(addr_t addr, size_t size) {
		return 
// #ifdef _WIN64
// 			m_addr_is32 ? (addr & 0xFFFFFFFF) :
// #endif
			addr;
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

	bool rawRead(addr_t addr, size_t size, LPVOID buffer);
	bool rawWrite(addr_t addr, size_t size, LPCVOID buffer);

	bool read(addr_t addr, size_t size, LPVOID buffer);
	bool write(addr_t addr, size_t size, LPCVOID buffer);

	bool add(addr_t addr, int value);

	UINT64 readUint(addr_t addr, size_t size)
	{
		UINT64 data = 0;
		read(addr, size, &data);
		return data;
	}

	bool writeUint(addr_t addr, size_t size, UINT64 data)
	{
		return write(addr, size, &data);
	}

	/**
	 * 读取数据到数组
	 */
	template<size_t size, typename TYPE>
	bool read(addr_t addr, TYPE(&arr)[size]) {
		return read(addr, size * sizeof(TYPE), arr);
	}

	/**
	 * 写入数组中的数据
	 */
	template<size_t size, typename TYPE>
	bool write(addr_t addr, TYPE(&arr)[size]) {
		return write(addr, size * sizeof(TYPE), arr);
	}

	/**
	 * 读取数据
	 */
	template<typename TYPE>
	bool read(addr_t addr, TYPE &buff) {
		return read(addr, sizeof(TYPE), &buff);
	}

	/**
	 * 写入数据
	 */
	template<typename ValueType>
	bool write(addr_t addr, const ValueType &buff) {
		return write(addr, sizeof(ValueType), &buff);
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
		if (m_addr_is32)
		{
			addr &= 0xFFFFFFFF;
		}
#endif

		if (!read(addr,
#ifdef _WIN64
			m_addr_is32 ? sizeof(u32) :
#endif
			sizeof(addr), &addr))
		{
			return 0;
		}

		return addr;
	}

	bool ptrRead(addr_t addr, u32 offset, size_t size, LPVOID buffer);
	bool ptrWrite(addr_t addr, u32 offset, size_t size, LPCVOID buffer);

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
		return addr && read(addr, size, buffer);
	}

	/**
	* 多级指针写入数据
	*/
	template<typename ListType>
	bool ProcessHandler::ptrsWrite(addr_t addr, const ListType &offsets, size_t size, LPCVOID buffer) {
		addr = readLastAddr(addr, offsets);
		return addr && write(addr, size, buffer);
	}
};
