#include <wx/wx.h>
#include "frames.h"


void BaseTopLevelWindow::__exit__(py::args & args)
{
	show();

	// 引用加一
	py::cast(this).inc_ref();
	Layout::__exit__(args);
}

void BaseTopLevelWindow::setSize(py::sequence & size)
{
	ptr()->SetSize({ size[0].cast<int>(), size[1].cast<int>() });
}

pyobj BaseTopLevelWindow::getSize()
{
	py::tuple ret = py::tuple(2);
	const wxSize &sz = ptr()->GetSize();
	ret[0] = sz.GetWidth();
	ret[1] = sz.GetHeight();
	return ret;
}

void BaseTopLevelWindow::setPosition(py::sequence & point)
{
	ptr()->SetPosition({ point[0].cast<int>(), point[1].cast<int>() });
}

pyobj BaseTopLevelWindow::getPosition()
{
	py::tuple ret = py::tuple(2);
	const wxPoint &pt = ptr()->GetPosition();
	ret[0] = pt.x;
	ret[1] = pt.y;
	return ret;
}

bool BaseTopLevelWindow::setIcon(wxcstr path)
{
	wxIcon icon;
	wxBitmapType type = (wxBitmapType)getBitmapTypeByExt(path);
	if (type)
	{
		icon.LoadFile(path, type);
		((wxTopLevelWindow*)ptr())->SetIcon(icon);
		return true;
	}
	return false;
}

void BaseTopLevelWindow::_onClose(wxCloseEvent & event) {
	onClose(event);
}

bool BaseTopLevelWindow::onClose(wxCloseEvent & event)
{
	if (hasEventHandler(event))
	{
		if (!handleEvent(event))
		{
			event.Veto();
			return false;
		}
	}
	onRelease();
	event.Skip();
	return true;
}

void BaseTopLevelWindow::onRelease()
{
	// 引用减一，销毁对象
	py::cast(this).dec_ref();
}

void BaseFrame::onRelease()
{
	auto menubar = getMenuBar();

	if (menubar)
		py::cast(menubar).dec_ref();

	BaseTopLevelWindow::onRelease();
}

void HotkeyWindow::onRelease()
{
	stopHotkey();
	Window::onRelease();
}

bool HotkeyWindow::prepareHotkey(pyobj & hotkeyId, WORD & int_hotkeyId)
{
	if (PY_IS_TYPE(hotkeyId, PyUnicode))
	{
		int_hotkeyId = GlobalAddAtom(py::cast<wxString>(hotkeyId));
		hotkeyId = py::int_(int_hotkeyId);
	}
	else if (PY_IS_TYPE(hotkeyId, PyLong))
	{
		int_hotkeyId = py::cast<int>(hotkeyId);
	}
	else
	{
		py::print(hotkeyId, "不支持的格式");
		return false;
	}
	return true;
}

void HotkeyWindow::RegisterHotKey(pyobj hotkeyId, int modifiers, int virtualKeyCode, pycref onhotkey)
{
	WORD _hotkeyId;
	const pyobj origin_hotkey_id = hotkeyId;

	if (prepareHotkey(hotkeyId, _hotkeyId))
	{
		if (m_hotkey_map.contains(hotkeyId))
		{
			py::print(origin_hotkey_id, "已经在使用了");
			return;
		}
		if (ptr()->RegisterHotKey(_hotkeyId, modifiers, virtualKeyCode))
		{
			m_hotkey_map[hotkeyId] = onhotkey;
		}
		else {
			py::print(origin_hotkey_id, "热键注册失败");
		}
	}
}

void HotkeyWindow::RegisterHotKeys(py::iterable &items)
{
	for (auto e : items)
	{
		const py::tuple &item = e.cast<py::tuple>();
		pyobj key;
		if (py::len(item) >= 4)
		{
			key = item[3];
		}
		else
		{
			try
			{
				key = item[2].attr("__name__");
			}
			catch (py::error_already_set &e)
			{
				e.restore();
				PyErr_Print();
			}
		}
		RegisterHotKey(key, item[0].cast<int>(), item[1].cast<int>(), item[2]);
	}
}

void HotkeyWindow::UnregisterHotKey(pyobj hotkeyId, bool force)
{
	WORD _hotkeyId;
	if (prepareHotkey(hotkeyId, _hotkeyId))
	{
		if (force || m_hotkey_map.contains(hotkeyId))
		{
			ptr()->UnregisterHotKey(_hotkeyId);
		}
	}
}

void HotkeyWindow::stopHotkey()
{
	wxChar buf[32];
	int hotkeyId;
	for (auto e : m_hotkey_map)
	{
		hotkeyId = e.first.cast<WORD>();
		GlobalGetAtomName(hotkeyId, buf, 32);
		if (!wxIsEmpty(buf))
		{
			GlobalDeleteAtom(hotkeyId);
		}
		ptr()->UnregisterHotKey(hotkeyId);
	}
}

