__author__ = "dmccoy@mit.edu (Dave McCoy)"

from pynq import PL
from .emmio import EMMIO

from array import array as Array

REG_CONTROL                 =   0 << 2
REG_MASTER_MUX_START_BASE   =   0x040
DISABLE_MASK                =   0x80000000
CONTROL_UPDATE              =   2

class AXISInterconnect (object):
    def __init__(self, name, debug = False):
        if name not in PL.ip_dict:
            print ("No such %s" % name)

        base_addr   = PL.ip_dict[name]["phys_addr"]
        addr_length = PL.ip_dict[name]["addr_range"]

        self.debug = debug
        if debug: print("Base Addr:           0x%08X" % base_addr)
        if debug: print("Address Length:      0x%08X" % addr_length)
        self.mmio = EMMIO(base_addr, addr_length, debug)
        for i in range (16):
            self.mmio.write(REG_MASTER_MUX_START_BASE + 4 * i, DISABLE_MASK)
        self.mmio.write(REG_CONTROL, CONTROL_UPDATE)

    def __del__(self):
        pass

    def disable_all_routes(self):
        for i in range(16):
            self.mmio.write(REG_MASTER_MUX_START_BASE + 4 * i, DISABLE_MASK)
        self.mmio.write(REG_CONTROL, CONTROL_UPDATE)

    def set_route(self, source_index, master_index):
    #def set_route(self, master_index, source_index):
        self.mmio.write(REG_MASTER_MUX_START_BASE + 4 * master_index, source_index)
        self.mmio.write(REG_CONTROL, CONTROL_UPDATE)

    def disable_video_source(master_index):
        self.mmio.write(REG_MASTER_MUX_START_BASE + 4 * master_index, DISABLE_MASK)

    def get_video_source(master_index):
        return self.mmio.read(MASTER_MUX_START_BASE + 4 * master_index)
