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
else:  # elif screen_width <= 3840:
    btn_width = 100
    btn_xs_width = 60
    btn_sm_width = 100
    btn_md_width = 120
    dialog_width = 900
    dialog_height = 640


dialog_style = {'width': dialog_width, 'height': dialog_height}

btn_xs_style = {'width': btn_xs_width}

btn_sm_style = {'width': btn_sm_width}

btn_md_style = {'width': btn_md_width}


# padding-flag: top right bottom left
styles = {
    'class': {
        'fill': {
            'weight': 1,
            'expand': True,
        },
        'grow': {'weight': 1},
        'expand': {'expand': True},
        'vcenter': {'vertical-align': 'middle'},
        'right': {'align': 'right'},
        'button': {
            'weight': 1,
            'width': btn_width,
        },
        'padding': {
            'padding': 10,
            'padding-flag': 1,
        },
        'padding_label': {
            'padding': 8,
            'padding-flag': 0b1101,
        },
        'padding_top': {'padding': 10, 'padding-flag': 0b1000},
        'padding_right': {'padding': 8, 'padding-flag': 0b1110},
        'padding_bottom': {'padding': 10, 'padding-flag': 0b0010},
        'padding_left': {'padding': 10, 'padding-flag': 0b0001},
        'input_label': {
            'padding': 8,
            'padding-flag': 0b1101,
            'text-align': 'right',
        },
        'input_label_vertical': {
            'padding': 5,
            'padding-flag': 0b0010,
        },
        'form_label': {
            'padding': 8,
            'padding-flag': 0b0101,
            'text-align': 'right',
        },
        'btn_xs': btn_xs_style,
        'btn_sm': btn_sm_style,
        'btn_md': btn_md_style,
    }
}
