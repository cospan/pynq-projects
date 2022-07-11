from pynq import PL
from pynq.lib.video import VideoMode
from pynq.lib.video.dma import _FrameCache
from .emmio import EMMIO
#import fxpmath as fxp
from array import array as Array

import sys
import os
import time

__author__ = "<your@email.here>"

REG_CONTROL             = 0x00
REG_STATUS              = 0x04
REG_CLK_PERIOD          = 0x08
REG_TOTAL_FRAMES        = 0x0C
REG_FRAMES_PER_SECOND   = 0x10
REG_LINES_PER_FRAME     = 0x14
REG_PIXELS_PER_ROW      = 0x18
REG_VERSION             = 0x1C

#Set/Clear a bit
BIT_CTRL_RESET_FRAME_COUNTS     = 0

BIT_STS_FRAME_DETECTED          = 0
BIT_STS_ROWS_NOT_EQUAL          = 1
BIT_STS_LINES_NOT_EQUAL         = 2

class FPSCounterDriver (object):
    def __init__(self, name, debug = False):
        if name not in PL.ip_dict:
            print ("No such %s" % name)

        base_addr   = PL.ip_dict[name]["phys_addr"]
        addr_length = PL.ip_dict[name]["addr_range"]
        self.frames = []
        self.debug = debug
        if debug: print("Base Addr:           0x%08X" % base_addr)
        if debug: print("Address Length:      0x%08X" % addr_length)
        self.mmio = EMMIO(base_addr, addr_length, debug)

    def __del__(self):
        pass

    def get_version(self):
        data = self.mmio.read(REG_VERSION)
        return data

    def are_rows_equal(self):
        data = self.mmio.is_register_bit_set(REG_STATUS, BIT_STS_ROWS_NOT_EQUAL)
        self.mmio.set_register_bit(REG_STATUS, BIT_STS_ROWS_NOT_EQUAL)
        return data

    def are_lines_equal(self):
        data = self.mmio.is_register_bit_set(REG_STATUS, BIT_STS_LINES_NOT_EQUAL)
        self.mmio.set_register_bit(REG_STATUS, BIT_STS_LINES_NOT_EQUAL)
        return (not data)

    def is_frame_detected(self):
        data = self.mmio.is_register_bit_set(REG_STATUS, BIT_STS_FRAME_DETECTED)
        self.mmio.set_register_bit(REG_STATUS, BIT_STS_FRAME_DETECTED)
        return (not data)

    def set_clock_frequency(self, frequency):
        self.mmio.write(REG_CLK_PERIOD, frequency)

    def get_clock_frequency(self):
        return self.mmio.read(REG_CLK_PERIOD)

    def reset_frame_counts(self, enable):
        self.mmio.enable_register_bit(REG_CONTROL, BIT_CTRL_RESET_FRAME_COUNTS, enable)

    def get_total_frames(self):
        data = self.mmio.read(REG_TOTAL_FRAMES)
        return data

    def get_frames_per_second(self):
        data = self.mmio.read(REG_FRAMES_PER_SECOND)
        return data

    def get_lines_per_frame(self):
        data = self.mmio.read(REG_LINES_PER_FRAME)
        return data

    def get_pixels_per_row(self):
        data = self.mmio.read(REG_PIXELS_PER_ROW)
        return data

