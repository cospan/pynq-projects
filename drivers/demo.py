from pynq import PL
from .emmio import EMMIO


import sys
import os
import time

from array import array as Array

REG_CONTROL             = 0  << 2
REG_VERSION             = 1  << 2

class Demo (object):
    def __init__(self, name, debug = False):
        if name not in PL.ip_dict:
            print ("No such %s" % name)

        base_addr   = PL.ip_dict[name]["phys_addr"]
        addr_length = PL.ip_dict[name]["addr_range"]
        self.debug = debug
        if debug: print("Base Addr:           0x%08X" % base_addr)
        if debug: print("Address Length:      0x%08X" % addr_length)
        self.mmio = EMMIO(base_addr, addr_length, debug)

    def __del__(self):
        pass

    def get_version(self):
        data = self.mmio.read(REG_VERSION)
        return data

    # Set an entire Register
    def set_control(self, data):
        self.mmio.write(REG_CONTROL, data)

    # Get Entire Register
    def get_control(self):
        data = self.mmio.read(REG_CONTROL)
        return data


