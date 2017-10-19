#include <wx/wx.h>
#include "aui.h"
#include "layouts.h"

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
		if (data != None)
		{
			info.Name(data.cast<wxString>());
		}

		data = pyDictGet(item->m_kwargs, wxT("direction"));
		if (data != None)
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
		if (data != None)
		{
			info.Caption(data.cast<wxString>());
		}

		if (!pyDictGet(item->m_kwargs, wxT("closeButton"), false))
		{
			info.CloseButton(false);
		}

		data = pyDictGet(item->m_kwargs, wxT("maximizeButton"));
		if (data != None)
		{
			info.MaximizeButton(data.cast<bool>());
		}

		data = pyDictGet(item->m_kwargs, wxT("minimizeButton"));
		if (data != None)
		{
			info.MinimizeButton(data.cast<bool>());
		}

		data = pyDictGet(item->m_kwargs, wxT("captionVisible"));
		if (data != None)
		{
			info.CaptionVisible(data.cast<bool>());
		}

		data = pyDictGet(item->m_kwargs, wxT("row"));
		if (data != None)
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
	else
	{
		log_message(wxString::Format("Child of %s must be AuiItem.", "AuiManager"));
	}
}

void AuiManager::__exit__(py::args & args)
{
	Layout::__exit__(args);
	layout();

	// 引用加一，避免被析构
	pyobj &self = py::cast(this);
	self.inc_ref();
}

void AuiNotebook::doAdd(View & child)
{
	AuiItem *item = (AuiItem*)child.ptr()->GetClientData();
	if (isPyDict(item->m_kwargs))
	{
		// 替换回原指针
		child.ptr()->SetClientData(&child);

		wxcstr caption = pyDictGet(item->m_kwargs, wxT("caption"), wxNoneString);
		ctrl().AddPage(child, caption);

		pycref onclose = pyDictGet(item->m_kwargs, wxT("onclose"));
		if (onclose != None)
		{
			m_close_listeners[py::cast(&child)] = onclose;
		}

		py::cast(item).dec_ref();
	}
	else
	{
		log_message(wxString::Format("Child of %s must be AuiItem.", "AuiNotebook"));
	}
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

	if (onclose != None)
	{
		ret = PyObject_IsTrue(pyCall(onclose).ptr()) != 0;
		if (ret)
		{
			m_close_listeners.attr("pop")(page);
		}
	}

	if (ret) {
		// 手动调用子窗口的onClose
		if (py::isinstance<BaseFrame>(page))
		{
			page.cast<BaseFrame*>()->onClose(wxCloseEvent());
		}
	}

	return ret;
}

