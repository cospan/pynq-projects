#! /usr/bin/env python3

import sys
import os
import argparse
import time
from pynq import PL
from pynq import Overlay

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from drivers.lightshow import Lightshow

NAME = os.path.basename(os.path.realpath(__file__))

DESCRIPTION = "\n" \
              "\n" \
              "usage: %s [options]\n" % NAME

EPILOG = "\n" \
         "\n" \
         "Examples:\n" \
         "\tSomething\n" \
         "\n"

def set_color_intensity(color, intensity = 1.0):
    r = color >> 16 & 0xFF
    g = color >>  8 & 0xFF
    b = color >>  0 & 0xFF
    r *= intensity
    g *= intensity
    b *= intensity
    color = 0x00
    color |= (int(r) & 0xFF) << 16
    color |= (int(g) & 0xFF) << 8
    color |= (int(b) & 0xFF)  << 0
    return color

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
    print ("Download the image...")
    ol.download()
    print ("Downloaded")
    print ("")


    #COLOR_RED         = 0xFF0000
    #COLOR_ORANGE      = 0xFFA500
    #COLOR_YELLOW      = 0xFFFF00
    #COLOR_GREEN       = 0x00FF00
    #COLOR_BLUE        = 0x0000FF
    #COLOR_PURPLE      = 0xA020F0
    #COLOR_WHITE       = 0xFFFFFF
    #COLOR_BLACK       = 0x000000
    #COLOR_TERQUOISE   = 0x00F5FF
    #COLOR_VIOLET      = 0xEE82EE
    #COLOR_STEEL_BL    = 0x63B8FF
    #COLOR_SPRING_GR   = 0x00FF7F
    #COLOR_STATE_BL    = 0x836FFF
    #COLOR_OLIVE_DR1   = 0xC0FF3E
    #COLOR_FORREST_GR  = 0x228B22
    #COLOR_FIRE_BR_RED = 0xFF3030
    #COLOR_DARK_PINK   = 0xFF1493


    COLOR_RED         = 0xFF0000
    COLOR_ORANGE      = 0xFFA500
    COLOR_YELLOW      = 0xFFFF00
    COLOR_GREEN       = 0x00FF00
    COLOR_BLUE        = 0x0000FF
    COLOR_PURPLE      = 0xA020F0
    COLOR_WHITE       = 0xFFFFFF
    COLOR_BLACK       = 0x000000
    COLOR_TERQUOISE   = 0x00F5FF
    COLOR_VIOLET      = 0xEE82EE
    COLOR_STEEL_BL    = 0x63B8FF
    COLOR_SPRING_GR   = 0x00FF7F
    COLOR_STATE_BL    = 0x836FFF
    COLOR_OLIVE_DR1   = 0xC0FF3E
    COLOR_FORREST_GR  = 0x228B22
    COLOR_FIRE_BR_RED = 0xFF3030
    COLOR_DARK_PINK   = 0xFF1493




    name = 'lightshow_0'

    if args.debug: print ("Checking: %s" % name)
    if args.debug: print ("%s: " % dir(PL.ip_dict))
    if args.debug: print ("Keys %s" % PL.ip_dict.keys())
    if name not in PL.ip_dict:
        print ("No such %s" % name)
        exit(0)

    lightshow = Lightshow(name, debug = args.debug)
    print ("Vesion: 0x%08X" % lightshow.get_version())
    #lightshow.set_manual_color(COLOR_DARK_PINK)
    #lightshow.enable_rgb(True)
    print ("Clock Div: %d" % lightshow.get_clk_div())
    #lightshow.set_clk_div(100000000 // 1000 // 256)
    lightshow.set_clk_div(100)
    print ("Clock Div: %d" % lightshow.get_clk_div())

    lightshow.set_state_pwm_length(5000)
    lightshow.set_state_transition_length(12)
    #intensity = 0.10
    intensity = 1.0

    #Make PWM really short at first
    lightshow.set_state_color(0,  set_color_intensity(COLOR_RED,         intensity))
    lightshow.set_state_color(1,  set_color_intensity(COLOR_ORANGE,      intensity))
    lightshow.set_state_color(2,  set_color_intensity(COLOR_YELLOW,      intensity))
    lightshow.set_state_color(3,  set_color_intensity(COLOR_GREEN,       intensity))
    lightshow.set_state_color(4,  set_color_intensity(COLOR_BLUE,        intensity))
    lightshow.set_state_color(5,  set_color_intensity(COLOR_PURPLE,      intensity))
    lightshow.set_state_color(6,  set_color_intensity(COLOR_BLACK,       intensity))
    lightshow.set_state_color(7,  set_color_intensity(COLOR_TERQUOISE,   intensity))
    lightshow.set_state_color(8,  set_color_intensity(COLOR_VIOLET,      intensity))
    lightshow.set_state_color(9,  set_color_intensity(COLOR_STEEL_BL,    intensity))
    lightshow.set_state_color(10, set_color_intensity(COLOR_SPRING_GR,   intensity))
    lightshow.set_state_color(11, set_color_intensity(COLOR_FORREST_GR,  intensity))
    lightshow.set_state_color(12, set_color_intensity(COLOR_FIRE_BR_RED, intensity))
    lightshow.set_state_color(13, set_color_intensity(COLOR_DARK_PINK,   intensity))
    lightshow.set_state_color(14, set_color_intensity(COLOR_WHITE,       intensity))
    lightshow.set_state_color(15, set_color_intensity(COLOR_BLACK,       intensity))
    lightshow.set_state_count(16)


    lightshow.enable_auto(True)
    lightshow.enable_rgb(True)



    #lightshow_data = 0x01234567
    #print ("")
    #print ("Clear Control Register...")
    #lightshow.set_control(0x00)
    #print ("Read back control data")
    #print ("Control Data: 0x%08X" % lightshow.get_control())
    #print ("")
    #print ("Write 0x%08X to the control register" % lightshow_data)
    #lightshow.set_control(lightshow_data)
    #print ("Read back control data")
    #print ("Control Data: 0x%08X" % lightshow.get_control())

if __name__ == "__main__":
    main(sys.argv)


