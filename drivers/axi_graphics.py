__author__ = "dmccoy@mit.edu (Dave McCoy)"

from pynq import PL
from .emmio import EMMIO

import sys
import os
import time

from array import array as Array

REG_CONTROL             =  0 << 2
REG_STATUS              =  1 << 2
REG_WIDTH               =  2 << 2
REG_HEIGHT              =  3 << 2
REG_INTERVAL            =  4 << 2
REG_MODE_SEL            =  5 << 2
REG_XY_REF0             =  6 << 2
REG_XY_REF1             =  7 << 2
REG_FG_COLOR_REF        =  8 << 2
REG_BG_COLOR_REF        =  9 << 2
REG_ALPHA               = 10 << 2

REG_VERSION             = 20 << 2

BIT_CTRL_ENABLE         = 0
BIT_CTRL_RGBA_FORMAT    = 1

class AXIGraphics (object):
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

    def get_control(self):
        data = self.mmio.read(REG_CONTROL)
        return data

    def set_control(self, data):
        self.mmio.write(REG_CONTROL, data)

    def enable(self, enable):
        self.mmio.enable_register_bit(REG_CONTROL, BIT_CTRL_ENABLE, enable)

    def is_enable(self):
        data = self.mmio.is_register_bit_set(REG_CONTROL, BIT_CTRL_ENABLE)
        return data

    def enable_rgba_format(self, enable):
        self.mmio.enable_register_bit(REG_CONTROL, BIT_CTRL_RGBA_FORMAT, enable)

    def is_rgba_format_enabled(self):
        return self.mmio.is_register_bit_set(REG_CONTROL, BIT_CTRL_RGBA_FORMAT)

    def set_alpha(self, alpha):
        self.mmio.write(REG_ALPHA, alpha)

    def get_status(self):
        data = self.mmio.read(REG_STATUS)
        return data

    def set_width(self, width):
        self.mmio.write(REG_WIDTH, width)

    def get_width(self):
        data = self.mmio.read(REG_WIDTH)
        return data

    def set_height(self, height):
        self.mmio.write(REG_HEIGHT, height)

    def get_height(self):
        data = self.mmio.read(REG_HEIGHT)
        return data

    def set_interval(self, interval):
        self.mmio.write(REG_INTERVAL, interval)

    def get_interval(self):
        data = self.mmio.read(REG_INTERVAL)
        return data

    def set_mode(self, mode):
        self.mmio.write(REG_MODE_SEL, mode)

    def get_mode(self):
        data = self.mmio.read(REG_MODE_SEL)
        return data

    def set_ref0_xy(self, x, y):
        data = (y << 16) | (x << 0)
        self.mmio.write(REG_XY_REF0, data)

    def get_ref0_xy(self):
        data = self.mmio.read(REG_XY_REF0)
        x = (data >>  0) & 0x0FFF
        y = (data >> 16) & 0x0FFF
        return (x, y)

    def set_ref1_xy(self, x, y):
        data = (y << 16) | (x << 0)
        self.mmio.write(REG_XY_REF1, data)

    def get_ref1_xy(self):
        data = self.mmio.read(REG_XY_REF1)
        x = (data >>  0) & 0x0FFF
        y = (data >> 16) & 0x0FFF
        return (x, y)

    def set_fg_color(self, fg_color):
        self.mmio.write(REG_FG_COLOR_REF, fg_color)

    def get_fg_color(self):
        data = self.mmio.read(REG_FG_COLOR_REF)
        return data

    def set_bg_color(self, bg_color):
        self.mmio.write(REG_BG_COLOR_REF, bg_color)

    def get_bg_color(self):
        data = self.mmio.read(REG_BG_COLOR_REF)
        return data





