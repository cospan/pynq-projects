#   Copyright (c) 2016, Xilinx, Inc.
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__ = "Yun Rock Qu"
__copyright__ = "Copyright 2016, Xilinx"
__email__ = "pynq_support@xilinx.com"


import os
import sys
import struct
import mmap
import math
#from . import general_const
import numpy as np
from pynq import MMIO


#class EMMIO(MMIO):
class EMMIO(object):
    """ This class exposes API for MMIO read and write.

    Attributes
    ----------
    virt_base : int
        The address of the page for the MMIO base address.
    virt_offset : int
        The offset of the MMIO base address from the virt_base.
    base_addr : int
        The base address, not necessarily page aligned.
    length : int
        The length in bytes of the address range.
    debug : bool
        Turn on debug mode if it is True.
    mmap_file : file
        Underlying file object for MMIO mapping
    mem : mmap
        An mmap object created when mapping files to memory.
    array : numpy.ndarray
        A numpy view of the mapped range for efficient assignment

    """
    def __init__(self, base_addr, length=4, debug=False):
        """Return a new MMIO object.

        Parameters
        ----------
        base_addr : int
            The base address of the MMIO.
        length : int
            The length in bytes; default is 4.
        debug : bool
            Turn on debug mode if it is True; default is False.
        """
        self.mmio = MMIO(base_addr, length)

    def enable_register_bit(self, address, bit, enable):
        """ enable_register_bit
        Pass a bool value to set/clear a bit

        Parameters
        ----------
        address : int
            Address of the register/memory to modify
        bit : int
            Address of bit to set (31 - 0)
        enable :Boolean
            Set or clear a bit

        Returns
        -------
          None

        """
        if enable:
            self.set_register_bit(address, bit)
        else:
            self.clear_register_bit(address, bit)

    def set_register_bit(self, address, bit):
        """ set_register_bit
        Sets an individual bit in a register

        Parameters
        ----------

        address : int
            Address of the register/memory to modify
        bit : int
            Address of bit to set (31 - 0)

        Returns
        -------
          None
        """
        register = self.mmio.read(address)
        bit_mask =  1 << bit
        register |= bit_mask
        self.mmio.write(address, register)

    def clear_register_bit(self, address, bit):
        """clear_register_bit

        Clear an individual bit in a register

        Parameters
        ----------
        address : int
            Address of the register/memory to modify
        bit : int
            Address of bit to set (31 - 0)

        Returns
        -------
            None
        """
        register = self.mmio.read(address)
        bit_mask =  1 << bit
        register &= ~bit_mask
        self.mmio.write(address, register)

    def is_register_bit_set(self, address, bit):
        """is_register_bit_set
        returns true if an individual bit is set, false if clear
        Args:
          address (int): Address of the register/memory to read
          bit (int): Address of bit to check (31 - 0)
        Returns:
          (boolean):
            True: bit is set
            False: bit is not set
        Raises:
          ValueError
        """
        register = self.mmio.read(address)
        bit_mask =  1 << bit
        return ((register & bit_mask) > 0)

    def write_register_bit_range(self, address, high_bit, low_bit, value):
        """Write data to a range of bits within a register
        Register = [XXXXXXXXXXXXXXXXXXXXXXXH---LXXXX]
        Write to a range of bits within ia register

        Parameters
        ----------
        address : int
            Address or the register/memory to write
        high_bit : int
            the high bit of the bit range to edit
        low_bit : int
            the low bit of the bit range to edit
        value : int
            the value to write in the range

        Returns
        -------
            Nothing
        """
        reg = self.mmio.read(address)
        bitmask = (((1 << (high_bit + 1))) - (1 << low_bit))
        reg &= ~(bitmask)
        reg |= value << low_bit
        self.mmio.write(address, reg)

    def read_register_bit_range(self, address, high_bit, low_bit):
        """
        Read a range of bits within a register at address 'address'
        Register = [XXXXXXXXXXXXXXXXXXXXXXXH---LXXXX]
        Read the value within a register, the top bit is H and bottom is L

        Parameters
        ----------
        address : int
            Address or the register/memory to read
        high_bit : int
            the high bit of the bit range to read
        low_bit : int
            the low bit of the bit range to read

        Returns
        -------
            Value within the bitfield
        """

        value = self.mmio.read(address)
        bitmask = (((1 << (high_bit + 1))) - (1 << low_bit))
        value = value & bitmask
        value = value >> low_bit
        return value

    def write_register_bitmask(self, address, bitmask, value):
        """
        Write a range of bits using a bitmask

        Parameters
        ----------
        address : int
            Address or the register/memory to write
        bitmask : int
            bitfield that defines the range of bits
        value : int
            the value to write in the range

        Returns
        -------
            None
        """
        #Get the high bit and low bit
        low_bit = 0
        high_bit = 0
        bm = bitmask
        if bitmask == 0:
            raise ValueError("Bitmask cannot be equal to 0")

        while (bm & 0x01) == 0:
            low_bit += 1
            bm = bm >> 1

        bm = bitmask
        while (bm - 1) > 0:
            high_bit += 1
            bm = bm >> 1

        self.write_register_bit_range(address, high_bit, low_bit, value)

    def read_register_bitmask(self, address, bitmask):
        """
        Write a range of bits using a bitmask

        Parameters
        ----------
        address : int
            Address or the register/memory to write
        bitmask : int
            bitfield that defines the range of bits

        Returns
        -------
            Value within the bitfield
        """
        #Get the high bit and low bit
        low_bit = 0
        high_bit = 0
        bm = bitmask
        if bitmask == 0:
            raise ValueError("Bitmask cannot be equal to 0")

        while (bm & 0x01) == 0:
            low_bit += 1
            bm = bm >> 1

        bm = bitmask
        while (bm - 1) > 0:
            high_bit += 1
            bm = bm >> 1
        return self.read_register_bit_range(address, high_bit, low_bit)

    def write(self, address, data):
        self.mmio.write(address, data)

    def read(self, address):
        return self.mmio.read(address)

    def _debug(self, s, *args):
        """The method provides debug capabilities for this class.

        Parameters
        ----------
        s : str
            The debug information format string
        *args : any
            The arguments to be formatted
        Returns
        -------
        None

        """
        if self.debug:
            print('MMIO Debug: {0}'.format(s.format(*args)))



