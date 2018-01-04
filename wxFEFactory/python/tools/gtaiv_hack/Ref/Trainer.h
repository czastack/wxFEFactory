#pragma once

#include "../ScriptHook/ScriptHook/ScriptThread.h"
#include "../ScriptHook/ScriptHook/Scripting.h"
#include "../ScriptHook/ScriptHook/Log.h"

#include <iostream>
#include <windows.h>

class Trainer : public ScriptThread
{
protected:
	void RunScript();

public:
	Trainer();
	~Trainer();
};
