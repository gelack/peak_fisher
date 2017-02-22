# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 22:04:03 2017

@author: GLackner
"""
import os
import emzed
from emzed.core.data_types import Blob
import plot_tools as pl
import peak_search as ps



def add_file_targets(t, path, format_):
    def make_target(path, scan, rt):
        title = "scan_%s-RT_%s_m.%s" %(scan, rt/60, format_) 
        return os.path.join(path, title)
    t.addColumn("file_target", t.apply(make_target, (path, t.scan_number, t.rt)), type_= str)
    return t
    
    
def plot_specs_from_table(t, target_col="file_target", decimals=2):
    specs = t.spectrum.values
    targets = t.getColumn(target_col).values
    pairs = zip(specs, targets)
    for pair in pairs:
        spec, file_target = pair
        box_title = pl.create_box_title(spec)
        plot_title = "scan #%s" % (str(spec.scan_number))
        pl.plot_spectrum(spec, file_target, box_title=box_title, plot_title=plot_title, decimals=decimals, show=False, close=True)      
    t.dropColumns(target_col)
    return t

def load_blobs(t, target_col="file_target"):
    def open_blob(target):
        return emzed.io.loadBlob(path=target)
    t.addColumn("plot", t.apply(open_blob,(t.getColumn(target_col),)),type_=Blob)
    t.dropColumns(target_col)  
    return t

def gui_get_plot_params():
    format_choice = ['png', 'pdf', 'svg']
    params = emzed.gui.DialogBuilder('Workflow parameters')\
    .addInt("Number of decimals for spectrum plot", default=2, help="Number of decimals of mz values in spectrum plot")\
    .addChoice("Formate", format_choice, default=0,\
                           help='File format for spectra plot. Possible formats: pdf, png')\
    .addDirectory('Please choose result directory')\
    .show()
    decimals, format_select, path = params
    format_ = format_choice[format_select]
    return  decimals, format_, path
def parse_mz_list(mzs_text):
        mz_list_string =  mzs_text.splitlines()
        mz_list_float = []
        for item in mz_list_string:
            fl = float(item)
            mz_list_float.append(fl)
        return mz_list_float

def gui_get_n(mode, mz_list): 
    if mode == "minimum":
        n = emzed.gui.DialogBuilder('Choose minimum number of peaks')\
        .addInt("minimum number of peaks", default=1, help="For a hit, require a minumum of n peaks")\
        .show()
        m = len(mz_list)
        if n == m:
            mode = "all"
        elif n>m:
            print "Careful: n > number of peaks provided!"
            print 'Setting search mode to "all"'
            mode = "all"
    else:
        n=None
    return mode, n

def gui_get_params():
    DialogBuilder = emzed.gui.DialogBuilder
    mode_choice = ['all', 'minimum']
    
    params = DialogBuilder('Workflow parameters')\
    .addFileOpen('select peakmap',formats=['mzXML', 'mzML'])\
    .addInt('MS level', default=2, help="MS level of spectra to search. Is an integer n for MSn, e.g. 2 for MS2")\
    .addFloat('relative noise threshold', default=0.01, help='Minimal relative intensity to define  peak as existing')\
    .addFloat("MZ tolerance in ppm", default=5.0, help="relative MZ tolerance for targeted identification")\
    .addChoice('Search mode', mode_choice, default=0,\
                help='For a hit, require all mz values in a list to be found or a minimum of n peaks')\
    .addText('mz values of peaks (separated by line break)', help="Enter mz values of peaks to search for, separated by line breaks")\
    .show()
    peakmap_path, ms_level, rel_noise_threshold, mz_tol_ppm, mode_select, mz_text = params
    mz_tol = mz_tol_ppm*1e-6  
    mz_list = parse_mz_list(mz_text)
    mode = mode_choice[mode_select]

    mode, n = gui_get_n(mode, mz_list)
     
    search_params =  (ms_level, rel_noise_threshold, mz_tol, mz_list, mode, n)
    return peakmap_path, search_params

def search_peaks(pm, *search_params):
    ms_level, rel_noise_threshold, mz_tol, mz_list, mode, n = search_params
    print "Searching for peaks", mz_list
    if mode == "all":
        results = ps.find_spectra_with_all_mz(pm, mz_list,ms_level=ms_level, mz_tol=mz_tol, rel_noise_threshold=rel_noise_threshold)
    elif mode == "minimum":
        results = ps.find_spectra_with_n_mz(pm, n, mz_list,ms_level=ms_level, mz_tol=mz_tol, rel_noise_threshold=rel_noise_threshold)
    else: print "unknown search mode", mode
    return results

def show_results(results, *args):     #decimals, plot_format, result_path
    decimals, plot_format, result_path = args
    results = add_file_targets(results, result_path, "png")         
    results = plot_specs_from_table(results, decimals=decimals)
    results = add_file_targets(results, result_path, "png")  
    results = load_blobs(results)
    if plot_format != "png":
        results = add_file_targets(results, result_path, plot_format)         
        results = plot_specs_from_table(results, decimals=decimals)
    results.dropColumns("spectrum")
    emzed.gui.inspect(results)
    return results

def save_results(results, *args):
    decimals, plot_format, result_path = args
    target =os.path.join(result_path,"result.table")
    emzed.io.storeTable(results, target, forceOverwrite=True)
    emzed.gui.showInformation('Result is saved')

def reload_results(__):
    result_path=emzed.gui.askForSingleFile(extensions=['table'])
    results = emzed.io.loadTable(result_path)
    emzed.gui.inspect(results)
    return
    
def run_peak_fisher(__):
    peakmap_path, search_params= gui_get_params() #search_params: ms_level, rel_noise_threshold, mz_tol, mz_list, mode, n
    plot_params = gui_get_plot_params() #decimals, plot_format, result_path
    pm = emzed.io.loadPeakMap(peakmap_path)
    results = search_peaks(pm, *search_params)
    if results:
        results = show_results(results, *plot_params)
        save_results(results, *plot_params)
    else:
        print 'No MS spectra with matching mz values'
    return


    
       
def main_workflow():
    emzed.gui.DialogBuilder('Please select a task...   ')\
    .addButton('Run Peak Fisher', run_peak_fisher)\
    .addButton('Reload results', reload_results)\
    .show()

if __name__=='__main__':
    main_workflow()



 
