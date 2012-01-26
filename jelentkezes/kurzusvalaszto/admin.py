from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from kurzusvalaszto.models import Kurzus, Targy, Felhasznalo

admin.site.unregister(User)

class KurzusAdmin(admin.ModelAdmin):
    list_display = ('nev', 'idopont_nap', 'idopont_sav', 'ferohely',
        'hallgatok')

admin.site.register(Kurzus, KurzusAdmin)

class TargyAdmin(admin.ModelAdmin):
    list_display = ('nev', 'kod')

admin.site.register(Targy, TargyAdmin)
     
class FelhasznaloInline(admin.StackedInline):
    model = Felhasznalo
     
class FelhasznaloAdmin(UserAdmin):
    inlines = [FelhasznaloInline]
     
admin.site.register(User, FelhasznaloAdmin)

