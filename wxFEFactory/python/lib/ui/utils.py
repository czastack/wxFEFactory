

def update_wxparams(data, **kwargs):
    """更新wxWindow初始化参数"""
    wxparams = data.get('wxparams', None)
    if wxparams is None:
        wxparams = {}
    wxparams.update(kwargs)
    data['wxparams'] = wxparams
