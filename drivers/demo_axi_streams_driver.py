__author__ = "dmccoy@mit.edu (Dave McCoy)"

from pynq import PL
from .emmio import EMMIO


import sys
import os
import time

from array import array as Array

REG_CONTROL             = 0  << 2
REG_VERSION             = 1  << 2

#Set/Clear a bit
BIT_CTRL_TEST           = 0

#Set/Get a range of bits
BIT_CTRL_TR_HIGH        = 15
BIT_CTRL_TR_LOW         = 8

class DemoAXIStreamsDriver (object):
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
        self.mmio.read(REG_CONTROL, data)

    # Get Entire Register
    def get_control(self):
        data = self.mmio.read(REG_CONTROL)
        return data

    # Set a bit within a register
    def enable_test_mode(self, enable):
        self.mmio.enable_register_bit(REG_CONTROL, BIT_CTRL_TEST, enable)

    # Get a bit within a register
    def is_test_mode(self):
        bit_val = self.self.mmio.is_register_bit_set(REG_CONTROL, BIT_CTRL_TEST)
        return bit_val

    # Set a range of data withing a register
    def set_control_test_range(self, data):
        self.mmio.write_register_bit_range(REG_CONTROL, BIT_CTRL_TR_HIGH, BIT_CTRL_TR_LOW, data)

    # Get a range of data within a register
    def get_control_test_range(self, data):
        data = self.mmio.read_bit_range(REG_CONTROL, BIT_CTRL_TR_HIGH, BIT_CTRL_TR_LOW, data)
        return data

