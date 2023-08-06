#encoding:utf-8
from .forms import *
from .models import *
# from django.db.models import get_app, get_models
from django.apps import apps
#from django.db.models import get_app, get_models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_microsip_base.libs.models_base.models import Articulo,ArticuloPrecio,ArticuloClave, Moneda, PrecioEmpresa,Registry,ClienteDireccion, Cliente, CondicionPago, Vendedor, VentasDocumento, VentasDocumentoDetalle, Almacen,ClienteClave,VentasDocumentoLiga
from django.contrib.auth.models import User
from datetime import datetime
from django.forms.models import inlineformset_factory
from django.forms import formset_factory
# Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list import ListView
from django.db import router, connections,connection
from django.core import management
from microsip_api.comun.sic_db import first_or_none
from .storage import send_mail_orden
# Python
import time
import json
import os
import pdb
import re, io
# import cStringIO as StringIO
from io import StringIO
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from datetime import date,datetime,timedelta
from django.db.models import Q
from xhtml2pdf import pisa
from base64 import decodestring
from django.core.files import File
import onesignal as onesignal_sdk


@login_required(login_url='/login/')
def index(request):

	context={}
	return render(request, 'djlicencias_sic/index.html',context)

def insert_licencia(request):
	no_serie_hdd = request.GET.get('hdd_serial')
	fecha_vencimiento=request.GET.get('fecha')

	Licencias.objects.create(
		no_serie_hdd = no_serie_hdd,
		fecha_vencimiento = fecha_vencimiento,
	)

	return HttpResponse()
