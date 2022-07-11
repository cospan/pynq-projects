#! /bin/bash

scp cospan@192.168.86.44:Projects/xilinx/pynq_2022_05_26_vdma_rot/pynq_2022_05_26_vdma_rot.runs/impl_1/system_wrapper.bit ./system_wrapper.bit
scp cospan@192.168.86.44:Projects/xilinx/pynq_2022_05_26_vdma_rot/pynq_2022_05_26_vdma_rot.gen/sources_1/bd/system/hw_handoff/system.hwh ./system_wrapper.hwh

