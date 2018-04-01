#pragma once

void log_message(wxcstr text);

void alert(wxcstr title, wxcstr msg);
int confirm_dialog(wxcstr title, wxcstr msg, int defaultButton = wxYES);
pyobj input_dialog(wxcstr title, wxcstr msg, wxcstr defaultValue=wxNoneString);
pyobj longtext_dialog(wxcstr title, wxcstr defaultValue=wxNoneString, bool readonly=false, bool sm=false);

wxString choose_file(wxcstr msg, pycref dir, pycref file, pycref wildcard, bool mustExist);
wxString choose_dir(wxcstr msg, pycref defaultPath, bool mustExist);

wxString get_clipboard();
void set_clipboard(wxcstr text);

void exec_file(py::str file, pyobj scope);

py::bytes mem_read(size_t address, size_t size);
void mem_write(size_t address, py::bytes value, size_t size);

wxItemKind getItemKind(wxcstr kindStr);

long getBitmapTypeByExt(wxcstr path);