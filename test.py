# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:47:09 2017

@author: GLackner
"""
import emzed
mode_choice = ['all', 'minimum']
mode_select = emzed.gui.DialogBuilder('Choose search mode')\
    .addChoice('Search mode', mode_choice, default=0,\
                       help='For a hit, require all mz values in a list to be found or a minimum of n peaks')\
    .show()
mode = mode_choice[mode_select]