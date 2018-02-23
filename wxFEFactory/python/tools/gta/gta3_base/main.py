from functools import partial
from ..gta_base.main import BaseGTATool
from . import opcodes
import fefactory_api
ui = fefactory_api.ui


class BaseGTA3_VC_SA_Tool(BaseGTATool):
    """GTA3, VC, SA公共基类"""

    def init_remote_function(self):
        super().init_remote_function()
        
        script_ctx_addr = self.handler.alloc_memory(self.RunningScript.SIZE)
        self.script_context = self.RunningScript(script_ctx_addr, self, 
            self.address.SCRIPT_SPACE_BASE, self.address.FUNC_CRunningScript__Init, self.address.FUNC_CRunningScript__ProcessOneCommand)

    def free_remote_function(self):
        super().free_remote_function()
        del self.script_context

    def script_call(self, command_id, signature, *args):
        """执行一条脚本"""
        if self.handler.active:
            return self.script_context.run(command_id, signature, *args)

    @property
    def ped_id(self):
        """获取当前角色的句柄"""
        self.script_call(opcodes.GET_PLAYER_CHAR, 'LP', 0, self.native_context.get_temp_addr())
        return self.native_context.get_temp_value()

    @property
    def vehicle_id(self):
        """获取当前载具的句柄"""
        self.script_call(opcodes.STORE_CAR_CHAR_IS_IN_NO_SAVE, 'LP', self.ped_id, self.native_context.get_temp_addr())
        handle = self.native_context.get_temp_value()
        if handle == 0xfd16e500:
            return 0
        return handle

    EXPLOSION_TYPE_GRENADE = 0
    EXPLOSION_TYPE_MOLOTOV = 1
    EXPLOSION_TYPE_ROCKET = 2
    EXPLOSION_TYPE_CAR = 3
    EXPLOSION_TYPE_CAR_QUICK = 4
    EXPLOSION_TYPE_BOAT = 5
    EXPLOSION_TYPE_HELI = 6
    EXPLOSION_TYPE_HELI2 = 7
    EXPLOSION_TYPE_MINE = 8
    EXPLOSION_TYPE_BARREL = 9
    EXPLOSION_TYPE_TANK_GRENADE = 10
    EXPLOSION_TYPE_HELI_BOMB = 11
    def create_explosion(self, coord, explosionType=EXPLOSION_TYPE_ROCKET, radius=5):
        """产生爆炸"""
        # (X, Y, Z, iType, Radius)
        # self.native_call_auto(address.FUNC_AddExplosion, '3fLL', *coord, explosionType, radius)
        self.script_call(opcodes.ADD_EXPLOSION, '3fL', *coord, explosionType)

    def enemys_explode(self, _=None):
        """敌人爆炸"""
        for e in self.get_enemys():
            self.create_explosion(e.coord)

    def spawn_vehicle(self, model_id, coord=None):
        self.load_model(model_id)
        self.script_call(0xa5, 'L3fP', model_id, *(coord or self.get_front_coord()), self.native_context.get_temp_addr())
        vehicle_handle = self.native_context.get_temp_value()
        if vehicle_handle:
            return self.vehicle_pool[vehicle_handle >> 8]

    def freeze_timer(self, _=None, freeze=True):
        """停止计时"""
        self.script_call(opcodes.FREEZE_ONSCREEN_TIMER, 'L', freeze)

    def set_ped_invincible(self, tb):
        """当前角色无伤"""
        on = tb.checked
        self.script_call(opcodes.SET_CHAR_PROOFS, '6L', self.ped_id, on, on, on, on, on)

    def set_vehicle_invincible(self, tb):
        """当前载具无伤"""
        vehicle_id = self.vehicle_id
        if vehicle_id:
            on = tb.checked
            self.script_call(opcodes.SET_CAR_PROOFS, '6L', vehicle_id, on, on, on, on, on)


class BaseGTA3Tool(BaseGTA3_VC_SA_Tool):
    """GTA3, VC公共基类"""

    def render_common_button(self):
        Marker = self.models.Marker
        super().render_common_button()
        ui.Button("敌人爆炸", onclick=self.enemys_explode)
        ui.Button("停止计时", onclick=self.freeze_timer)
        ui.Button("恢复计时", onclick=partial(self.freeze_timer, freeze=False))
        ui.Button("瞬移到目的地(粉红)", onclick=partial(self.teleport_to_destination, color=Marker.MARKER_COLOR_PINK))
        ui.Button("瞬移到目的地(深红)", onclick=partial(self.teleport_to_destination, color=Marker.MARKER_COLOR_DARK_RED))
        ui.Button("瞬移到目的地(黄)", onclick=partial(self.teleport_to_destination, color=Marker.MARKER_COLOR_YELLOW))
        ui.Button("瞬移到目的地(绿)", onclick=partial(self.teleport_to_destination, color=Marker.MARKER_COLOR_LIGHT_GREEN))
