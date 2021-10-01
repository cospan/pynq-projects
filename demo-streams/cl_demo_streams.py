#! /usr/bin/env python3

# Copyright (c) 2021 Dave McCoy (dave.mccoy@cospandesign.com)
#
# NAME is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# NAME is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NAME; If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import argparse
import warnings
import time
from pynq import PL
from pynq import Overlay
from pynq import allocate
from pynq.lib.dma import DMA

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from drivers.demo_axi_streams_driver import DemoAXIStreamsDriver


NAME = os.path.basename(os.path.realpath(__file__))

DESCRIPTION = "\n" \
              "\n" \
              "usage: %s [options]\n" % NAME

EPILOG = "\n" \
         "\n" \
         "Examples:\n" \
         "\tSomething\n" \
         "\n"

def main(argv):
    #Parse out the commandline arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION,
        epilog=EPILOG
    )

    parser.add_argument("-t", "--test",
                        nargs=1,
                        default=["something"])

    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="Enable Debug Messages")

    args = parser.parse_args()
    print ("Running Script: %s" % NAME)

    if args.debug:
        print ("test: %s" % str(args.test[0]))

    BF = os.path.join("./data/system_wrapper.bit")

    if not os.path.exists(BF):
        print ("%s Doesn't exist Exiting!!" % BF)
        return
    else:
        print ("Found bit file!")

    ol = Overlay(BF)

    BUFFER_SIZE = 16
    name = 'demo_axi_streams_0'
    print ("Checking: %s" % name)
    #print ("%s: " % dir(PL.ip_dict))
    #print ("Keys %s" % PL.ip_dict.keys())
    das = DemoAXIStreamsDriver('demo_axi_streams_0', debug = True)
    print ("Demo AXIStreamsDriver Version: 0x%08X" % das.get_version())

    dma_writer = DMA(PL.ip_dict["axi_dma_writer"])
    dma_reader = DMA(PL.ip_dict["axi_dma_reader"])
    sbuffer = allocate([1, BUFFER_SIZE], dtype='u4')
    rbuffer = allocate([1, BUFFER_SIZE], dtype='u4')

    for i in range(BUFFER_SIZE):
        sbuffer[0][i] = i

    print ("rbuffer: %s" % str(rbuffer))

    dma_writer.set_up_tx_channel()
    dma_writer.sendchannel.transfer(sbuffer, start = 0, nbytes=BUFFER_SIZE * 4)
    dma_writer.sendchannel.start()
    dma_writer.sendchannel.wait()


    dma_reader.set_up_rx_channel()
    buf = [0] * BUFFER_SIZE
    dma_reader.recvchannel.transfer(rbuffer, start = 0, nbytes=BUFFER_SIZE * 4)
    dma_reader.recvchannel.start()
    dma_reader.recvchannel.wait_async()

    print ("rbuffer: %s" % str(rbuffer))

    if sbuffer is not None:
        sbuffer.freebuffer()

    if rbuffer is not None:
        rbuffer.freebuffer()

if __name__ == "__main__":
    main(sys.argv)
