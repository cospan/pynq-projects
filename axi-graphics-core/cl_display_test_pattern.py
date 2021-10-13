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
from drivers.test_pattern_generator import TestPatternID
from drivers.axi_graphics import AXIGraphics

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
    ol.download()

    print ("Bitfile downloaded!")

    print ("Starting Video")

    print ("Configuring Timing Controller")
    tc = TimingController("video/timing_generator")
    tc.reset()
    while (not tc.is_reset_done()):
        print (".")

    WIDTH   = tc.get_generator_width()
    HEIGHT  = tc.get_generator_height()
    print ("Image Size (Retrieved from Timing Controller): %d x %d" % (WIDTH, HEIGHT))
    print ("Configuring Test Pattern Generator")
    tpg = TestPatternGenerator("video/v_tpg_0", debug = args.debug)
    tpg.set_image_size(WIDTH, HEIGHT)
    tpg.set_color_format_to_rgb()
    #tpg.set_color_bar_test_pattern()
    #tpg.set_test_pattern(TestPatternID.SOLID_RED)
    #tpg.set_test_pattern(TestPatternID.SOLID_WHITE)
    tpg.set_test_pattern(TestPatternID.SOLID_BLACK)
    #tpg.set_test_pattern(TestPatternID.COLOR_BARS)
    tpg.start()

    SUB_WIN_WIDTH = 640
    SUB_WIN_HEIGHT = 480
    #SUB_WIN_WIDTH = 16
    #SUB_WIN_HEIGHT = 4
    #SUB_WIN_WIDTH = WIDTH
    #SUB_WIN_HEIGHT = HEIGHT

    print ("Configuring Video Mixer")
    vm = VideoMixer("video/v_mix_0", WIDTH, HEIGHT)
    #vm.configure_layer(0, 0, 0, WIDTH, HEIGHT)
    vm.configure_layer(1, 0, 0, SUB_WIN_WIDTH, SUB_WIN_HEIGHT)
    vm.enable_layer(1, True)
    vm.configure_master_layer(WIDTH, HEIGHT)
    #vm.enable_overlay_layer(True)


    if args.debug: print ("Video Mixer Control Register Before Enable: 0x%08X" % vm.get_control())
    vm.start()

    if args.debug: print ("Video Mixer Control Register After Enable: 0x%08X" % vm.get_control())
    print ("Enable Master Layer (Test Pattern) Output")
    vm.enable_master_layer(True)
    if args.debug: print ("VM Settings:")
    if args.debug: print ("  x pos:   %d" % vm.get_layer_x(0))
    if args.debug: print ("  y pos:   %d" % vm.get_layer_y(0))
    if args.debug: print ("  width:   %d" % vm.get_layer_width(0))
    if args.debug: print ("  height:  %d" % vm.get_layer_height(0))
    if args.debug: print ("  scale:   %d" % vm.get_layer_scale(0))
    if args.debug: print ("  alpha:   %d" % vm.get_layer_alpha(0))
    if args.debug: print ("  stride:  %d" % vm.get_layer_stride(0))
    if args.debug: print ("  p1 Addr: %d" % vm.get_layer_plane1_addr(0))
    if args.debug: print ("  p2 Addr: %d" % vm.get_layer_plane2_addr(0))

    if args.debug: print ("Layer Settings: 0x%08X" % vm.get_layer_enable_reg())

    g0 = ol.low_speed.axi_gpio_0
    g0.write(0x0C, 0x01)
    tc.enable(gen_enable = True, use_gen_src = True)
    if args.debug: print ("TC Control Register: 0x%08X" % tc.get_control_reg())

    print ("Interfacing with AXI Graphics Controller: \n")
    print ("%s" % str(ol.ip_dict["video/axi_graphics_0"]))
    ag = AXIGraphics("video/axi_graphics_0", debug = args.debug)
    #print ("AXI Graphics Started: %s" % str(ol.ip_dict["video/axi_graphics"]))
    #time.sleep(0.1)
    #time.sleep(5)
    print ("AXI Graphics Control Register: 0x%08X" % ag.get_control())
    #print ("AXI Graphics: 0x%08X" % ag.get_version())
    ag.set_width(SUB_WIN_WIDTH)
    ag.set_height(SUB_WIN_HEIGHT)
    print ("Size: %d x %d" % (ag.get_width(), ag.get_height()))
    #ag.set_mode(0)  # Black
    #ag.set_mode(1)  # White
    #ag.set_mode(2)  # Red
    #ag.set_mode(3)  # Green
    #ag.set_mode(4)  # Blue
    ag.set_mode(5)  # Color Bars
    #ag.set_mode(6)  # Block
    #ag.set_mode(7)  # Ramp
    ag.set_alpha(0xFF)
    ag.set_ref0_xy(100, 100)
    ag.set_ref1_xy(200, 200)
    ag.set_interval(100)
    ag.enable_rgba_format(True)
    #ag.enable_rgba_format(False)
    ag.enable(True)
    print ("AXI Graphics Control Register: 0x%08X" % ag.get_control())
    #print ("Sleeping for 5 seconds")
    #time.sleep(5)

if __name__ == "__main__":
    main(sys.argv)
