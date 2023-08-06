from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin
# Register your models here.
from .models import User, Vehicle, ParkingSpot, Destination


#admin.site.register(User)
admin.site.register(Vehicle)

@admin.register(ParkingSpot)
class ParkingSpotAdmin(OSMGeoAdmin):
    list_display = ('owner', 'location')

@admin.register(Destination)
class ParkingSpotAdmin(OSMGeoAdmin):
    list_display = ('user', 'location')
# class ChoiceInline(admin.TabularInline):
#     model = Vehicle
#     extra = 1
#
#
# class UserAdmin(admin.ModelAdmin):
#     fieldsets = [(None, {'fields': ["first_name", "last_name"]}),
#                  ('Date Information', {'fields': ['date_joined'], 'classes': ['collapse']}), ]
#     inlines = [ChoiceInline]
#
#
# admin.site.register(User,UserAdmin)