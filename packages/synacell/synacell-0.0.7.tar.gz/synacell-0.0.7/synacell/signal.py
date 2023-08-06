"""
Functions used for testing:
    - Printing and ploting test outputs
    - Generating input data
"""
import math
import numpy as np
import wave
import struct
import pandas as pd


def func_generator(func_name="sin", freq=16000.0, amp=1.0, phase=0.0):
    """
    Factory for generating arbitrary functions

    :param func_name: Keyword
    :param freq: Frequency
    :param amp: Amplitude
    :param phase: Phase in radians
    :return: Function with one float argument
    """

    def sin_func(t):
        return amp * math.sin(2 * math.pi * freq * t + phase)

    def const_func(t):
        return amp

    if func_name == "sin":
        return sin_func
    if func_name == "const":
        return const_func


def func_to_nparray(func=math.sin, t_min=0.0, t_max=2.0 * math.pi):
    """
    Returns numpy array of a function with the given range at 16KHz sampling rate

    :param func: Function for tabulating
    :param t_min: Start time
    :param t_max: End time
    :return: Numpy array
    """
    dt = 1.0 / 16000.0
    data_pts = int(t_max/dt)
    return np.asarray([func(i * dt) if t_min <= i*dt < t_max else 0.0 for i in range(data_pts)])


def make_wav(samples, filename):
    """
    Prints data to wav file sampled at 16KHz as uint16

    :param samples: Numpy array
    :param filename: File to print data to
    :return: None
    """
    wav = wave.open(filename, 'w')
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(16000)

    for i in samples:
        value = struct.pack('<h', int(i))
        wav.writeframes(value)

    wav.close()


def load_spice_out(file_name):
    """
    Loads spice output file and returs pandas object

    :param file_name: LTSpice output file name
    :return: Pandas object
    """
    return pd.read_csv(file_name, delimiter='\t', comment='#', dtype=float)
