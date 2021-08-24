from pynq import PL
from .emmio import EMMIO
import time


REG_CONTROL             =   0x000
REG_STATUS              =   0x004
REG_CLK_L               =   0x008
REG_FB_L                =   0x00C
REG_FB_H_CLK_H          =   0x010
REG_DIV                 =   0x014
REG_LOCK_L              =   0x018
REG_FLTR_LOCK_H         =   0x01C
REG_REF_CLK_FREQ        =   0x020

BIT_CR_START            =   0

BIT_SR_RUNNING          =   0

BIT_WEDGE               =   13
BIT_NOCOUNT             =   12

ERR_CLKDIVIDER          = (1 << BIT_WEDGE) | (1 << BIT_NOCOUNT)
ERR_CLKCOUNTCALC        = 0xFFFFFFFF

class clk_config:
    lock_l = 0
    fb_l =0
    fb_h_lock_h = 0
    div_clk = 0
    lock_l = 0
    fltr_lock_h = 0

class clk_mode:
    freq = 0.00
    fb_mult = 0
    clk_div = 0
    main_div = 0


lock_lookup = [
   0b0011000110111110100011111010010000000001,
   0b0011000110111110100011111010010000000001,
   0b0100001000111110100011111010010000000001,
   0b0101101011111110100011111010010000000001,
   0b0111001110111110100011111010010000000001,
   0b1000110001111110100011111010010000000001,
   0b1001110011111110100011111010010000000001,
   0b1011010110111110100011111010010000000001,
   0b1100111001111110100011111010010000000001,
   0b1110011100111110100011111010010000000001,
   0b1111111111111000010011111010010000000001,
   0b1111111111110011100111111010010000000001,
   0b1111111111101110111011111010010000000001,
   0b1111111111101011110011111010010000000001,
   0b1111111111101000101011111010010000000001,
   0b1111111111100111000111111010010000000001,
   0b1111111111100011111111111010010000000001,
   0b1111111111100010011011111010010000000001,
   0b1111111111100000110111111010010000000001,
   0b1111111111011111010011111010010000000001,
   0b1111111111011101101111111010010000000001,
   0b1111111111011100001011111010010000000001,
   0b1111111111011010100111111010010000000001,
   0b1111111111011001000011111010010000000001,
   0b1111111111011001000011111010010000000001,
   0b1111111111010111011111111010010000000001,
   0b1111111111010101111011111010010000000001,
   0b1111111111010101111011111010010000000001,
   0b1111111111010100010111111010010000000001,
   0b1111111111010100010111111010010000000001,
   0b1111111111010010110011111010010000000001,
   0b1111111111010010110011111010010000000001,
   0b1111111111010010110011111010010000000001,
   0b1111111111010001001111111010010000000001,
   0b1111111111010001001111111010010000000001,
   0b1111111111010001001111111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001,
   0b1111111111001111101011111010010000000001
]


filter_lookup_low = [
	 0b0001011111,
	 0b0001010111,
	 0b0001111011,
	 0b0001011011,
	 0b0001101011,
	 0b0001110011,
	 0b0001110011,
	 0b0001110011,
	 0b0001110011,
	 0b0001001011,
	 0b0001001011,
	 0b0001001011,
	 0b0010110011,
	 0b0001010011,
	 0b0001010011,
	 0b0001010011,
	 0b0001010011,
	 0b0001010011,
	 0b0001010011,
	 0b0001010011,
	 0b0001010011,
	 0b0001010011,
	 0b0001010011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0001100011,
	 0b0010010011,
	 0b0010010011,
	 0b0010010011,
	 0b0010010011,
	 0b0010010011,
	 0b0010010011,
	 0b0010010011,
	 0b0010010011,
	 0b0010010011,
	 0b0010010011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011,
	 0b0010100011
]




class MODE_640x480:
    label = "640x480@60Hz"
    width = 640
    height = 480
    mode = 10
    freq = 25.0


class MODE_800x600:
    label = "800x600@60Hz"
    width = 800
    height = 600
    mode = 11
    freq = 40.0


class MODE_1280x1024:
    label = "1280x1024@60Hz"
    width = 1280
    height = 1024
    mode = 13
    freq = 108.0


class MODE_1280x720:
    label = "1280x720@60Hz"
    width = 1280
    height = 720
    mode = 1
    freq = 74.25 #74.2424 is close enough


class MODE_1920x1080:
    label = "1920x1080@60Hz"
    width = 1920
    height = 1080
    mode = 2
    #.freq = 148.5 #148.57 is close enough
    freq = 150


# Functions

