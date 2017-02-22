# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 17:23:16 2017

@author: GLackner
"""

import matplotlib.pyplot as plt
#from matplotlib.ticker import MaxNLocator
from matplotlib import rc
import os

rc('pdf', fonttype=42)
rc('font', **{'sans-serif':['arial']})

def autolabel_peaks(ax, peaks, decimals, x_range, y_range, abs_int = 0, rel_int=0.05):
    
    def filter_and_label(x,y, y_range, text, abs_int = 0, rel_int=0.0):
        if (y >= abs_int) and (y/y_range >= rel_int):
            ax.text(x, 1.01* y, text, ha='center', va='bottom')
    def filter_and_annotate(text, x, y, new_x, new_y, y_range, abs_int = abs_int, rel_int=rel_int):
        if (y >= abs_int) and (y/y_range >= rel_int):
            ax.annotate(text, xy=(x, y), xytext = (new_x, new_y), ha='center', va='bottom', arrowprops=dict(edgecolor='red', shrink=0.05, width=0.01, headwidth=0.1))
       
    def define_pixel_per_unit(): 
        f_y = 350/y_range
        f_x = 450/x_range
        return f_x, f_y
    def unit_to_pixel(x, f_x):
        return x * f_x
        
    def distances_in_pt(peaks, f_x, f_y):
        x_succ = peaks[i+1].get_x()
        y_succ = peaks[i+1].get_height()
        x_prec = peaks[i-1].get_x()
        y_prec = peaks[i-1].get_height()       
        x_succ_pt = x_succ * f_x
        y_succ_pt = y_succ * f_y
        x_prec_pt = x_prec * f_x
        y_prec_pt = y_prec * f_y
        x_dist_right = x_succ_pt - x_pt
        x_dist_left = x_pt - x_prec_pt
        y_dist_right = y_succ_pt - y_pt
        y_dist_left =  y_prec_pt - y_pt
        return x_dist_left, x_dist_right, y_dist_left, y_dist_right
    def format_label_text(x):
        text = format_string %float(x)
        text_width = len(text) * 6.6
        text_height = 9.7
        return text, text_width, text_height
   # attach some text labels
    
    format_string = '%.'+str(decimals)+'f'
    
    f_x, f_y = define_pixel_per_unit()
    
    for i, peak in enumerate(peaks):
        y = peak.get_height()
        x = peak.get_x()
        x_pt = unit_to_pixel(x, f_x)
        y_pt = unit_to_pixel(y, f_y)
        text, text_width, text_height = format_label_text(x)
        if i==0: #first peak
            filter_and_label(x,y, y_range, text, abs_int = abs_int, rel_int=rel_int)
        elif (i == len(peaks)-1):
            filter_and_label(x,y, y_range, text, abs_int = abs_int, rel_int=rel_int)
        elif (i > 0) and (i < len(peaks)-1):
          
            x_dist_left, x_dist_right, y_dist_left, y_dist_right = distances_in_pt(peaks, f_x, f_y)
           
            if ((x_dist_right < text_width*0.5) and (y_dist_right > 0)):
                if ((x_dist_left < text_width*0.5) and (y_dist_left > 0)):
                    new_x = x
                    y_shift = (max([y_dist_left, y_dist_right]) + text_height)/f_y
                    new_y = (y + y_shift)*1.1
                    filter_and_annotate(text, x, y, new_x, new_y, y_range, abs_int = abs_int, rel_int=rel_int)
                else:
                    new_x = x - (text_width*0.5-x_dist_right)/f_x
                    new_y = y
                    filter_and_label(x,y, y_range, text, abs_int = abs_int, rel_int=rel_int)
            elif ((x_dist_left < text_width*0.5) and (y_dist_left > 0)):
          
                new_x = x + (text_width*0.5-x_dist_left)/f_x
                new_y = y
                filter_and_label(x,y, y_range, text, abs_int = abs_int, rel_int=rel_int) 
            else:
                filter_and_label(x,y, y_range, text, abs_int = abs_int, rel_int=rel_int)

def unpack_and_filter_spec(spec, mz_min=None, mz_max=None, abs_int = 0, rel_int=0.0):
    if not mz_min:
        mz_min = spec.mzMin()
    if not mz_max:
        mz_max = spec.mzMax()
    peaks_in_range = spec.peaksInRange(mz_min, mz_max)

    mass_list = peaks_in_range[:,0]
      
    intensity_list = peaks_in_range[:,1]
    max_int = spec.maxIntensity()
    pairs = zip(mass_list, intensity_list)
    filtered_pairs=[]
    for pair in pairs:
        intensity = pair[1]
        if (intensity>=abs_int) & (intensity/max_int > rel_int):
            filtered_pairs.append(pair)
    filtered_mass_list, filtered_intensity_list = zip(*filtered_pairs)
    return filtered_mass_list, filtered_intensity_list
        


def create_box_title(spec):
    if spec.msLevel == 1:
        rt = spec.rt
        box_title = "RT: %.2f m" % rt
    else:
        precursor = spec.precursors[0][0]
        rt = spec.rt
        box_title = "m/z: %.2f \nRT: %.2f m" % (precursor, rt)    
    return box_title
    
def plot_spectrum(mass_spec, file_target, box_title="", mz_min=None, mz_max=None, decimals=2,
                  abs_int = 0, rel_int=0.05, plot_title="", show=True, close=False):
    """ 
    Plots the mass spectrum (emzed spectrum object). If a path (complete path to a file) is 
    provided, a file (default format: png) file will be saved. Other available formast: pdf, svg
    
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    mass_list, intensity_list = unpack_and_filter_spec(mass_spec, mz_min=mz_min, mz_max=mz_max) 
        
    # to set x axis range find minimum and maximum m/z channels
    if not mz_min:
        mz_min = mass_spec.mzMin()
    if not mz_max:
        mz_max = mass_spec.mzMax()
    
    mz_range = mz_max-mz_min
    mz_plot_range_overhang = mz_range*0.05
    max_intensity = mass_spec.maxIntensity()
    
    peaks = plt.bar(mass_list, intensity_list, width=0.01)
        
    plt.xlim(mz_min - mz_plot_range_overhang, mz_max + mz_plot_range_overhang)
    plt.ylim(0, max_intensity*1.1)
    ax.set_title(plot_title)
    

    ax.text(mz_max, max_intensity, box_title, horizontalalignment='right', bbox={'facecolor':'grey', 'alpha':0.5, 'pad':10})
    ax.set_ylabel('intensity')
    ax.set_xlabel('m/z')
    autolabel_peaks(ax, peaks, decimals, mz_range + mz_plot_range_overhang, max_intensity*1.1,
                    abs_int=abs_int, rel_int = rel_int)
    plt.savefig(file_target)
    if show:
        plt.show()
    if close:
        plt.close()
    return
    