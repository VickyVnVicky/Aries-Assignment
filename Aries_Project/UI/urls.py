# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:20:28 2023

@author: Vicky 
"""


from django.urls import path  
from UI import views  
urlpatterns = [  
    #path('admin/', admin.site.urls),  
    path('',views.Base_UI),
    path('file_upload', views.index,name="file_upload"),  
    path('data/',views.Show_data,name="data"),
    path('download/', views.download_file,name="download"),
    path('home/',views.home,name="home")
]  