# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 08:18:41 2017

@author: GLackner
"""

import emzed
from emzed.core.data_types import Spectrum


def find_spectra_with_all_mz(pm, mz_list, ms_level=None, mz_tol = 5e-6, rel_noise_threshold=0.01):
    """find all ms2_spectra containing MS2 peaks with given mz within relative mz_tol,
        more intense than rel_noise_threshold. Result is a table with Scan number, precursor mass, precursor rt"""
    if ms_level:
        search_spectra = pm.levelNSpecs(ms_level)
    else:
        search_spectra = pm.spectra
    for mz in mz_list:
        hit_spectra = []
        for spec in search_spectra:
            if find_mz_in_spec(spec, mz, mz_tol=mz_tol, rel_noise_threshold=rel_noise_threshold):
                hit_spectra.append(spec)
        search_spectra = hit_spectra
    return spectra_list_toTable(hit_spectra)

def find_spectra_with_n_mz(pm, n, mz_list, ms_level=None, mz_tol = 5e-6, rel_noise_threshold=0.01):
    """find ms2_spectra containing a minimum of n MS2 peaks with given mz within relative mz_tol,
        more intense than rel_noise_threshold. Result is a table with Scan number, precursor mass, precursor rt"""
    if ms_level:
        search_spectra = pm.levelNSpecs(ms_level)
    else:
        search_spectra = pm.spectra
    hit_spectra = []
    for spec in search_spectra:
        hits = 0
        for mz in mz_list:
            if find_mz_in_spec(spec, mz, mz_tol=mz_tol, rel_noise_threshold=rel_noise_threshold):
                hits = hits + 1
            if hits >= n:
                hit_spectra.append(spec)            
    return spectra_list_toTable(hit_spectra)

def define_mz_range(mz, mz_tol):
    mzmin = mz - mz_tol*mz
    mzmax = mz + mz_tol*mz
    return mzmin, mzmax     

def spec_number_of_peaks(spec):
    return spec.peaks.shape[0]
def spectra_list_toTable(spectra_list):
    if (len(spectra_list)==0):
        return None
    else:
        scan_number_list = []
        precursor_list = []
        rt_list = []
        for spec in spectra_list:
            scan_number_list.append(spec.scan_number)
            precursor_list.append(spec.precursors[0][0])
            rt_list.append(spec.rt)
        t=emzed.utils.toTable("spectrum", spectra_list, type_=Spectrum)
        t.addColumn("scan_number", scan_number_list, type_=int, insertBefore="spectrum")
        t.addColumn("precursor", precursor_list, type_=float, format_="%4f", insertBefore="spectrum")
        t.addColumn("rt", rt_list, type_=float, format_="%1f", insertBefore="spectrum")
        return t

def find_mz_in_spec(spec, mz, mz_tol=5e-6, rel_noise_threshold=0.01):
    mzmin, mzmax = define_mz_range(mz, mz_tol)    
    max_int = spec.maxIntensity()
    n = spec_number_of_peaks(spec)
    for i in range(n):
        peak_int = spec.peaks[i,1]
        peak_mz = spec.peaks[i,0]
        if (peak_int/max_int >=rel_noise_threshold) & (mzmin < peak_mz <mzmax):
            return True
    return False



