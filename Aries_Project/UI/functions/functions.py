# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:22:29 2023

@author: Vicky 
"""

def handle_uploaded_file(f):  
    with open('UI/static/upload/'+f.name, 'wb+') as destination:  
       
        for chunk in f.chunks():  
            destination.write(chunk)  