# Django
from django import forms 
from datetime import date
from django.forms.models import inlineformset_factory
import autocomplete_light
from django_select2 import forms as s2forms
from .models import *
from django_microsip_base.libs.models_base.models import VentasDocumentoDetalle, VentasDocumento, Articulo, Cliente, Almacen, ClienteDireccion, CondicionPago, Vendedor,Registry
from django.conf import settings
class PreferenciasManageForm(forms.Form):
	articulo = forms.ModelChoiceField(queryset=Articulo.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class': 'form-control'}))
	logo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
	imagen_extra = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
	url_pdf_destino=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}),)
	email=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}),)
	password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control'}),)
	servidor_correo = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}),)
	puerto=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control'}),)
	def save(self, *args, **kwargs):
		articulo = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Articulo_predeterminado')
		articulo.valor = self.cleaned_data['articulo'].id
		articulo.save()
		
		logo = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Logo')
		logo.valor = self.cleaned_data['logo']
		logo.save()
		
		imagen_extra = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Imagen_extra')
		imagen_extra.valor = self.cleaned_data['imagen_extra']
		imagen_extra.save()
		
		url_pdf_destino = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Url_Pdf_Destino')
		url_pdf_destino.valor = self.cleaned_data['url_pdf_destino']
		url_pdf_destino.save()

		email = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Email')
		email.valor = self.cleaned_data['email']
		email.save()

		password = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Password')
		password.valor = self.cleaned_data['password']
		password.save()

		servidor_correo = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Servidro_Correo')
		servidor_correo.valor = self.cleaned_data['servidor_correo']
		servidor_correo.save()

		puerto = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Puerto')
		puerto.valor = self.cleaned_data['puerto']
		puerto.save()
		
class FindFrom(forms.Form):
	llamada=forms.BooleanField(required=False)
	inicio=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}),required=False,initial=date.today)
	fin=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}),required=False,initial=date.today)
	busqueda=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','place-holder':'Ingrese criterio de busqueda'}), required=False)
	FILTRO = (
		(u'', u'-------------'),
		(u'EP', u'En Proceso'),
		(u'PDA', u'Pendiente de Asignar'), 
		(u'F', u'Finalizado'),
		)
	filtro = forms.ChoiceField(choices=FILTRO,widget=forms.Select(attrs={'class': 'form-control'}), required=False)
	TIPO_DOCUMENTO = (
		(u'', u'-------------'),
		(u'F', u'Facturado'),
		(u'R', u'Remisionado'),
		)
	tipo_documento = forms.ChoiceField(choices=TIPO_DOCUMENTO,widget=forms.Select(attrs={'class': 'form-control'}), required=False)	