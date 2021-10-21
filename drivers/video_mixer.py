from pynq import PL
from .emmio import EMMIO
#from pynq.drivers.framebuffer import FrameBuffer

REG_CONTROL             =   0x000
REG_GLOBAL_INTERRUPT_EN =   0x004
REG_INTERRUPT_ENABLE    =   0x008
REG_INTERRUPT_STATUS    =   0x00C
REG_WIDTH               =   0x010
REG_HEIGHT              =   0x018
REG_BACKGROUND_Y_R      =   0x028
REG_BACKGROUND_U_G      =   0x030
REG_BACKGROUND_V_B      =   0x038
REG_LAYER_ENABLE        =   0x040


BIT_CR_START            =   0
BIT_CR_DONE             =   1
BIT_CR_IDLE             =   2
BIT_CR_READY            =   3
BIT_CR_FLUSH            =   4
BIT_CR_FLUSH_DONE       =   5
BIT_CR_AUTO_RESTART     =   7

BIT_GIE_EN              =   0

BIT_IPE_DONE            =   0
BIT_IPE_READY           =   1

BIT_IPS_DONE            =   0
BIT_IPS_READY           =   1

BIT_LAYER_MASTER_EN     =   0
BIT_LAYER_OVERLAY       =   16
BIT_LAYER_LOGO          =   23

LAYER_OFFSET_BASE       =   0x100

LAYER_OFFSET_ALPHA      =   0x000
LAYER_OFFSET_X          =   0x008
LAYER_OFFSET_Y          =   0x010
LAYER_OFFSET_WIDTH      =   0x018
LAYER_OFFSET_STRIDE     =   0x020
LAYER_OFFSET_HEIGHT     =   0x028
LAYER_OFFSET_SCALE      =   0x030
LAYER_OFFSET_PLANE1     =   0x040
LAYER_OFFSET_PLANE2     =   0x04C

LAYER_SIZE              =   0x100

class VideoMixer(object):

    def __init__(self, name, debug = False, width=1280, height=720):
        if name not in PL.ip_dict:
            print ("No such %s" % name)
        base_addr   = PL.ip_dict[name]["phys_addr"]
        addr_length = PL.ip_dict[name]["addr_range"]
        self.debug = debug
        self.mmio = EMMIO(base_addr, addr_length, debug)
        self.width = width
        self.height = height

    def start(self, auto_start=True):
        control = 1 << BIT_CR_AUTO_RESTART | 1 << BIT_CR_START
        #print ("Control: 0x%08X\n" % control)
        self.mmio.write(REG_CONTROL, control)

    def stop(self):
        control = 0x00

    def get_control(self):
        return self.mmio.read(REG_CONTROL)

    def get_layer_enable_reg(self):
        return self.mmio.read(REG_LAYER_ENABLE)

    def enable_master_layer(self, enable):
        self.mmio.enable_register_bit(REG_LAYER_ENABLE, BIT_LAYER_MASTER_EN, enable)

    def enable_layer(self, layer, enable):
        self.mmio.enable_register_bit(REG_LAYER_ENABLE, layer + 1, enable)

    def enable_overlay_layer(self, enable):
        self.mmio.enable_register_bit(REG_LAYER_ENABLE, BIT_LAYER_OVERLAY, enable)

    def enable_logo_layer(self, enable):
        self.mmio.enable_register_bit(REG_LAYER_ENABLE, BIT_LAYER_LOGO, enable)

    def configure_master_layer(self, width, height):
        self.mmio.write(REG_WIDTH, width)
        self.mmio.write(REG_HEIGHT, height)

    def configure_layer(self, index, x, y, width, height, stride = None, alpha = 255, scale = 0, plane1 = 0, plane2 = 0):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        if stride is None:
            stride = width
        self.mmio.write(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_ALPHA, alpha)
        self.mmio.write(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_X, x)
        self.mmio.write(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_Y, y)
        self.mmio.write(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_WIDTH, width)
        self.mmio.write(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_STRIDE, stride)
        self.mmio.write(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_HEIGHT, height)
        self.mmio.write(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_SCALE, scale)
        self.mmio.write(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_PLANE1, plane1)
        self.mmio.write(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_PLANE2, plane2)

    def get_layer_x(self, index):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        return self.mmio.read(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_X)

    def get_layer_y(self, index):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        return self.mmio.read(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_Y)

    def get_layer_width(self, index):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        return self.mmio.read(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_WIDTH)

    def get_layer_stride(self, index):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        return self.mmio.read(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_STRIDE)

    def get_layer_height(self, index):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        return self.mmio.read(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_HEIGHT)

    def get_layer_scale(self, index):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        return self.mmio.read(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_SCALE)

    def get_layer_alpha(self, index):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        return self.mmio.read(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_ALPHA)

    def get_layer_plane1_addr(self, index):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        return self.mmio.read(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_PLANE1)

    def get_layer_plane2_addr(self, index):
        addr_base = LAYER_OFFSET_BASE + index * LAYER_SIZE
        return self.mmio.read(addr_base + LAYER_OFFSET_BASE + LAYER_OFFSET_PLANE2)


