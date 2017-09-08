import fefactory_api


class BaseGTATool:
    def go_prev_pos(self, _=None):
        view = self.vehicle_coord_view if self.isInVehicle else self.coord_view
        view.listbox.prev()
        view.write()

    def go_next_pos(self, _=None):
        view = self.vehicle_coord_view if self.isInVehicle else self.coord_view
        view.listbox.next()
        view.write()

    def g3l2json(self, btn=None):
        """g3l坐标转json"""
        path = fefactory_api.choose_file("选择要读取的文件", wildcard='*.g3l')
        if path:
            with open(path) as file:
                if not file.readline().strip() == '[Locks]':
                    fefactory_api.alert('不支持的格式')
                    return

                coord = [0, 0, 0]
                datas = []
                while True:
                    line = file.readline()
                    if not line:
                        break
                    line = line.strip()
                    if line.startswith('x='):
                        coord[0] = float(line[2:])
                    elif line.startswith('y='):
                        coord[1] = float(line[2:])
                    elif line.startswith('z='):
                        coord[2] = float(line[2:])
                    elif line.startswith('desc='):
                        datas.append({'name': line[5:], 'value': tuple(coord)})

            jsonpath = path[:path.rfind('.') + 1] + 'json'
            with open(jsonpath, 'w', encoding="utf-8") as file:
                json.dump(datas, file, ensure_ascii=False)

            fefactory_api.alert('转换成功: ' + jsonpath)