class DynamicClock(object):
    def __init__(self, name, debug = False):
        if name not in PL.ip_dict:
            print ("No such %s" % name)

        base_addr   = PL.ip_dict[name]["phys_addr"]
        addr_length = PL.ip_dict[name]["addr_range"]
        self.debug = debug
        self.mmio = EMMIO(base_addr, addr_length, debug)

    def divider(self, divide):
        output = 0
        high_time = 0
        low_time = 0

        if (divide < 1) or (divide > 128):
            return ERR_CLKDIVIDER

        if divide == 1:
            return 0x1041

        high_time = divide / 2
        if (divide & 0b1) > 0: # if divide is odd
            low_time = high_time + 1
            output = 1 << BIT_WEDGE
        else:
            low_time = high_time

        output |= int(0x03F) & int(low_time)
        output |= int(0xFC0) & int(int(high_time) << 6)
        return output

    def count_calc(self, divide):
        output = 0
        div_calc = self.divider(divide)
        if div_calc == ERR_CLKDIVIDER:
            output = ERR_CLKCOUNTCALC;
        else:
            output = (0xFFF & div_calc) | ((div_calc << 10) & 0x00C00000);
        return output

    def get_register_values (self, clk_params):
        reg_values = {}
        reg_values["lock_l"]      = 0
        reg_values["fb_l"]        = 0
        reg_values["fb_h_lock_h"] = 0
        reg_values["div_clk"]     = 0
        reg_values["lock_l"]      = 0
        reg_values["fltr_lock_h"] = 0


        if ((clk_params["fb_mult"] < 2) or clk_params["fb_mult"] > 64 ):
            return None;

        reg_values["lock_l"] = self.count_calc(clk_params["clk_div"]);
        if (reg_values["lock_l"] == ERR_CLKCOUNTCALC):
            return None;

        reg_values["fb_l"] = self.count_calc(clk_params["fb_mult"]);
        if (reg_values["fb_l"] == ERR_CLKCOUNTCALC):
            return None;

        reg_values["fb_h_lock_h"] = 0;

        reg_values["div_clk"] = self.divider(clk_params["main_div"]);
        if (reg_values["div_clk"] == ERR_CLKDIVIDER):
            return None;

        reg_values["lock_l"] = (lock_lookup[clk_params["fb_mult"] - 1] & 0xFFFFFFFF);

        reg_values["fltr_lock_h"]  = ((lock_lookup[clk_params["fb_mult"] - 1] >> 32) & 0x000000FF);
        reg_values["fltr_lock_h"] |= ((filter_lookup_low[clk_params["fb_mult"] - 1] << 16) & 0x03FF0000);

        return reg_values;

    def write_config(self, reg_values):
        self.mmio.write(REG_CLK_L,       reg_values["lock_l"]     )
        self.mmio.write(REG_FB_L,        reg_values["fb_l"]       )
        self.mmio.write(REG_FB_H_CLK_H,  reg_values["fb_h_lock_h"])
        self.mmio.write(REG_DIV,         reg_values["div_clk"]    )
        self.mmio.write(REG_LOCK_L,      reg_values["lock_l"]     )
        self.mmio.write(REG_FLTR_LOCK_H, reg_values["fltr_lock_h"])

    def find_params(self, frequency):
        REF_CLK_FREQ = 100.0
        best_error = 2000.0

        cur_fb = 0
        cur_clk_div = 0

	# This is necessary because the MMCM actual is generating 5x the desired pixel clock, and that
	# clock is then run through a BUFR that divides it by 5 to generate the pixel clock. Note this
	# means the pixel clock is on the Regional clock network, not the global clock network. In the
	# future if options like these are parameterized in the axi_dynclk core, then this function will
	# need to change.

        freq = frequency * 5.0
        best_pick = {}
        best_pick["clk_div"]    = 0
        best_pick["fb_mult"]    = 0
        best_pick["main_div"]   = 0
        best_pick["freq"]       = 0.0

        # TODO: Replace with smarter algorithm that doens't check all possible combinations
        for cur_div in range (1, 11):
            min_fb = cur_div * 6
            max_fb = cur_div * 12
            if max_fb > 64:
                max_fb = 64

            cur_clk_mult = (REF_CLK_FREQ / cur_div) / freq

            cur_fb = min_fb
            while cur_fb <= max_fb:
                cur_clk_div = int((cur_clk_mult * cur_fb) + 0.5)
                cur_freq = (REF_CLK_FREQ / cur_div) / cur_clk_div * cur_fb
                cur_error = abs(cur_freq - freq)
                if cur_error < best_error:
                    if (self.debug): print ("freq x 5: %f, cur_div: %d, cur_fb: %d, cur_clk_mult: %f" % (freq, cur_div, cur_fb, cur_clk_mult))
                    best_error = cur_error
                    best_pick["clk_div"] = int(cur_clk_div)
                    best_pick["fb_mult"] = int(cur_fb)
                    best_pick["main_div"] = int(cur_div)
                    best_pick["freq"] = cur_freq
                cur_fb = cur_fb + 1

        best_pick["freq"] = best_pick["freq"] / 5.0
        best_error = best_error / 5.0
        return (best_error, best_pick)

    def set_frequency(self, frequency):
        error, clk_params = self.find_params(frequency)
        print ("Requested Frequency:    %f" % frequency)
        print ("Found Frequency:        %f" % clk_params["freq"])
        print ("Error:                  %f" % error)

        reg_values = self.get_register_values(clk_params)

        if self.debug:
             print ("Parameters:")
             print ("clk_div:                %d" % clk_params["clk_div"])
             print ("fb_mult:                %d" % clk_params["fb_mult"])
             print ("main_div:               %d" % clk_params["main_div"])
             print ("Register Values:")
             if reg_values is None:
                 print ("register values were invalid!")
             else:
                 for key in reg_values:
                     print ("%s: 0x%08X, %d"  % (key, reg_values[key], reg_values[key]))
                 print ("")

        print ("Status Register: 0x%08X" % self.mmio.read(REG_STATUS))
        self.write_config(reg_values)
        self.start()
        print ("Status Register: 0x%08X" % self.mmio.read(REG_STATUS))

        

    def start(self):
        self.mmio.set_register_bit(REG_CONTROL, BIT_CR_START)
        while not self.mmio.is_register_bit_set(REG_STATUS, BIT_SR_RUNNING):
            print ("Not Locked!")
            time.sleep(0.01)

    def stop(self):
        self.mmio.clear_register_bit(REG_CONTROL, BIT_CR_START)
        while self.mmio.is_register_bit_set(REG_STATUS, BIT_SR_RUNNING):
            time.sleep(0.01)
        
    def is_running(self):
        return self.mmio.is_register_bit_set(REG_STATUS, BIT_SR_RUNNING)
