from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Invoice)
admin.site.register(models.Product)
admin.site.register(models.Customer)
admin.site.register(models.InvoiceItem)
admin.site.register(models.Payment)
