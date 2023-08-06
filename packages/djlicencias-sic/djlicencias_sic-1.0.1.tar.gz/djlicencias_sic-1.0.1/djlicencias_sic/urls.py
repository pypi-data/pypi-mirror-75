# from django.conf.urls import patterns, url
from django.urls import path,include
from .views import *

urlpatterns = (
	path('', index),
	# path('info_cliente/', info_cliente),
)

  