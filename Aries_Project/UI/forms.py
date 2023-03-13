# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:12:32 2023

@author: Vicky 
"""

from django import forms  
class DataForm(forms.Form):  
   
    file      = forms.FileField() # for creating file input  
    