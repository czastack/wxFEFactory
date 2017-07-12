#pragma once
#include "types.h"

typedef struct
{
	u32 baseAddr;
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

	/*
	 * close the handle
	 */
	void close();

	/**
	 * find the first process whose main window has the specified class and window name,
	 * the handle will be automatically closed, unless it is detached
	 */
	bool attachByWindowName(LPCTSTR className, LPCTSTR windowName);

	/*
	 * attach the process whose main window is the specified window
	 * the handle will be automatically closed, unless it is detached
	 */
	bool attachByWindowHandle(HWND hWnd);

	/*
	 * return value is TRUE, if this object has attached to a valid process handle
	 */

	bool isValid();

	virtual bool read(u32 address, size_t size, LPVOID buffer);
	virtual bool write(u32 address, size_t size, LPCVOID buffer);

	bool ptrRead(u32 address, u32 offset, size_t size, LPVOID buffer);
	bool ptrWrite(u32 address, u32 offset, size_t size, LPCVOID buffer);

	bool readLastPtr(const PtrEntry &entry, u32 *addrPtr);

	bool ptrsRead(const PtrEntry &entry, size_t size, LPVOID buffer);
	bool ptrsWrite(const PtrEntry &entry, size_t size, LPCVOID buffer);

	/**
	 * 读取数据到数组
	 */
	template<size_t size, typename TYPE>
	bool read(u32 address, TYPE(&arr)[size]) {
		return read(address, size * sizeof(TYPE), arr);
	}

	/**
	 * 写入数组中的数据
	 */
	template<size_t size, typename TYPE>
	bool write(u32 address, TYPE(&arr)[size]) {
		return write(address, size * sizeof(TYPE), arr);
	}

	/**
	 * 读取数据
	 */
	template<typename TYPE>
	bool read(u32 address, TYPE &buff) {
		return read(address, sizeof(TYPE), &buff);
	}

	/**
	 * 写入数据
	 */
	template<typename TYPE>
	bool write(u32 address, TYPE &buff) {
		return write(address, sizeof(TYPE), &buff);
	}

	/**
	 * 读取数据
	 */
	template<typename T=u8>
	T read(u32 address) {
		T data;
		read(address, data);
		return data;
	}

private:
	HANDLE		mProcess;
};
