#pragma once

void log_message(wxcstr text);

void alert(wxcstr title, wxcstr msg);
int confirm_dialog(wxcstr title, wxcstr msg);
pyobj input_dialog(wxcstr title, wxcstr msg, wxcstr defaultValue=wxNoneString);

wxString choose_file(wxcstr msg, pycref dir, pycref file, pycref wildcard);

wxString get_clipboard();

void set_clipboard(wxcstr text);
