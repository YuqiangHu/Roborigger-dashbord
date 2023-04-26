from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('generatePdf/', views.generatePdf, name='generatePdf'),
    path('makepdf/', views.makepdf, name='makepdf'),
]