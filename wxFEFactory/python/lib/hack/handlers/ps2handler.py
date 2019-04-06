from .handler import MemHandler


class Pcsx2Handler(MemHandler):
    CLASS_NAME = 'wxWindowNR'
    WINDOW_NAME = 'PCSX2  1.4.0'

    # RAM
    # 0x00100000-0x01ffffff this is the physical address for the ram.its cached there
    # 0x20100000-0x21ffffff uncached
    # 0x30100000-0x31ffffff uncached & accelerated
    eeMem = 0x20000000

    def attach(self):
        succeed = self.attach_window(self.CLASS_NAME, self.WINDOW_NAME)
        if succeed:
            # with self.raw_env():
            #     self.eeMem = self.read_addr(self.base_addr + 0x8252AC)
            self.eeHw = self.base_addr + 0x828000  # size: 0x10000(64kb)
            self.Main = self.eeMem
            self.ROM = self.eeMem + 0x02004000
            self.ROM1 = self.eeMem + 0x02404000
            self.ROM2 = self.eeMem + 0x02444000
            self.EROM = self.eeMem + 0x024C4000
        return succeed

    def address_map(self, addr):
        if self._raw_addr:
            return addr

        if addr < 0x00100000:
            return self.eeHw + addr

        addr &= 0x0fffffff
        if 0x00100000 <= addr <= 0x01ffffff:
            return self.Main + addr
