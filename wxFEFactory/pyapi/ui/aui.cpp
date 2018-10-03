#include <wx/wx.h>
#include "aui.h"


void AuiManager::doAdd(View & child)
{
	AuiItem *item = (AuiItem*)child.ptr()->GetClientData();
	if (isPyDict(item->m_kwargs))
	{
		wxAuiPaneInfo info;

		// 替换回原指针
		child.ptr()->SetClientData(&child);

		pyobj data;

		data = pyDictGet(item->m_kwargs, wxT("name"));
		if (!data.is(None))
		{
			info.Name(data.cast<wxString>());
		}

		data = pyDictGet(item->m_kwargs, wxT("direction"));
		if (!data.is(None))
		{
			wxcstr direction = data.cast<wxString>();

			if (direction == wxT("top"))
				info.Top();
			else if (direction == wxT("right"))
				info.Right();
			else if (direction == wxT("bottom"))
				info.Bottom();
			else if (direction == wxT("left"))
				info.Left();
			else if (direction == wxT("center"))
				info.Center();
		}

		data = pyDictGet(item->m_kwargs, wxT("caption"));
		if (!data.is(None))
		{
			info.Caption(data.cast<wxString>());
		}

		if (!pyDictGet(item->m_kwargs, wxT("closeButton"), false))
		{
			info.CloseButton(false);
		}

		data = pyDictGet(item->m_kwargs, wxT("maximizeButton"));
		if (!data.is(None))
		{
			info.MaximizeButton(data.cast<bool>());
		}

		data = pyDictGet(item->m_kwargs, wxT("minimizeButton"));
		if (!data.is(None))
		{
			info.MinimizeButton(data.cast<bool>());
		}

		data = pyDictGet(item->m_kwargs, wxT("captionVisible"));
		if (!data.is(None))
		{
			info.CaptionVisible(data.cast<bool>());
		}

		data = pyDictGet(item->m_kwargs, wxT("row"));
		if (!data.is(None))
		{
			info.Row(data.cast<int>());
		}

		if (pyDictGet(item->m_kwargs, wxT("hide"), false))
		{
			info.Hide();
		}

		m_mgr->AddPane(child, info);

		py::cast(item).dec_ref();
	}
	/*else
	{
		log_message(wxString::Format("Child of %s must be AuiItem.", "AuiManager"));
	}*/
}

void AuiManager::__exit__(py::args & args)
{
	layout();

	// 引用加一，避免被析构
	pyobj &self = py::cast(this);
	self.inc_ref();
	Layout::__exit__(args);
}

void AuiNotebook::doAdd(View & child)
{
	AuiItem *item = (AuiItem*)child.ptr()->GetClientData();
	if (isPyDict(item->m_kwargs))
	{
		// 替换回原指针
		child.ptr()->SetClientData(&child);

		wxcstr caption = pyDictGet(item->m_kwargs, wxT("caption"), wxNoneString);
		child.ptr()->Reparent(NULL);
		ctrl().AddPage(child, caption);

		pycref onclose = pyDictGet(item->m_kwargs, wxT("onclose"));
		if (!onclose.is(None))
		{
			m_close_listeners[py::cast(&child)] = onclose;
		}

		py::cast(item).dec_ref();
	}
	/*else
	{
		log_message(wxString::Format("Child of %s must be AuiItem.", "AuiNotebook"));
	}*/
}

bool AuiNotebook::canPageClose(int n)
{
	if (ctrl().GetPageCount() == 0)
		return false;

	bool ret = true;

	if (n == -1)
		n = ctrl().GetSelection();

	pyobj page = py::cast(getPage(n));
	pyobj onclose = pyDictGet(m_close_listeners, page);

	if (!onclose.is(None))
	{
		ret = PyObject_IsTrue(pyCall(onclose).ptr()) != 0;
		if (ret)
		{
			m_close_listeners.attr("pop")(page);
		}
	}

	if (ret) {
		// 手动调用子窗口的onClose
		if (py::isinstance<BaseTopLevelWindow>(page))
		{
			ret = page.cast<BaseTopLevelWindow*>()->onClose(wxCloseEvent(wxEVT_CLOSE_WINDOW));
		}
	}

	return ret;
}

View * AuiNotebook::getPage(int n)
{
	if (n == -1)
	{
		n = getSelection();
	}
	return (View*)ctrl().GetPage(n)->GetClientData();
}


void AuiNotebook::_removePage(int n)
{
	auto page = py::cast(getPage(n));
	if (m_children.contains(page)) {
		pyCall(m_children.attr("remove"), page);
	}
}

void AuiNotebook::OnPageClose(wxAuiNotebookEvent & event)
{
	auto selection = event.GetSelection();
	if (!canPageClose(selection))
	{
		event.Veto();
	}
	else {
		_removePage(selection);
	}
}

bool AuiNotebook::closePage(int n)
{
	if (n == -1)
	{
		n = getSelection();
	}

	if (canPageClose(n))
	{
		_removePage(n);
		ctrl().DeletePage(n);
		return true;
	}
	return false;
}

bool AuiNotebook::closeAllPage()
{
	for (int i = 0; i < getPageCount(); i++)
	{
		if (!closePage(i))
		{
			return false;
		}
	}
	return true;
}

void AuiMDIParentFrame::onRelease()
{
	wxAuiNotebook * notebook = win().GetNotebook();
	if (notebook)
	{
		/// 关闭所有子窗口.
		notebook->DeleteAllPages();
	}

	m_mgr->UnInit();
	delete m_mgr;

	BaseFrame::onRelease();
}

void init_aui(py::module & m)
{
	using namespace py::literals;

	auto className = "className"_a = None;
	auto style = "style"_a = None;
	auto styles = "styles"_a = None;
	auto label = "label"_a;
	auto base_frame_wxstyle_a = "wxstyle"_a = (long)(wxDEFAULT_FRAME_STYLE | wxTAB_TRAVERSAL);

	py::class_t<AuiMDIParentFrame, BaseFrame>(m, "AuiMDIParentFrame")
		.def(py::init<wxcstr, MenuBar*, long, pyobj, pyobj, pyobj>(), label, "menubar"_a = nullptr, base_frame_wxstyle_a, styles, className, style);

	py::class_t<AuiMDIChildFrame, BaseTopLevelWindow>(m, "AuiMDIChildFrame")
		.def(py::init<wxcstr, long, pyobj, pyobj, pyobj>(), label, base_frame_wxstyle_a, styles, className, style);

	py::class_<AuiManager, Layout>(m, "AuiManager")
		.def(py::init<>())
		.def("showPane", &AuiManager::showPane, "name"_a, "show"_a = true)
		.def("hidePane", &AuiManager::hidePane)
		.def("togglePane", &AuiManager::togglePane);

	auto pyItem = py::class_t<Item>(m, "Item")
		.def(py::init<View&, py::kwargs>(), "view"_a)
		.def("getView", &AuiItem::getView);

	setattr(m, "AuiItem", pyItem);

	py::class_t<AuiNotebook, Layout>(m, "AuiNotebook")
		.def(py::init<pyobj, pyobj, pyobj>(), styles, className, style)
		.def("getPage", &AuiNotebook::getPage, "n"_a = -1)
		.def("closePage", &AuiNotebook::closePage, "n"_a = -1)
		.def("closeAllPage", &AuiNotebook::closeAllPage)
		.def_property("index", &AuiNotebook::getSelection, &AuiNotebook::setSelection)
		.def_property_readonly("count", &AuiNotebook::getPageCount);
}
