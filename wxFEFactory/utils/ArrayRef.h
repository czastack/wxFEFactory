#pragma once
template<typename TYPE>
class ArrayRef
{
public:
	const int length;
	TYPE *ptr;

	ArrayRef() :length(0), ptr(nullptr)
	{}

	ArrayRef(int size) :length(size)
	{
		ptr = new TYPE[size];
	}

	ArrayRef(std::nullptr_t) :length(0), ptr(nullptr)
	{}

	template<size_t size>
	ArrayRef(TYPE(&arr)[size]) : ptr(arr), length(size)
	{}

	TYPE& last()
	{
		return ptr[length - 1];
	}

	void free()
	{
		delete[] ptr;
		ptr = nullptr;
	}
	operator TYPE*()
	{
		return ptr;
	}
};
