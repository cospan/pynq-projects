from pynq import PL
from .emmio import EMMIO


REG_CONTROL             = 0x000
REG_STATUS              = 0x004
REG_ERROR               = 0x008
REG_IRQ_ENABLE          = 0x00C
REG_VERSION             = 0x010
REG_ADAPTIVE_SYNC_CTRL  = 0x014
REG_STRETCH_LIMIT       = 0x018
REG_DET_ACTIVE_SIZE     = 0x020
REG_DET_TIMING_STATUS   = 0x024
REG_DET_ENCODING        = 0x028
REG_DET_HSIZE           = 0x030
REG_DET_VSIZE           = 0x034
REG_DET_HSYNC           = 0x038
REG_DET_F0_VBLANK_H     = 0x03C
REG_DET_F0_VSYNC_V      = 0x040
REG_DET_F0_VSYNC_H      = 0x044
REG_DET_F1_VBLANK_H     = 0x048
REG_DET_F1_VSYNC_V      = 0x04C
REG_DET_F1_VSYNC_H      = 0x050
REG_GEN_ACTIVE_SIZE     = 0x060
REG_GEN_TIMING_STATUS   = 0x064
REG_GEN_ENCODING        = 0x068
GEN_POLARITY            = 0x06C
GEN_HSIZE               = 0x070
GEN_VSIZE               = 0x074
GEN_HSYNC               = 0x078
GEN_F0_VBLANK_H         = 0x07C
GEN_F0_VSYNC_V          = 0x080
GEN_F0_VSYNC_H          = 0x084
GEN_F1_VBLANK_H         = 0x088
GEN_F1_VSYNC_V          = 0x08C
GEN_F1_VSYNC_H          = 0x090
GEN_ACTIVE_SIZE         = 0x094
FRAME_SYNC_CONFIG_START = 0x100

BIT_CR_SW_RESET               = 31
BIT_CR_FSYNC_RESET            = 30
BIT_CR_FIELD_ID_POL_SRC       = 26
BIT_CR_ACTIVE_CHROMA_POL_SRC  = 25
BIT_CR_ACTIVE_VIDEO_POL_SRC   = 24
BIT_CR_HSYNC_POL_SRC          = 23
BIT_CR_VSYNC_POL_SRC          = 22
BIT_CR_HBLANK_POL_SRC         = 21
BIT_CR_VBLANK_POL_SRC         = 20
BIT_CR_CHROMA_SRC             = 18
BIT_CR_VBLANK_HOFF_SRC        = 17
BIT_CR_VSYNC_END_SRC          = 16
BIT_CR_VSYNC_START_SRC        = 15
BIT_CR_ACTIVE_VSYNC_SRC       = 14
BIT_CR_FRAME_VSIZE_SRC        = 13
BIT_CR_HSYNC_END_SRC          = 11
BIT_CR_HSYNC_START_SRC        = 10
BIT_CR_ACTIVE_HSIZE_SRC       = 9
BIT_CR_FRAME_HSIZE_SRC        = 8
BIT_CR_SYNC_ENABLE            = 5
BIT_CR_DET_ENABLE             = 3
BIT_CR_GEN_ENABLE             = 2
BIT_CR_REG_UPDATE             = 1
BIT_CR_SW_ENABLE              = 0


BIT_RANGE_SR_FSYNC            = 0xFFFF0000
BIT_SR_GEN_ACTIVE_VIDEO       = 13
BIT_SR_GEN_VBLANK             = 12
BIT_SR_DET_ACTIVE_VIDEO       = 11
BIT_SR_DET_VBLANK             = 10
BIT_SR_LOCK_LOSS              = 9
BIT_SR_LOCK                   = 8

BIT_ERR_ACTIVE_CHROMA_LOCK    = 21
BIT_ERR_ACTIVE_VIDEO_LOCK     = 20
BIT_ERR_HSYNC_LOCK            = 19
BIT_ERR_VSYNC_LOCK            = 18
BIT_ERR_HBLANK_LOCK           = 17
BIT_ERR_VBLANK_LOCK           = 16

