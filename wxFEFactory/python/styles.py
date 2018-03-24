import fefactory

screen_width = fefactory.Screen.width

if screen_width <= 1920:
    btn_width = 50
    btn_xs_width = 36
    btn_sm_width = 50
    btn_md_width = 80
    dialog_width = 640
    dialog_height = 480
elif screen_width <= 2560:
    btn_width = 80
    btn_xs_width = 50
    btn_sm_width = 80
    btn_md_width = 100
    dialog_width = 800
    dialog_height = 600
else: # elif screen_width <= 3840:
    btn_width = 100
    btn_xs_width = 60
    btn_sm_width = 100
    btn_md_width = 120
    dialog_width = 900
    dialog_height = 640


dialog_style = {'width': dialog_width, 'height': dialog_height}

btn_xs_style = {
    'width': btn_xs_width,
}

btn_sm_style = {
    'width': btn_sm_width,
}

btn_md_style = {
    'width': btn_md_width,
}


styles = {
    'class': {
        'fill': {
            'flex': 1,
            'expand': True,
        },
        'grow': {'flex': 1},
        'expand': {'expand': True},
        'vcenter': {'verticalAlign': 'middle'},
        'right': {'align': 'right'},
        'button': {
            'flex': 1,
            'width': btn_width,
        },
        'container': {
            'padding': 10,
            'showPadding': '1',
        },
        'input_label': {
            'padding': 8,
            'showPadding': '1 1 0 1',
            'textAlign': 'right',
        },
        'form_label': {
            'padding': 8,
            'showPadding': '0 1 0 1',
            'textAlign': 'right',
        },
        'top_padding': {'padding': 10, 'showPadding': '1 0 0 0'},
        'left_padding': {'padding': 10, 'showPadding': '0 0 0 1'},
        'btn_xs': btn_xs_style,
        'btn_sm': btn_sm_style,
        'btn_md': btn_md_style,
    }
}