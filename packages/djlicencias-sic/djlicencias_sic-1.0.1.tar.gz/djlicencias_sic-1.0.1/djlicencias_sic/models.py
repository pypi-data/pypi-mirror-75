from django.db import models
#Python
from datetime import datetime
#Own
from multiselectfield import MultiSelectField
from .storage import OverwriteStorage
from django_microsip_base.libs.models_base.models import VentasDocumento,VendedorBase



class Licencias(models.Model):
    cliente_id=models.IntegerField(blank=True, null=True, db_column='CLIENTE_ID')
    no_serie_hdd= models.CharField(max_length=50,db_column='NO_SERIE_HDD',null=True)
    no_licencias=models.IntegerField(blank=True, null=True, db_column='NO_LICENCIAS')
    tipo_licencia=models.CharField(max_length=50,db_column='TIPO_LICENCIA',null=True)
    fecha_vencimiento = models.DateField(db_column='FECHA_VENCIMIENTO')
    no_serie=models.CharField(max_length=50,db_column='NO_SERIE',null=True)

    class Meta:
        db_table = 'SIC_LICENCIAS'
        abstract = True
        app_label = 'models_base'