BIT_RANGE_IRQ_FSYNC           = 0xFFFF0000
BIT_IRQ_GEN_ACTIVE_VIDEO      = 13
BIT_IRQ_GEN_VBLANK            = 12
BIT_IRQ_DET_ACTIVE_VIDEO      = 11
BIT_IRQ_DET_VBLANK            = 10
BIT_IRQ_LOCK_LOSS             = 9
BIT_IRQ_LOCK                  = 8


BIT_RANGE_GEN_ACTIVE_SIZE_WIDTH   = 0x00000FFF
BIT_RANGE_GEN_ACTIVE_SIZE_HEIGHT  = 0x0FFF0000
#uuuhhhggg I'll do the rest later!





class TimingController(object):
    def __init__(self, name, debug = False):
        if name not in PL.ip_dict:
            print ("No such %s" % name)

        base_addr   = PL.ip_dict[name]["phys_addr"]
        addr_length = PL.ip_dict[name]["addr_range"]
        self.debug = debug
        self.mmio = EMMIO(base_addr, addr_length, debug)

    def reset(self, fsync=False):
        if fsync:
            self.mmio.set_register_bit(REG_CONTROL, BIT_CR_FSYNC_RESET)
        else:
            self.mmio.set_register_bit(REG_CONTROL, BIT_CR_SW_RESET)

    def is_reset_done(self, fsync=False):
        if fsync:
            return not self.mmio.is_register_bit_set(REG_CONTROL, BIT_CR_FSYNC_RESET)
        else:
            return not self.mmio.is_register_bit_set(REG_CONTROL, BIT_CR_SW_RESET)

    def get_generator_width(self):
        return self.mmio.read_register_bitmask(REG_GEN_ACTIVE_SIZE, BIT_RANGE_GEN_ACTIVE_SIZE_WIDTH)

    def get_generator_height(self):
        return self.mmio.read_register_bitmask(REG_GEN_ACTIVE_SIZE, BIT_RANGE_GEN_ACTIVE_SIZE_HEIGHT)

    def get_control_reg(self):
        return self.mmio.read(REG_CONTROL)

    def enable(self,
                det_enable  = False,
                gen_enable  = False,
                reg_update  = False,
                sw_enable   = False,
                sync_enable = False,
                use_gen_src = False):
        data = 0
        data |= (use_gen_src << BIT_CR_FIELD_ID_POL_SRC)
        data |= (use_gen_src << BIT_CR_ACTIVE_CHROMA_POL_SRC)
        data |= (use_gen_src << BIT_CR_ACTIVE_VIDEO_POL_SRC)
        data |= (use_gen_src << BIT_CR_HSYNC_POL_SRC)
        data |= (use_gen_src << BIT_CR_VSYNC_POL_SRC)
        data |= (use_gen_src << BIT_CR_HBLANK_POL_SRC)
        data |= (use_gen_src << BIT_CR_VBLANK_POL_SRC)
        data |= (use_gen_src << BIT_CR_CHROMA_SRC)
        data |= (use_gen_src << BIT_CR_VBLANK_HOFF_SRC)
        data |= (use_gen_src << BIT_CR_VSYNC_END_SRC)
        data |= (use_gen_src << BIT_CR_VSYNC_START_SRC)
        data |= (use_gen_src << BIT_CR_ACTIVE_VSYNC_SRC)
        data |= (use_gen_src << BIT_CR_FRAME_VSIZE_SRC)
        data |= (use_gen_src << BIT_CR_HSYNC_END_SRC)
        data |= (use_gen_src << BIT_CR_HSYNC_START_SRC)
        data |= (use_gen_src << BIT_CR_ACTIVE_HSIZE_SRC)
        data |= (use_gen_src << BIT_CR_FRAME_HSIZE_SRC)
        data |= (sync_enable << BIT_CR_SYNC_ENABLE)
        data |= (det_enable  << BIT_CR_DET_ENABLE)
        data |= (gen_enable  << BIT_CR_GEN_ENABLE)
        data |= (reg_update  << BIT_CR_REG_UPDATE)
        data |= (sw_enable   << BIT_CR_SW_ENABLE)
        self.mmio.write(REG_CONTROL, data)




