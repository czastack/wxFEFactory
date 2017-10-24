from ..gta_base.models import ManagedModel


class BaseBlip(ManagedModel):
    MARKER_TYPE_CAR = 1
    MARKER_TYPE_PED = 2
    MARKER_TYPE_OBJECT = 3
    MARKER_TYPE_COORDS = 4
    MARKER_TYPE_CONTACT = 5
    AVAILABLE_TYPE = (MARKER_TYPE_CAR, MARKER_TYPE_PED)

    MARKER_COLOR_DARK_RED = 0
    MARKER_COLOR_LIGHT_GREEN = 1
    MARKER_COLOR_WHITE = 2
    MARKER_COLOR_YELLOW = 4
    MARKER_COLOR_PINK = 5
    MARKER_COLOR_CYAN = 6
    MARKER_COLOR_BLACK = 7

    @property
    def entity(self):
        blipType = self.blipType
        index = self.entity_handle >> 8
        if blipType is __class__.MARKER_TYPE_CAR:
            return self.mgr.vehicle_pool[index]
        elif blipType is __class__.MARKER_TYPE_PED:
            return self.mgr.ped_pool[index]
        elif blipType is __class__.MARKER_TYPE_OBJECT:
            return self.mgr.object_pool[index]