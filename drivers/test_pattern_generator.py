from pynq import PL
from .emmio import EMMIO

# Register Space
REG_CONTROL             = 0x00
REG_GIE                 = 0x04
REG_IE                  = 0x08
REG_IS                  = 0x0C
REG_ACTIVE_HEIGHT       = 0x10
REG_ACTIVE_WIDTH        = 0x18
REG_BG_PATTERN_ID       = 0x20
REG_FG_PATTERN_ID       = 0x28
REG_MASK_ID             = 0x30
REG_MOTION_SPEED        = 0x38
REG_COLOR_FORMAT        = 0x40
REG_CROSS_HAIR_HOR      = 0x48
REG_CROSS_HAIR_VER      = 0x50
REG_ZP_HOR_CTRL_START   = 0x58
REG_SP_HOR_CTRL_DELTA   = 0x60
REG_ZP_VER_CTRL_START   = 0x68
REG_ZP_VER_CTRL_DELTA   = 0x70
REG_BOX_SIZE            = 0x78
REG_BOX_COLOR_RED_Y     = 0x80
REG_BOX_COLOR_GREEN_U   = 0x88
REG_BOX_COLOR_BLUE_V    = 0x90
REG_ENABLE_INPUT        = 0x98
REG_PASS_THRU_START_X   = 0xA0
REG_PASS_THRU_START_Y   = 0xA8
REG_PASS_THRU_END_X     = 0xB0
REG_PASS_THRU_END_Y     = 0xB8
REG_DP_DYN_RANGE        = 0xC0
REG_DP_YUV_COEF         = 0xC8

BIT_CR_START            = 0
BIT_CR_CONTINUOUS       = 7

ID_BG_PAT_PASS_THRU     = 0x00
ID_BG_PAT_HRAMP         = 0x01
ID_BG_PAT_VRAMP         = 0x02
ID_BG_PAT_TRAMP         = 0x03
ID_BG_PAT_SOLID_RED     = 0x04
ID_BG_PAT_SOLID_GREEN   = 0x05
ID_BG_PAT_SOLID_BLUE    = 0x06
ID_BG_PAT_SOLID_BLACK   = 0x07
ID_BG_PAT_SOLID_WHITE   = 0x08
ID_BG_PAT_COLOR_BARS    = 0x09
ID_BG_PAT_ZONE          = 0x0A
ID_BG_PAT_TCOLOR_BARS   = 0x0B
ID_BG_PAT_CROSS_HATCH   = 0x0C
ID_BG_PAT_COLOR_SWEEP   = 0x0D
ID_BG_PAT_VH_RAMP       = 0x0E
ID_BG_PAT_BW_CV         = 0x0F
ID_BG_PAT_PSRANDOM      = 0x10
ID_BG_PAT_DP_CRAMP      = 0x11
ID_BG_PAT_DP_BW_VLINES  = 0x12
ID_BG_PAT_DP_C_SQUARE   = 0x13

ID_FG_PAT_NONE          = 0x00
ID_FG_PAT_MOVE_BOX      = 0x01
ID_FG_PAT_CROSS_HAIR    = 0x02

BIT_MASK_RED            = 0x01
BIT_MASK_GREEN          = 0x02
BIT_MASK_BLUE           = 0x04

ID_COLOR_FORMAT_RGB     = 0x00
ID_COLOR_FORMAT_YUV444  = 0x01
ID_COLOR_FORMAT_YUV422  = 0x02
ID_COLOR_FORMAT_YUV420  = 0x03

ID_DP_RANGE_VESA        = 0x00
ID_DP_RANGE_CEA         = 0x01

ID_DP_YUV_COEF_601      = 0x00
ID_DP_YUV_COEF_709      = 0x01

class TestPatternID(object):
    PASS_THRU     = 0x00
    HRAMP         = 0x01
    VRAMP         = 0x02
    TRAMP         = 0x03
    SOLID_RED     = 0x04
    SOLID_GREEN   = 0x05
    SOLID_BLUE    = 0x06
    SOLID_BLACK   = 0x07
    SOLID_WHITE   = 0x08
    COLOR_BARS    = 0x09
    ZONE          = 0x0A
    TCOLOR_BARS   = 0x0B
    CROSS_HATCH   = 0x0C
    COLOR_SWEEP   = 0x0D
    VH_RAMP       = 0x0E
    BW_CV         = 0x0F
    PSRANDOM      = 0x10
    DP_CRAMP      = 0x11
    DP_BW_VLINES  = 0x12
    DP_C_SQUARE   = 0x13





class TestPatternGenerator(object):

    def __init__(self, name, debug = False):
        if name not in PL.ip_dict:
            print ("No such %s" % name)

        base_addr   = PL.ip_dict[name]["phys_addr"]
        addr_length = PL.ip_dict[name]["addr_range"]
        self.debug = debug
        self.mmio = EMMIO(base_addr, addr_length, debug)

    def start(self, continuous=True):
        data = 1 << BIT_CR_START
        if continuous:
            data |= 1 << BIT_CR_CONTINUOUS
        self.mmio.write(REG_CONTROL, data)

    def set_color_bar_test_pattern(self):
        self.mmio.write(REG_BG_PATTERN_ID, ID_BG_PAT_COLOR_BARS);

    def set_test_pattern(self, pattern_id):
        self.mmio.write(REG_BG_PATTERN_ID, pattern_id);

    def set_image_size(self, width, height):
        self.mmio.write(REG_ACTIVE_WIDTH, width)
        self.mmio.write(REG_ACTIVE_HEIGHT, height)

    def set_color_format_to_rgb(self):
        self.mmio.write(REG_COLOR_FORMAT, ID_COLOR_FORMAT_RGB)

    def set_color_format_to_yuv444(self):
        self.mmio.write(REG_COLOR_FORMAT, ID_COLOR_FORMAT_YUV444)

    def set_color_format_to_yuv422(self):
        self.mmio.write(REG_COLOR_FORMAT, ID_COLOR_FORMAT_YUV422)

    def set_color_format_to_yuv420(self):
        self.mmio.write(REG_COLOR_FORMAT, ID_COLOR_FORMAT_YUV420)
