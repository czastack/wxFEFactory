#pragma once
#include "types.h"
#include <windows.h>

typedef size_t addr_t; typedef wchar_t* STR;
typedef const wchar_t* CSTR;

typedef struct
{
	addr_t baseAddr;
	int ptrLevel;
	u32 offsets[4];
	u32 lastOffset() const{
		return offsets[ptrLevel - 1];
	}
} PtrEntry;


class ProcessHandler
{
public:
	ProcessHandler();
	virtual ~ProcessHandler();

	virtual bool attach() = 0;
	virtual addr_t prepareAddr(addr_t addr, size_t size) = 0;

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

	bool ptrRead(addr_t addr, u32 offset, size_t size, LPVOID buffer);
	bool ptrWrite(addr_t addr, u32 offset, size_t size, LPCVOID buffer);

	bool readLastPtr(const PtrEntry &entry, addr_t *addrPtr);

	bool ptrsRead(const PtrEntry &entry, size_t size, LPVOID buffer);
	bool ptrsWrite(const PtrEntry &entry, size_t size, LPCVOID buffer);

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
	template<typename TYPE>
	bool write(addr_t addr, TYPE &buff) {
		return write(addr, sizeof(TYPE), &buff);
	}

	/**
	 * 读取数据
	 */
	template<typename T=u8>
	T read(addr_t addr) {
		T data;
		read(addr, data);
		return data;
	}

private:
	HANDLE		mProcess;
};
