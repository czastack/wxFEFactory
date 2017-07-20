#pragma once
#include "types.h"

#define HAS_MEM_FUNC(FunctionName, HelperName) \
template<typename T> \
struct HelperName { \
	template <typename C> static bool test(decltype(&C::FunctionName)); \
	template <typename C> static short test(...); \
	static constexpr bool value = sizeof(test<T>(0)) == sizeof(bool); \
}

constexpr size_t operator"" _len(const char *, size_t l)
{
	return l;
}

template<size_t size, typename T>
constexpr size_t lengthof(T(&arr)[size]) {
	return size;
}