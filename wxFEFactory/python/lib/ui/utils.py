

def update_wxparams(data, **kwargs):
    wxparams = data.get('wxparams', None)
    if wxparams is None:
        wxparams = {}
    wxparams.update(kwargs)
    data['wxparams'] = wxparams
