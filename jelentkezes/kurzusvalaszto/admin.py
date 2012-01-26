from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from kurzusvalaszto.models import Kurzus, Targy, Felhasznalo

admin.site.unregister(User)

admin.site.register(Kurzus)
admin.site.register(Targy)
     
class FelhasznaloInline(admin.StackedInline):
    model = Felhasznalo
     
class FelhasznaloAdmin(UserAdmin):
    inlines = [FelhasznaloInline]
     
admin.site.register(User, FelhasznaloAdmin)

