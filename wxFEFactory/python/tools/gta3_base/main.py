from functools import partial
from ..gta_base.main import BaseGTATool
import fefactory_api
ui = fefactory_api.ui


class BaseGTA3Tool(BaseGTATool):
    def init_remote_function(self):
        super().init_remote_function()
        
        script_ctx_addr = self.handler.alloc_memory(self.RunningScript.SIZE)
        self.script_context = self.RunningScript(script_ctx_addr, self, 
            self.address.SCRIPT_SPACE_BASE, self.address.FUNC_CRunningScript_ProcessOneCommand)

    def free_remote_function(self):
        super().free_remote_function()
        del self.script_context

    def script_call(self, command_id, signature, *args):
        """执行一条脚本"""
        if self.handler.active:
            return self.script_context.run(command_id, signature, *args)

    def render_common_button(self):
        super().render_common_button()
        ui.Button("瞬移到目的地(粉红)", onclick=partial(self.teleport_to_destination, color=5))
        ui.Button("瞬移到目的地(黄)", onclick=partial(self.teleport_to_destination, color=4))
        ui.Button("敌人爆炸", onclick=self.enemys_explode)

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
        self.script_call(0x20C, '3fL', *coord, explosionType)

    def enemys_explode(self, _=None):
        """敌人爆炸"""
        for e in self.get_enemys():
            self.create_explosion(e.coord)

    def spawn_vehicle(self, model_id):
        self.load_model(model_id)
        self.script_call(0xa5, 'L3fP', model_id, *self.get_front_coord(), self.native_context.get_temp_addr())
        vehicle_handle = self.native_context.get_temp_value()
        if vehicle_handle:
            return self.vehicle_pool[vehicle_handle >> 8]