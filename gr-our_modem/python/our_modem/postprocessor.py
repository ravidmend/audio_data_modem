#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 fucking-us.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class postprocessor(gr.sync_block):
    """
    docstring for block postprocessor
    """
    def __init__(self, t,fs,sensitivity,timeout):
        self.t = t
        self.fs = fs
        self.sensitivity = sensitivity
        self.timeout = timeout
        gr.sync_block.__init__(self,
            name="postprocessor",
            in_sig=[np.float32, ],
            out_sig=None)


    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>
        diff = np.diff(input_items[0])



        return len(input_items[0])
    
    @staticmethod
    def bits_to_string(bits_array):
        output_str = ""
        bytes = [bits_array[i:i+8] for i in range(0,len(bits_array),8)] #break into bytes arrays
        
        for byte in bytes:
            byte_string = "".join(map(str,byte)) # turn array to string
            ch = int(byte_string,2)
            output_str += chr(ch)
        return output_str