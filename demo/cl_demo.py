#! /usr/bin/env python3

import sys
import os
import argparse
import time
from pynq import PL
from pynq import Overlay

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from drivers.demo import Demo

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
    print ("Download the image...")
    ol.download()
    print ("Downloaded")
    print ("")

    name = 'demo_0'

    if args.debug: print ("Checking: %s" % name)
    if args.debug: print ("%s: " % dir(PL.ip_dict))
    if args.debug: print ("Keys %s" % PL.ip_dict.keys())
    if name not in PL.ip_dict:
        print ("No such %s" % name)
        exit(0)


    demo = Demo(name, debug = args.debug)
    print ("Vesion: 0x%08X" % demo.get_version())
    demo_data = 0x01234567
    print ("")
    print ("Clear Control Register...")
    demo.set_control(0x00)
    print ("Read back control data")
    print ("Control Data: 0x%08X" % demo.get_control())
    print ("")
    print ("Write 0x%08X to the control register" % demo_data)
    demo.set_control(demo_data)
    print ("Read back control data")
    print ("Control Data: 0x%08X" % demo.get_control())

if __name__ == "__main__":
    main(sys.argv)


