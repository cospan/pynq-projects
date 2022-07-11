import numpy as np


def float2fixed(float_in, signed_flag, total_bits, fractional_bits):
    scale = total_bits - fractional_bits
    r = signed_flag ? (-(scale - 1) : (scale - 1)) : (0 : scale)
    fixed_ar = np.ndarray(
    pass

def fixed2float(fixed_in, fractional_bits):
    pass

