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
from pynq.lib.video import *
from pynq.lib.video.hierarchies import *

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from drivers.video_mixer import VideoMixer
from drivers.dynamic_clock import DynamicClock
from drivers.timing_controller import TimingController
from drivers.test_pattern_generator import TestPatternGenerator
from drivers.axi_graphics import AXIGraphics
from drivers.demo_axi_streams_driver import DemoAXIStreamsDriver
from drivers.sdma import SDMA


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

    name = 'demo_axi_streams_0'
    print ("Checking: %s" % name)
    print ("%s: " % dir(PL.ip_dict))
    print ("Keys %s" % PL.ip_dict.keys())
    #if name not in ol.ip_dict:
    #if name not in PL.ip_dict:
    #    print ("No such %s" % name)
    #    exit(0)
    #exit(0)

    #ol.download()
    #das = DemoAXIStreamsDriver(ol.ip_dict['demo_axi_streams_0'], debug = True)
    das = DemoAXIStreamsDriver('demo_axi_streams_0', debug = True)
    #print (das)
    #print ("Control: 0x%08X" % das.get_control())
    sdma = SDMA('axi_dma_0', 'axi_bram_ctrl_0', 0x00, debug = True)



if __name__ == "__main__":
    main(sys.argv)


