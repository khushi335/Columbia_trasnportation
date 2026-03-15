from django.contrib import admin
from .models import Service,CarReservation,Reservation,Fleet, FleetImage, FleetCategory

# Register your models here.
@admin.register(CarReservation)
class CarReservationAdmin(admin.ModelAdmin):
    list_display = (
        'car_type',
        'pick_up_location',
        'drop_off_location',
        'pick_up_date',
        'pick_up_time',
        'drop_off_date',
        'drop_off_time',
        'email',
        'created_at',
    )
    list_filter = ('car_type', 'pick_up_date', 'drop_off_date', 'created_at')
    search_fields = ('pick_up_location', 'drop_off_location', 'email')
    ordering = ('-created_at',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title']
    
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "service_type",
        "vehicle_class",
        "pickup",
        "dropoff",
        "pickup_date",
        "pickup_time",
        "created_at",
    )
    list_filter = ("service_type", "vehicle_class", "pickup_date", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone", "pickup", "dropoff", "flight_number")
    ordering = ("-created_at",)
    date_hierarchy = "pickup_date"
    
class FleetImageInline(admin.TabularInline):
    model = FleetImage
    extra = 1

@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    inlines = [FleetImageInline]
    list_display = ('name', 'vehicle_class', 'passengers', 'price_per_hour', 'category')

admin.site.register(FleetCategory)