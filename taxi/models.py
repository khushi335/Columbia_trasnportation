from django.db import models
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver


# Create your models here.
# class CarReservation(models.Model):
#     CAR_CHOICES = [
#         ('', 'Select your Car type'),("sedan","Sedan"), ("suv","SUV"), ("van","Van"), ("luxury","Luxury")
#     ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
#     car_type = models.CharField(max_length=50, choices=CAR_CHOICES)
#     pick_up_location = models.CharField(max_length=255)
#     drop_off_location = models.CharField(max_length=255)
#     pick_up_date = models.DateField()
#     pick_up_time = models.TimeField()
#     drop_off_date = models.DateField()
#     drop_off_time = models.TimeField()
#     email = models.EmailField(blank=True, null=True)  # Auto-filled for logged-in users
#     # phone_number = models.CharField(max_length=20, blank=True, null=True)  # Optional
#     created_at = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return f"{self.car_type} reservation for {self.user if self.user else 'Guest'}"

class CarReservation(models.Model):
    CAR_CHOICES = [
        ('', 'Select your Car type'),
        ("sedan", "Sedan"),
        ("suv", "SUV"),
        ("van", "Van"),
        ("luxury", "Luxury"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    car_type = models.CharField(max_length=50, choices=CAR_CHOICES)
    pick_up_location = models.CharField(max_length=255)
    drop_off_location = models.CharField(max_length=255)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    drop_off_date = models.DateField()
    drop_off_time = models.TimeField()
    email = models.EmailField(blank=False, null=False)  # user email
    phone_number = models.CharField(max_length=10, blank=False, null=False)  # ✅ phone number
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_type} reservation for {self.email if self.email else 'Guest'}"

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
SERVICE_CHOICES = [
    ('airport', 'Airport'),
    ('point_to_point', 'Point To Point'),
    ('hourly', 'Hourly'),
    ('frederick', 'Frederick Special Services'),
]

class Reservation(models.Model):
    SERVICE_TYPES = [
        ("point_to_point","Point to Point"),
        ("round_trip","Round Trip"),
        ("hourly","Hourly"),
    ]
    VEHICLE_CLASSES = [
        ("sedan","Sedan"), ("suv","SUV"), ("van","Van"), ("luxury","Luxury")
    ]

    created_at = models.DateTimeField(auto_now_add=True)

    service_type = models.CharField(max_length=40, choices=SERVICE_TYPES)
    vehicle_class = models.CharField(max_length=40, choices=VEHICLE_CLASSES)
    passengers = models.PositiveIntegerField(default=1)
    luggage = models.PositiveIntegerField(default=0)

    pickup = models.CharField(max_length=255)
    dropoff = models.CharField(max_length=255, blank=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()

    return_pickup = models.CharField(max_length=255, blank=True)
    return_dropoff = models.CharField(max_length=255, blank=True)
    return_date = models.DateField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)

    hours = models.PositiveIntegerField(null=True, blank=True)
    wait_time = models.PositiveIntegerField(null=True, blank=True)

    flight_number = models.CharField(max_length=64, blank=True)
    child_seat = models.CharField(max_length=32, blank=True)
    child_seat_qty = models.PositiveIntegerField(default=0)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    email = models.EmailField()
    payment_method = models.CharField(max_length=64)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.pickup_date} {self.pickup_time}"
        
class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    project = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class FleetCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Fleet(models.Model):
    category = models.ForeignKey(FleetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    vehicle_class = models.CharField(max_length=50)
    passengers = models.PositiveIntegerField()
    luggage = models.PositiveIntegerField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    main_image = models.ImageField(upload_to='fleet/')
    
    def __str__(self):
        return self.name

class FleetImage(models.Model):
    fleet = models.ForeignKey(Fleet, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fleet/gallery/')

    def __str__(self):
        return f"{self.fleet.name} Image"
        
class Location(models.Model):
    AREA_CHOICES = (
        ('area', 'Area'),
        ('airport', 'Airport'),
    )

    name = models.CharField(max_length=255, unique=True)
    location_type = models.CharField(max_length=20, choices=AREA_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.location_type})"


# ------------------------
# Auto-populate default locations
# ------------------------

@receiver(post_migrate)
def populate_default_locations(sender, **kwargs):
    if sender.name != __name__.split('.')[0]:
        return  # only run for this app

    default_locations = [
        # Maryland
        ("Baltimore", "area"),
        ("Columbia", "area"),
        ("Silver Spring", "area"),
        ("Annapolis", "area"),
        ("Frederick", "area"),
        ("Rockville", "area"),
        ("Ellicott City", "area"),
        ("Bethesda", "area"),

        # Washington D.C.
        ("Downtown", "area"),
        ("Capitol Hill", "area"),
        ("Georgetown", "area"),
        ("Dupont Circle", "area"),
        ("Adams Morgan", "area"),
        ("National Mall", "area"),
        ("Union Station", "area"),

        # Virginia
        ("Arlington", "area"),
        ("Alexandria", "area"),
        ("Tysons Corner", "area"),
        ("Fairfax", "area"),
        ("McLean", "area"),
        ("Reston", "area"),
        ("Falls Church", "area"),
        ("Vienna", "area"),

        # Airports
        ("BWI- BALTIMORE WASHINGTON INTERNATIONAL", "airport"),
        ("DCA- RONALD REAGAN NATIONAL AIRPORT", "airport"),
        ("IAD- WASHINGTON DULLES INTERNATIONAL", "airport"),
        ("PHL- PHILADELPHIA INTERNATIONAL", "airport"),
    ]

    for name, loc_type in default_locations:
        Location.objects.get_or_create(name=name, location_type=loc_type)
