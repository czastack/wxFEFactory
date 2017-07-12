#pragma once
#include "types.h"

constexpr size_t operator"" _len(const char *, size_t l)
{
	return l;
}

template<size_t size, typename T>
constexpr size_t lengthof(T(&arr)[size]) {
	return size;
}