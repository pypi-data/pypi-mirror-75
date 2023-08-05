from django.contrib import admin
from .models import SoftwareProvider, SoftwareType, Software, LicenceType, Licence

@admin.register(SoftwareProvider)
class SoftwareProviderAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SoftwareType)
class SoftwareTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('name','softtype','provider',)

@admin.register(LicenceType)
class LicenceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ('inventory_number',
        'licencetype',
        'date_created',
        'date_valid',
        'amount',
        'software',
        'tenant',
        'site'
    )