void HotkeyWindow::onHotkey(wxKeyEvent & event)
{
	pycref hotkeyId = py::cast(event.GetId());
	pycref ret = pyCall(m_hotkey_map[hotkeyId], hotkeyId);
	if (!PyObject_IsTrue(ret.ptr()))
	{
		event.Skip();
	}
}


void Dialog::__exit__(py::args & args)
{
	Layout::__exit__(args);
	if (getActiveLayout() == nullptr)
	{
		py::cast(this).inc_ref();
	}
}

void Dialog::dismiss(bool ok)
{
	if (isModal())
	{
		endModal(ok);
	}
	else
	{
		win().Hide();
	}
}


/*pyobj StdModalDialog::__enter__()
{
	long style = ptr()->GetWindowStyle();
	style |= wxRESIZE_BORDER | wxCLIP_CHILDREN;
	ptr()->SetWindowStyle(style);

	auto ret = Layout::__enter__();
	wxSizer* topsizer = new wxBoxSizer(wxVERTICAL);
	ptr()->SetSizer(topsizer);
	return ret;
}

void StdModalDialog::__exit__(py::args & args)
{
	wxStdDialogButtonSizer* buttonSizer = new wxStdDialogButtonSizer();
	buttonSizer->AddButton(new wxButton(ptr(), wxID_OK));
	buttonSizer->AddButton(new wxButton(ptr(), wxID_CANCEL));
	buttonSizer->Realize();

	wxSizer* topsizer = ptr()->GetSizer();
	topsizer->Add(buttonSizer, wxSizerFlags(0).Right().Border(wxBOTTOM | wxRIGHT, 5));
	Dialog::__exit__(args);
}*/


void init_frames(py::module & m)
{
	using namespace py::literals;

	auto className = "className"_a = None;
	auto style = "style"_a = None;
	auto styles = "styles"_a = None;
	auto label = "label"_a;
	auto base_frame_init = py::init<wxcstr, MenuBar*, long, pyobj, pyobj, pyobj>();
	auto base_frame_wxstyle_a = "wxstyle"_a = (long)(wxDEFAULT_FRAME_STYLE | wxTAB_TRAVERSAL);
	auto menubar_a = "menubar"_a = nullptr;

	py::class_t<BaseTopLevelWindow, Layout>(m, "BaseTopLevelWindow")
		.def("close", &BaseTopLevelWindow::close)
		.def("setOnClose", &BaseTopLevelWindow::setOnClose)
		.def("setIcon", &BaseTopLevelWindow::setIcon)
		.def_property("title", &BaseTopLevelWindow::getTitle, &BaseTopLevelWindow::setTitle)
		.def_property("size", &BaseTopLevelWindow::getSize, &BaseTopLevelWindow::setSize)
		.def_property("position", &BaseTopLevelWindow::getPosition, &BaseTopLevelWindow::setPosition);
	py::class_t<BaseFrame, BaseTopLevelWindow>(m, "BaseFrame")
		.def_property("keeptop", &Window::isKeepTop, &Window::keepTop)
		.def_property_readonly("menubar", &Window::getMenuBar)
		.def_property_readonly("statusbar", &Window::getStatusBar);

	py::class_t<Window, BaseFrame>(m, "Window")
		.def(base_frame_init, label, menubar_a, base_frame_wxstyle_a, styles, className, style);

	py::class_t<MDIParentFrame, BaseFrame>(m, "MDIParentFrame")
		.def(base_frame_init, label, menubar_a, base_frame_wxstyle_a, styles, className, style);

	py::class_t<MDIChildFrame, BaseFrame>(m, "MDIChildFrame")
		.def(base_frame_init, label, menubar_a, base_frame_wxstyle_a, styles, className, style);

	py::class_t<HotkeyWindow, Window>(m, "HotkeyWindow")
		.def(base_frame_init, label, menubar_a, base_frame_wxstyle_a, styles, className, style)
		.def("RegisterHotKey", &HotkeyWindow::RegisterHotKey, "hotkeyId"_a, "mod"_a, "keycode"_a, "onhotkey"_a)
		.def("RegisterHotKeys", &HotkeyWindow::RegisterHotKeys, "items"_a)
		.def("UnregisterHotKey", &HotkeyWindow::UnregisterHotKey, "hotkeyId"_a, "force"_a = false)
		.def_property_readonly("hotkeys", &HotkeyWindow::getHotkeys);

	py::class_t<Dialog, BaseTopLevelWindow>(m, "Dialog")
		.def(py::init<wxcstr, long, pyobj, pyobj, pyobj>(),
			label, "wxstyle"_a = 0, styles, className, style)
		.def("showModal", &Dialog::showModal)
		.def("endModal", &Dialog::endModal, "ok"_a=true)
		.def("isModal", &Dialog::isModal)
		.def("dismiss", &Dialog::dismiss, "ok"_a=true);
}
