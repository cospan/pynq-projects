from pynq import PL
from pynq.lib.video import VideoMode
from pynq.lib.video.dma import _FrameCache
from .emmio import EMMIO
#import fxpmath as fxp
from fxpmath import Fxp


import sys
import os
import time

from array import array as Array



# Fixed Point
DEGREE_SINTEGER_BITS             = 8
DEGREE_FRACTION_BITS             = 2
                                 
SCALE_UINTEGER_BITS              = 6
SCALE_FRACTION_BITS              = 3
                                 
# Registers
REG_ADDR_AP_CTRL                 = 0x00

REG_ADDR_GIE                     = 0x04

REG_ADDR_IER                     = 0x08

REG_ADDR_ISR                     = 0x0C

REG_ADDR_SRC_IMG_P_DATA          = 0x10
REG_BITS_SRC_IMG_P_DATA          = 64

REG_ADDR_DEGREE_DATA             = 0x1C
REG_BITS_DEGREE_DATA             = 11

REG_ADDR_SCALE_DATA              = 0x24
REG_BITS_SCALE_DATA              = 9

REG_ADDR_GRAYCODE_FRAME_SEL_DATA = 0x2C
REG_BITS_GRAYCODE_FRAME_SEL_DATA = 1

REG_ADDR_FRAME_SEL_SRC_DATA      = 0x34
REG_BITS_FRAME_SEL_SRC_DATA      = 8

REG_ADDR_FRAME_SEL_DST_DATA      = 0x3C
REG_BITS_FRAME_SEL_DST_DATA      = 8

REG_ADDR_LINEAR_INTERPOLATE_DATA = 0x44
REG_BITS_LINEAR_INTERPOLATE_DATA = 1

REG_ADDR_START_X_DATA            = 0x4C
REG_BITS_START_X_DATA            = 16

REG_ADDR_START_Y_DATA            = 0x54
REG_BITS_START_Y_DATA            = 16

REG_ADDR_ROT_POS_X_DATA          = 0x80
REG_BITS_ROT_POS_X_DATA          = 16

REG_ADDR_ROT_POS_Y_DATA          = 0x88
REG_BITS_ROT_POS_Y_DATA          = 16

REG_ADDR_SRC_WIDTH_DATA          = 0x90
REG_BITS_SRC_WIDTH_DATA          = 16

REG_ADDR_SRC_HEIGHT_DATA         = 0x98
REG_BITS_SRC_HEIGHT_DATA         = 16

REG_ADDR_DST_WIDTH_DATA          = 0xa0
REG_BITS_DST_WIDTH_DATA          = 16

REG_ADDR_DST_HEIGHT_DATA         = 0xa8
REG_BITS_DST_HEIGHT_DATA         = 16

REG_ADDR_FRAME_ADDRS_BASE        = 0x60
REG_ADDR_FRAME_ADDRS_HIGH        = 0x7F
REG_WIDTH_FRAME_ADDRS            = 32
REG_DEPTH_FRAME_ADDRS            = 5

