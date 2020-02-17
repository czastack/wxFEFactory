import struct


def fn(data):
    if isinstance(data, int):
        return "0x%X" % data
    elif isinstance(data, bytes):
        return ["0x%X" % item for item in struct.unpack('%dL' % (len(data) / 4), data)]


for field in tool._global_ins.fields:
    if field.__class__.__name__ == 'ToggleFields':
        for subfield in field.fields:
            if subfield.disable == None:
                print(field.label, fn(super(subfield.__class__, subfield).__get__(tool._global_ins, None)))
    elif field.__class__.__name__ == 'ToggleField':
        if field.disable == None:
            print(field.label, fn(super(field.__class__, field).__get__(tool._global_ins, None)))
