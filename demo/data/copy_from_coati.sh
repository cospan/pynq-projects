#! /bin/bash

scp cospan@192.168.86.44:Projects/xilinx_projects/pynq_z2_barebones/pynq_z2_demo.runs/impl_1/system_wrapper.bit ./system_wrapper.bit
scp cospan@192.168.86.44:Projects/xilinx_projects/pynq_z2_barebones/pynq_z2_demo.srcs/sources_1/bd/system/hw_handoff/system.hwh ./system_wrapper.hwh

