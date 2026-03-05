#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 fucking-us.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
from scipy.signal import find_peaks
from collections import deque

class postprocessor(gr.sync_block):
    """
    docstring for block postprocessor
    """

    def __init__(self, t,fs,sensitivity,timeout):
        self.t = t
        self.fs = fs
        self.sensitivity = sensitivity
        self.timeout = timeout
        self.bits = []
        self.queue = deque([])
        self.did_removed_preamble = False
        gr.sync_block.__init__(self,
            name="postprocessor",
            in_sig=[np.float32, ],
            out_sig=None)


    def ravid_work(self, input_items, output_items):
        in0 = input_items[0]
        print(f"input samples:{input_items[0]}")
        # <+signal processing here+>
        sps = int(self.t*self.fs)

        window = np.concatenate(np.full(sps, 1), np.full(sps, -1))
        diff = np.convolve(in0, window, mode='full')


        threshold = 0.15 * 2 * sps * 0.5

        # threshold = diff[sps]
        bits = []
        for peak in diff[3*sps:len(diff):3*sps]:
            bit = 1
            if peak>threshold:
                bit = 0
            bits.append(bit)

        #print(bits[0:min(100, len(bits)-1)])
        output_str = self.bits_to_string(bits)
        
        print(output_str)
            
        return len(input_items[0])
    

    def old_work(self, input_items, output_items):
        in0 = input_items[0]
        window = np.concatenate((np.full((int(self.t*self.fs)), 1), np.full((int(self.t*self.fs)), -1)))
        diff = np.correlate(in0, window, mode='full')

        peak_indices, _ = find_peaks(diff)
        print(peak_indices[0:min(100, len(peak_indices)-1)])

        peak_indices = np.concatenate(([0], peak_indices))
        
        
        for peak_idx in peak_indices:
            
            if peak_idx < len(diff):
                bit = 1
                if input_items[0][int(peak_idx + 0.5*int(self.t*self.fs))] < 0:
                    bit = 0
                self.bits.append(bit)
            
            if (len(self.bits) == 8):
                output_str = self.bits_to_string(self.bits)
                print(f"char is {output_str}")
                self.bits = []
            
        return len(input_items[0])


    def BABOON_work(self, input_items, output_items):
        in0 = input_items[0]
        sps = int(self.t*self.fs)
        
        for x in input_items[0]:
            if (x>0):
                x=1
            else:
                x=-1

        print(f"size:{len(in0)},first_sample:{in0[0:30]}")
        diff = np.diff(in0)

        # peak_indices, _ = find_peaks(diff)
        # print(peak_indices[0:min(100, len(peak_indices)-1)])

        # peak_indices = np.concatenate(([0], peak_indices))
        
        
        for index,dif in enumerate(diff):
            if(dif == -2):
                # print(f"index is{index}")
                bit = 1
                # for i in range(3,(int(1.3*sps))):
                #     if((index + i)<len(in0) and in0[index + i] != -1):
                #         bit = 1
                #         break
                if(in0[index -(sps+1)] == -1):
                    bit = 0

                
                self.bits.append(bit)
            
            if (len(self.bits) == 8):
                output_str = self.bits_to_string(self.bits)
                print(f"char is {output_str}")
                self.bits = []
            
        return len(input_items[0])
    
    def BASIC_TASK3_BUT_IT_work(self, input_items, output_items):
        in0 = input_items[0]
        sps = int(self.t*self.fs)
        self.queue.extend(in0)
        if (self.did_removed_preamble == False):
            # for i in range(sps): 
            while(True):
                if(self.queue[0] == -1):
                    self.queue.popleft()
                else:
                    break
            self.did_removed_preamble = True

        while(len(self.queue) > (3 * sps)):
            dequeued_items = np.array([self.queue.popleft() for _ in range(3 * sps)])
            bit = postprocessor.decide_bit(dequeued_items,sps)
            self.bits.append(bit)

            if (len(self.bits) == 8):
                output_str = self.bits_to_string(self.bits)
                print(f"{output_str}")
                self.bits = []
        
        # for x in input_items[0]:
        #     if (x>0):
        #         x=1
        #     else:
        #         x=-1

            
        return len(input_items[0])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        sps = int(self.t*self.fs)
        self.queue.extend(in0)
        if (self.did_removed_preamble == False):
            for i in range(sps):
                self.queue.popleft()
            # while(True):
            #     if(self.queue[0] <0):
            #         self.queue.popleft()
            #     else:
            #         break
            self.did_removed_preamble = True

        while(len(self.queue) > (3 * sps)):

            dequeued_items = np.array([self.queue.popleft() for _ in range(3 * sps)])
            bit = postprocessor.decide_bit(dequeued_items,sps)
            self.bits.append(bit)

            if (len(self.bits) == 8):
                output_str = self.bits_to_string(self.bits)
                print(f"{output_str}")
                self.bits = []
    

            
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

    @staticmethod
    def BASIC_TASK3_BUT_IT_work_decide_bit(samples_array,sps):
        if (samples_array[int(1.5*sps)] == 1):
            return 1
        else:
            return 0
        
    @staticmethod
    def decide_bit(samples_array,sps): 
        binary_arr = (samples_array>0).astype(int)
        # print(f"sum {sum(binary_arr)}")
        if(sum(binary_arr)>(1.5*sps)):
            return 1
        else:
            return 0


        # sliced = samples_array[0:2*sps]
        
        # window = np.concatenate((np.full((sps), 1), np.full((sps), -1)))
        # res = sum(np.multiply(sliced,window)) 
        # print(f"res is {res}")
        # if res<10:
        #     return 1
        # return 0

