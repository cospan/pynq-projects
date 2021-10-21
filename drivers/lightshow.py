

__author__ = "<your@email.here>"

from pynq import PL
from .emmio import EMMIO

import sys
import os
import time

from array import array as Array

REG_CONTROL       = 0 << 2
REG_CLK_DIV	  = 1 << 2
REG_RGB0_COLOR    = 2 << 2
REG_RGB1_COLOR    = 3 << 2
REG_ST_CTRL       = 4 << 2
REG_ST_COUNT      = 5 << 2
REG_ST_PWM_LEN    = 6 << 2
REG_ST_TRANS_LEN  = 7 << 2
REG_VERSION       = 8 << 2

#Set/Clear a bit
BIT_CTRL_EN             = 0
BIT_CTRL_AUTO           = 1

#Set/Get a range of bits
BIT_CTRL_TR_HIGH        = 15
BIT_CTRL_TR_LOW         = 8

class Lightshow (object):
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

    # Set an entire Register
    def set_clk_div(self, data):
        self.mmio.write(REG_CLK_DIV, data)

    # Set an entire Register
    def get_clk_div(self):
        data = self.mmio.read(REG_CLK_DIV)
        return data

    # Set a bit within a register
    def enable_rgb(self, enable):
        self.mmio.enable_register_bit(REG_CONTROL, BIT_CTRL_EN, enable)

    # Set a bit within a register
    def enable_auto(self, enable):
        self.mmio.enable_register_bit(REG_CONTROL, BIT_CTRL_AUTO, enable)

    # Set an entire Register
    def set_state_pwm_length(self, data):
        self.mmio.write(REG_ST_PWM_LEN, data)

    # Set an entire Register
    def set_state_transition_length(self, data):
        self.mmio.write(REG_ST_TRANS_LEN, data)


    # Set an entire Register
    def set_state_color(self, index, color):
        data = 0x00
        data |= index << 24
        data |= color
        self.mmio.write(REG_ST_CTRL, data)

    # Set an entire Register
    def set_state_count(self, count):
        self.mmio.write(REG_ST_COUNT, count)

    # Set Color
    def set_manual_color(self, color):
        self.mmio.write(REG_RGB0_COLOR, color)


    # Get a bit within a register
    def is_enable(self):
        bit_val = self.mmio.is_register_bit_set(REG_CONTROL, BIT_CTRL_EN)
        return bit_val