class VDMARot (object):
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
        self.DEGREE_FXP = Fxp(None, signed=True,  n_word=REG_BITS_DEGREE_DATA, n_frac=DEGREE_FRACTION_BITS)
        #self.DEGREE_FXP = Fxp(None, signed=True,  n_word=DEGREE_SINTEGER_BITS, n_frac=DEGREE_FRACTION_BITS)
        self.SCALE_FXP  = Fxp(None, signed=False, n_word=REG_BITS_SCALE_DATA,  n_frac=SCALE_FRACTION_BITS)
        #self.SCALE_FXP  = Fxp(None, signed=False, n_word=SCALE_UINTEGER_BITS,  n_frac=SCALE_FRACTION_BITS)

    def __del__(self):
        pass
        #if self.frames is not None:
        #    for f in self.frames:
        #        print ("F: %s" % str(f))
        #        f.clear()
        #if self.dst_frames is not None:
        #    for f in self.dst_frames:
        #        print ("F: %s" % str(f))
        #        f.clear()

    # Set an entire Register
    def set_control(self, data):
        self.mmio.write(REG_ADDR_AP_CTRL, data)

    def start_continuous(self):
        self.mmio.write(REG_ADDR_AP_CTRL, 0x81)

    def stop(self):
        self.mmio.write(REG_ADDR_AP_CTRL, 0x00)

    def start_single(self):
        self.mmio.write(REG_ADDR_AP_CTRL, 0x01)

    # Get Entire Register
    def get_control(self):
        data = self.mmio.read(REG_ADDR_AP_CTRL)
        return data

    def generate_internal_frames(self, width, height):
        mode = VideoMode(width, height, 8)
        self.frames = []

        #Generate the source frames
        if self.debug: print ("SRC Buffers")
        for i in range (REG_DEPTH_FRAME_ADDRS):
            fc = _FrameCache(mode, capacity=REG_DEPTH_FRAME_ADDRS, cacheable=0)
            self.frames.append(fc.getframe())
            if self.debug: print ("  Pointer[%d]: 0x%08X" % (i, self.frames[i].physical_address))
            self.set_frame_address(i, self.frames[i].physical_address)

    def enable_graycode_select(self, enable):
        self.mmio.enable_register_bit(REG_ADDR_GRAYCODE_FRAME_SEL_DATA, REG_BITS_GRAYCODE_FRAME_SEL_DATA, enable);

    def is_graycode_select_enabled(self):
        return self.mmio.is_register_bit_set(REG_ADDR_GRAYCODE_FRAME_SEL_DATA, REG_BITS_GRAYCODE_FRAME_SEL_DATA)

    def set_src_frame_index(self, frame_index):
        self.mmio.write(REG_ADDR_FRAME_SEL_SRC_DATA, frame_index)

    def get_src_frame_index(self):
        return self.mmio.read(REG_ADDR_FRAME_SEL_SRC_DATA)

    def set_dst_frame_index(self, frame_index):
        self.mmio.write(REG_ADDR_FRAME_SEL_DST_DATA, frame_index)

    def get_dst_frame_index(self):
        return self.mmio.read(REG_ADDR_FRAME_SEL_DST_DATA)

    def enable_linear_interpolate(self, enable):
        self.mmio.enable_register_bit(REG_ADDR_LINEAR_INTERPOLATE_DATA, REG_BITS_LINEAR_INTERPOLATE_DATA, enable)

    def is_linear_interpolate_enabled(self):
        return self.mmio.is_register_bit_set(REG_ADDR_LINEAR_INTERPOLATE_DATA, REG_BITS_LINEAR_INTERPOLATE_DATA)

    def set_rotation_degree(self, degree):
        if self.debug: print ("In set_rotation_degress")
        fixed_degree = int(self.DEGREE_FXP(degree).raw())
        if self.debug: print("  Convert %f -> %d, Signed: %s, Num Bits: %d, Factional Bits: %d" % (degree, fixed_degree, "True", DEGREE_SINTEGER_BITS, DEGREE_FRACTION_BITS))
        self.mmio.write(REG_ADDR_DEGREE_DATA, fixed_degree)

    def get_rotation_degree(self):
        if self.debug: print ("In get_rotation_degress")
        fixed_degree = self.mmio.read(REG_ADDR_DEGREE_DATA)
        self.DEGREE_FXP.set_val(fixed_degree, raw=True)
        degree = float(self.DEGREE_FXP)
        if self.debug: print("  Convert %d -> %f, Signed: %s, Num Bits: %d, Factional Bits: %d" % (fixed_degree, degree, "True", DEGREE_UINTEGER_BITS, DEGREE_FRACTION_BITS))
        #return float(self.DEGREE_FXP)
        return float(degree)

    def set_scale(self, scale):
        fixed_scale = int(self.SCALE_FXP(scale).raw())
        if self.debug: print("Convert %f -> %d, Signed: %s, Num Bits: %d, Factional Bits: %d" % (scale, fixed_scale, "False", REG_BITS_SCALE_DATA, SCALE_FRACTION_BITS))
        self.mmio.write(REG_ADDR_SCALE_DATA, fixed_scale)

    def get_scale(self):
        fixed_scale = self.mmio.read(REG_ADDR_SCALE_DATA)
        self.SCALE_FXP.set_val(fixed_scale, raw=True)
        scale = float(self.SCALE_FXP)
        if self.debug: print("Convert %d -> %f, Signed: %s, Num Bits: %d, Factional Bits: %d" % (fixed_scale, scale, "False", REG_BITS_SCALE_DATA, SCALE_FRACTION_BITS))
        return float(self.SCALE_FXP)

    def set_src_frame_pos(self, x, y):
        self.mmio.write(REG_ADDR_START_X_DATA, x)
        self.mmio.write(REG_ADDR_START_Y_DATA, y)

    def get_src_frame_pos(self):
        x = self.mmio.read(REG_ADDR_START_X_DATA)
        y = self.mmio.write(REG_ADDR_START_Y_DATA)
        return (x, y)

    def set_rotation_pos(self, x, y):
        self.mmio.write(REG_ADDR_ROT_POS_X_DATA, x)
        self.mmio.write(REG_ADDR_ROT_POS_Y_DATA, y)

    def get_rotation_pos(self):
        x = self.mmio.read(REG_ADDR_ROT_POS_X_DATA)
        y = self.mmio.write(REG_ADDR_ROT_POS_Y_DATA)
        return (x, y)

    def set_src_size(self, width, height):
        self.mmio.write(REG_ADDR_SRC_WIDTH_DATA, width)
        self.mmio.write(REG_ADDR_SRC_HEIGHT_DATA, height)

    def get_src_size(self):
        width  = self.mmio.read(REG_ADDR_SRC_WIDTH_DATA)
        height = self.mmio.write(REG_ADDR_SRC_HEIGHT_DATA)
        return (width, height)

    def set_dst_size(self, width, height):
        self.mmio.write(REG_ADDR_DST_WIDTH_DATA, width)
        self.mmio.write(REG_ADDR_DST_HEIGHT_DATA, height)

    def get_dst_size(self):
        width  = self.mmio.read(REG_ADDR_DST_WIDTH_DATA)
        height = self.mmio.write(REG_ADDR_DST_HEIGHT_DATA)
        return (width, height)

    def set_frame_address(self, frame_index, frame_address):
        if frame_index >= REG_DEPTH_FRAME_ADDRS:
            raise IndexError("Requested Frame Index: %d is out of range: %d" % (frame_index, REG_DEPTH_FRAME_ADDRS))
        self.mmio.write(REG_ADDR_FRAME_ADDRS_BASE + frame_index * 4, frame_address)

    def get_frame_address(self, frame_index):
        if frame_index >= REG_DEPTH_FRAME_ADDRS:
            raise IndexError("Requested Frame Index: %d is out of range: %d" % (frame_index, REG_DEPTH_FRAME_ADDRS))
        return self.mmio.read(REG_ADDR_FRAME_ADDRS_BASE + frame_index * 4)

    def get_frame_address_count(self):
        return REG_DEPTH_FRAME_ADDRS

    def get_frame(self, frame_index):
        if frame_index >= len(self.frames):
            raise IndexError("Requested Frame Index: %d is out of range: %d, frames were not initialized" % (frame_index, len(self.frames)))
        return self.frames[frame_index]
