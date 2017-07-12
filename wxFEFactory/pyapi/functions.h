#pragma once

void log_message(wxcstr text);

int confirm_dialog(wxcstr title, wxcstr msg);

wxString choose_file(wxcstr msg, pycref dir, pycref file, pycref wildcard);

wxString get_clipboard();

void set_clipboard(wxcstr text);
