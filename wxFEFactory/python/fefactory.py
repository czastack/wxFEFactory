from modules import modules
import sys
import fefactory_api
import traceback
import imp

class _LogWriter:
    def flush(self):
        pass

    def write(self, s):
        fefactory_api.log_message(s)


sys.stdout = sys.stderr = _LogWriter()

YES    = 0x02
NO     = 0x08
CANCEL = 0x10


def reload(self):
    keys = ['lib', 'modules']

    for name in sys.modules.keys():
        for key in keys:
            if name == key or name.startswith(key + '.'):
                del sys.modules[key]

    fefactory_api.navBar.clear()
    imp.reload(sys.modules[__name__])


import mainframe


# def on_nav(i):
#     """左侧导航栏点击回调"""
#     name = modules[i][0]

#     try:
#         module = getattr(__import__('modules.' + name), name) # , fromlist=['main']
#         module.run()

#     except Exception as e:
#         print('加载模块%s失败' % name)
#         traceback.print_exc()


# fefactory_api.navBar.insertItems(item[1] for item in modules)
# fefactory_api.navBar.setListener(on_nav)

# data = {}
# pg = fefactory_api.PropertyGridListPage('人物')
# # pg2 = fefactory_api.PropertyGrid('人物2')
# pg.addCategory('主角')
# pg.insertItems(['选项1', '选项2', '选项3'])
# pg.setListener(print)
# pg.addStringProperty('姓名', 'name', '角色姓名', '哈哈')
# pg.addHexProperty('HP', 'hp', None, 48)
# pg.addEnumProperty('职业', 'prof', None, ("骑士", "圣骑士"), (0x10, 0x11), 0x11)
# pg.addFlagsProperty('职业2', 'prof2', None, ("骑士", "圣骑士"), None, 3)
# pg.addLongStringProperty('描述', 'desc', None, '温柔的公主')
# pg.addArrayStringProperty('数组', 'test', None, ('第一项','第二项'))
# data = {}
# pg.getValues(data)
# print(data)
# data = {'desc': '善良的公主', 'hp': 60, 'prof2': 2, 'prof': 0x10, 'test': ['no.1', 'no.2'], 'name': '嘻嘻'}
# pg.setValues(data)

# li = fefactory_api.ListView('人物')
# li.appendColumns(('姓名', '编号', 'R键说明'))
# li.insertItems([('艾希', '01', '少女'), ('赛思', 12, '圣骑士')])
# li.insertItems([('艾希', '01', '少女')], 1, False)

# print(fefactory_api.choose_file("选择火纹的Rom", wildcard='*.gba|*.gba|*.zip|*.zip'))

# print(fefactory_api.confirm_dialog('确认关闭', '数据未保存，是否先保存'))

# with open('E:/GBA/火焰之纹章/test/img.bin', 'rb') as bp, open('E:/GBA/rom/palette.bin', 'rb') as pal, open('E:/GBA/rom/testtiles.bin', 'wb') as test:
#     moveArgs = (
#             ( 0, 0, 8, 4, 1, 0 ),
#             ( 8, 0, 8, 4, 1, 4 ),
#             ( 16, 0, 4, 2, 1, 8 ),
#             ( 16, 2, 4, 2, 5, 8 ),
#             ( 21, 1, 1, 3, 0, 7 ),
#             ( 22, 1, 1, 3, 9, 7 ),
#             ( 7, 0, 1, 1, 0, 6 ),
#             ( 7, 0, 1, 1, 9, 6 ),
#         )

#     img = fefactory_api.FeImage()
#     img.create(80, 80, 32, bp.read(), pal.read(), moveArgs)
#     img.fillColor((
#         ( 0, 0, 1, 6 ),
#         ( 9, 0, 1, 6 )
#         ), 0)
#     # img.rescale(320, 320);
#     # img.view('头像')
#     test.write(img.toTiles(80, 80, 32, 4096, moveArgs))

# li = fefactory_api.ListBox('test')
# li.insertItems(item[1] for item in modules)
# li.setListener(print)