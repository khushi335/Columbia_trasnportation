from django.shortcuts import render,redirect,get_object_or_404
from .models import Service,Reservation,CarReservation,Fleet, FleetCategory, Location
from .forms import ReservationForm,CarReservationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.views.decorators.http import require_POST
# from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.models import AbstractUser
# CustomUser = get_user_model()
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import json
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseBadRequest
from urllib.parse import urlencode
from django.http import HttpResponse

# def index(request):
#     if request.method == "POST":
#         form = CarReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save()

#             user_message = f"""
# Dear {reservation.email},

# Thank you for booking with us!
# Your reservation details:
# Car: {reservation.car_type}
# Pick-up: {reservation.pick_up_location} on {reservation.pick_up_date} at {reservation.pick_up_time}
# Drop-off: {reservation.drop_off_location} on {reservation.drop_off_date} at {reservation.drop_off_time}

# We will contact you soon for confirmation.
# """

#             admin_message = f"""
# New Reservation Received:
# Email: {reservation.email}
# Car: {reservation.car_type}
# Pick-up: {reservation.pick_up_location} ({reservation.pick_up_date} {reservation.pick_up_time})
# Drop-off: {reservation.drop_off_location} ({reservation.drop_off_date} {reservation.drop_off_time})
# """

#             try:
#                 send_mail(
#                     "Car Reservation Confirmation",
#                     user_message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [reservation.email]
#                 )
#                 send_mail(
#                     "New Car Reservation",
#                     admin_message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [settings.DEFAULT_FROM_EMAIL, "sahkhushi946@gmail.com"]
#                 )
#             except Exception as e:
#                 print("Email failed:", e)

#             # If AJAX request, return JSON
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({"success": True, "message": "Your reservation has been submitted successfully!"})

#             messages.success(request, "Your reservation has been submitted successfully!")
#             return redirect("index")
#         else:
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 errors = form.errors.as_json()
#                 return JsonResponse({"success": False, "errors": errors})

#             messages.error(request, "Please correct the errors in the form.")
#     else:
#         form = CarReservationForm()

#     return render(request, "taxi/index.html", {"reservation_form": form})

# def index(request):
#     """Home page with reservation form."""
#     if request.method == "POST":
#         form = CarReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             # Save reservation to database
#             reservation.save()
#             # Show success message
#             messages.success(request, "Your reservation has been submitted successfully!")
#             return redirect("index")
#         else:
#             messages.error(request, "Please correct the errors in the form.")
#     else:
#         form = CarReservationForm()

#     context = {
#         "reservation_form": form,
#     }
#     return render(request, "taxi/index.html", context)

# def index(request):
#     if request.method == "POST":
#         form = CarReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save()

#             # --- Email messages ---
#             subject_user = "Car Reservation Confirmation"
#             message_user = f"""
# Dear {reservation.email},

# Thank you for booking with us!
# Your reservation details:
# Car: {reservation.car_type}
# Pick-up: {reservation.pick_up_location} on {reservation.pick_up_date} at {reservation.pick_up_time}
# Drop-off: {reservation.drop_off_location} on {reservation.drop_off_date} at {reservation.drop_off_time}

# We will contact you soon for confirmation.
# """
#             subject_admin = "New Car Reservation Received"
#             message_admin = f"""
# New Reservation Received:
# Email: {reservation.email}
# Car: {reservation.car_type}
# Pick-up: {reservation.pick_up_location} ({reservation.pick_up_date} {reservation.pick_up_time})
# Drop-off: {reservation.drop_off_location} ({reservation.drop_off_date} {reservation.drop_off_time})
# """

#             try:
#                 # Email to user
#                 send_mail(subject_user, message_user, settings.DEFAULT_FROM_EMAIL, [reservation.email])
#                 # Email to admin and aaa@gmail.com
#                 send_mail(subject_admin, message_admin, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL, "sahkhushi946@gmail.com"])
#             except Exception as e:
#                 print("Email sending failed:", e)

#             messages.success(request, "Your reservation has been submitted successfully!")
#             return redirect("index")
#         else:
#             messages.error(request, "Please correct the errors in the form.")
#     else:
#         form = CarReservationForm()

#     context = {"reservation_form": form}
#     return render(request, "taxi/index.html", context)

# def index(request):
#     """Home page with reservation form and email notifications."""
#     if request.method == "POST":
#         form = CarReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save()

#             # Recipient emails
#             user_email = reservation.email
#             admin_email = settings.ADMIN_EMAIL
#             host_email = settings.EMAIL_HOST_USER
#             default_email = settings.DEFAULT_FROM_EMAIL

#             try:
#                 # Email to user
#                 if user_email:
#                     send_mail(
#                         "Your Car Reservation Confirmation",
#                         f"Dear Customer,\n\nThank you for booking!\n"
#                         f"Car: {reservation.car_type}\n"
#                         f"Pick-up: {reservation.pick_up_location} ({reservation.pick_up_date} {reservation.pick_up_time})\n"
#                         f"Drop-off: {reservation.drop_off_location} ({reservation.drop_off_date} {reservation.drop_off_time})",
#                         default_email,
#                         [user_email],
#                         fail_silently=True
#                     )

#                 # Email to Admin
#                 send_mail(
#                     "New Car Reservation Received",
#                     f"New reservation:\nUser Email: {reservation.email}\n"
#                     f"Car: {reservation.car_type}\n"
#                     f"Pick-up: {reservation.pick_up_location} ({reservation.pick_up_date} {reservation.pick_up_time})\n"
#                     f"Drop-off: {reservation.drop_off_location} ({reservation.drop_off_date} {reservation.drop_off_time})",
#                     default_email,
#                     [admin_email],
#                     fail_silently=True
#                 )

#                 # Email to Host
#                 send_mail(
#                     "Car Reservation Notification",
#                     f"Reservation Details:\nCustomer Email: {reservation.email}\n"
#                     f"Car: {reservation.car_type}\n"
#                     f"Pick-up: {reservation.pick_up_location} ({reservation.pick_up_date} {reservation.pick_up_time})\n"
#                     f"Drop-off: {reservation.drop_off_location} ({reservation.drop_off_date} {reservation.drop_off_time})",
#                     default_email,
#                     [host_email],
#                     fail_silently=True
#                 )

#                 # Return JSON success for AJAX
#                 if request.headers.get("x-requested-with") == "XMLHttpRequest":
#                     return JsonResponse({"success": True, "message": "Reservation submitted successfully! Emails sent."})

#             except Exception as e:
#                 # Return JSON error for AJAX
#                 if request.headers.get("x-requested-with") == "XMLHttpRequest":
#                     return JsonResponse({"success": False, "error": "Reservation submitted, but email failed. Contact admin."})
#                 print("Email error:", e)

#             # Non-AJAX fallback
#             messages.success(request, "Your reservation has been submitted successfully! Emails sent.")
#             return redirect("index")

#         else:
#             # Form invalid
#             if request.headers.get("x-requested-with") == "XMLHttpRequest":
#                 errors = form.errors.as_json()
#                 return JsonResponse({"success": False, "error": "Please correct the errors in the form.", "form_errors": errors})
#             messages.error(request, "Please correct the errors in the form.")

#     else:
#         form = CarReservationForm()

#     context = {"reservation_form": form}
#     return render(request, "taxi/index.html", context)

def index(request):
    """Home page with reservation form, email notifications, and location autocomplete."""

    # --- Autocomplete endpoint ---
    q = request.GET.get("q", "").strip()
    autocomplete_type = request.GET.get("type", "")  # 'pick' or 'drop'
    if q and autocomplete_type in ["pick", "drop"]:
        # Filter locations containing the query, limit 10 results
        locations = Location.objects.filter(name__icontains=q)[:10]
        data = [{"id": loc.id, "name": loc.name} for loc in locations]
        return JsonResponse({"locations": data})

    # --- Handle POST reservation form ---
    if request.method == "POST":
        form = CarReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            user_email = reservation.email
            admin_email = settings.ADMIN_EMAIL
            host_email = settings.EMAIL_HOST_USER
            default_email = settings.DEFAULT_FROM_EMAIL

            try:
                # Email to user
                if user_email:
                    send_mail(
                        "Your Car Reservation Confirmation",
                        f"Dear Customer,\n\nThank you for booking!\n"
                        f"Car: {reservation.car_type}\n"
                        f"Pick-up: {reservation.pick_up_location} ({reservation.pick_up_date} {reservation.pick_up_time})\n"
                        f"Drop-off: {reservation.drop_off_location} ({reservation.drop_off_date} {reservation.drop_off_time})",
                        default_email,
                        [user_email],
                        fail_silently=False
                    )

                # Email to Admin
                send_mail(
                    "New Car Reservation Received",
                    f"New reservation:\nUser Email: {reservation.email}\n"
                    f"Car: {reservation.car_type}\n"
                    f"Pick-up: {reservation.pick_up_location} ({reservation.pick_up_date} {reservation.pick_up_time})\n"
                    f"Drop-off: {reservation.drop_off_location} ({reservation.drop_off_date} {reservation.drop_off_time})",
                    default_email,
                    [admin_email],
                    fail_silently=False
                )

                # Email to Host
                send_mail(
                    "Car Reservation Notification",
                    f"Reservation Details:\nCustomer Email: {reservation.email}\n"
                    f"Car: {reservation.car_type}\n"
                    f"Pick-up: {reservation.pick_up_location} ({reservation.pick_up_date} {reservation.pick_up_time})\n"
                    f"Drop-off: {reservation.drop_off_location} ({reservation.drop_off_date} {reservation.drop_off_time})",
                    default_email,
                    [host_email],
                    fail_silently=False
                )

                # Return JSON success for AJAX
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"success": True, "message": "Reservation submitted successfully! Emails sent."})

            except Exception as e:
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "error": "Reservation submitted, but email failed. Contact admin."})
                print("Email error:", e)

            # Non-AJAX fallback
            messages.success(request, "Your reservation has been submitted successfully! Emails sent.")
            return redirect("index")

        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                errors = form.errors.as_json()
                return JsonResponse({"success": False, "error": "Please correct the errors in the form.", "form_errors": errors})
            messages.error(request, "Please correct the errors in the form.")

    else:
        form = CarReservationForm()

    context = {"reservation_form": form}
    return render(request, "taxi/index.html", context)

def services_list(request):
    services = Service.objects.all()
    return render(request, 'taxi/services_list.html', {'services': services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'taxi/service_detail.html', {'service': service})

def blog(request):
    return render(request, 'taxi/blog.html')

def point_to_point_service(request):
    return render(request, 'taxi/point_to_point_service.html')

def airport_transportation(request):
    return render(request, 'taxi/airport_transportation.html')

def van(request):
    return render(request, 'taxi/van.html')

def hourly(request):
    return render(request, 'taxi/hourly.html')

def corporate(request):
    return render(request, 'taxi/corporate.html')

def wine(request):
    return render(request, 'taxi/wine.html')

def group(request):
    return render(request, 'taxi/group.html')

def private(request):
    return render(request, 'taxi/private.html')

def bachelor(request):
    return render(request, 'taxi/bachelor.html')

def wedding(request):
    return render(request, 'taxi/wedding.html')

def bus(request):
    return render(request, 'taxi/bus.html')

def exotic(request):
    return render(request, 'taxi/exotic.html')

def service(request):
    return render(request, 'taxi/service.html')

def bwi(request):
    return render(request, 'taxi/bwi.html')

def dca(request):
    return render(request, 'taxi/dca.html')

def phl(request):
    return render(request, 'taxi/phl.html')

def iad(request):
    return render(request, 'taxi/iad.html')

def about(request):
    return render(request, 'taxi/about.html')

def feature(request):
    return render(request, 'taxi/feature.html')

def team(request):
    return render(request, 'taxi/team.html')


def error(request):
    return render(request, 'taxi/404.html')


def testimonial(request):
    return render(request, 'taxi/testimonial.html')


def cars(request):
    return render(request, 'taxi/cars.html')

def contact(request):
    contact_info = {
        "description": "You can reach us via the form below or through our contact details.",
        "items": [
            {"icon": "fas fa-map-marker-alt", "title": "Address", "content": "123 Street, New York, USA"},
            {"icon": "fas fa-envelope", "title": "Mail Us", "content": "info@example.com"},
            {"icon": "fa fa-phone-alt", "title": "Telephone", "content": "(+012) 3456 7890"},
            {"icon": "fab fa-firefox-browser", "title": "Website", "content": "yoursite@ex.com"},
        ],
    }

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not (name and email and subject and message):
            messages.error(request, "All fields are required.")
            return redirect("contact")

        # Email to Admin
        admin_subject = f"New Contact Inquiry from {name}"
        admin_message = f"""
        You have received a new contact inquiry:

        Name: {name}
        Email: {email}
        Subject: {subject}
        Message: {message}
        """
        send_mail(
            admin_subject,
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  # defined in settings.py
            fail_silently=False,
        )

        # Email to User
        user_subject = "Thank you for contacting us!"
        user_message = f"""
        Dear {name},

        Thank you for reaching out to us. We have received your inquiry and our team will get back to you soon.

        Your submitted details:
        Subject: {subject}
        Message: {message}

        Best regards,  
        {settings.DEFAULT_FROM_EMAIL}
        """
        send_mail(
            user_subject,
            user_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],  # send to the user
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "taxi/contact.html", {"contact_info": contact_info})

# def reservation(request):
#     if request.method == 'POST':
#         # Collect form data
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         service_type = request.POST.get('service_type')
#         vehicle_class = request.POST.get('vehicle_class')
#         passengers = request.POST.get('passengers')
#         luggage = request.POST.get('luggage')
#         total_price = request.POST.get('total_price')  # pass via hidden input
#         payment_method = request.POST.get('payment_method')

#         # Send email to admin, user, and your email
#         subject = "New Reservation Received"
#         message = f"""
# Reservation Details:

# Name: {first_name} {last_name}
# Email: {email}
# Phone: {phone}
# Service Type: {service_type}
# Vehicle Class: {vehicle_class}
# Passengers: {passengers}
# Luggage: {luggage}
# Total Price: ${total_price}
# Payment Method: {payment_method}
# """
#         recipients = [settings.DEFAULT_FROM_EMAIL, email, 'sahkhushi946@gmail.com']
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)

#         # Redirect to PayPal if chosen
#         if payment_method == 'paypal':
#             paypal_url = settings.PAYPAL_URL  # e.g., 'https://www.paypal.com/cgi-bin/webscr'
#             business_email = settings.PAYPAL_PERSONAL_EMAIL

#             params = {
#                 'cmd': '_xclick',
#                 'business': business_email,
#                 'item_name': f'Reservation by {first_name} {last_name}',
#                 'amount': total_price,
#                 'currency_code': 'USD',
#                 'return': request.build_absolute_uri('/reservation-success/'),
#                 'cancel_return': request.build_absolute_uri('/payment-cancelled/'),
#             }
#             redirect_url = f"{paypal_url}?{urlencode(params)}"
#             return redirect(redirect_url)

#         # Otherwise, show reservation success page
#         return redirect('reservation_success')

#     # GET method
#     return render(request, 'taxi/reservation.html', {'paypal_client_id': settings.PAYPAL_CLIENT_ID})


# def reservation(request):
#     if request.method == 'POST':
#         # Collect form data
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         service_type = request.POST.get('service_type')
#         vehicle_class = request.POST.get('vehicle_class')
#         passengers = request.POST.get('passengers')
#         luggage = request.POST.get('luggage')
#         total_price = request.POST.get('total_price')  # hidden input in form
#         payment_method = request.POST.get('payment_method')

#         # Construct email content
#         subject = "🚖 New Reservation Received"
#         message = f"""
# Reservation Details:

# Name: {first_name} {last_name}
# Email: {email}
# Phone: {phone}
# Service Type: {service_type}
# Vehicle Class: {vehicle_class}
# Passengers: {passengers}
# Luggage: {luggage}
# Total Price: ${total_price}
# Payment Method: {payment_method}
# """

#         try:
#             recipients = [
#                 settings.DEFAULT_FROM_EMAIL,        # business email
#                 email,                              # user
#                 "sahkhushi946@gmail.com"            # your admin email
#             ]
#             send_mail(
#                 subject,
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 recipients,
#                 fail_silently=False,
#             )
#         except BadHeaderError:
#             return HttpResponse("Invalid header found.")
#         except Exception as e:
#             return HttpResponse(f"Error sending email: {e}")

#         # Handle PayPal redirection
#         if payment_method == "paypal":
#             paypal_url = settings.PAYPAL_URL
#             business_email = settings.PAYPAL_PERSONAL_EMAIL

#             params = {
#                 "cmd": "_xclick",
#                 "business": business_email,
#                 "item_name": f"Reservation by {first_name} {last_name}",
#                 "amount": total_price,
#                 "currency_code": "USD",
#                 "return": request.build_absolute_uri("/reservation-success/"),
#                 "cancel_return": request.build_absolute_uri("/payment-cancelled/"),
#                 "notify_url": request.build_absolute_uri("/paypal-ipn/"),  # optional IPN
#             }

#             redirect_url = f"{paypal_url}?{urlencode(params)}"
#             return redirect(redirect_url)

#         # Otherwise, redirect to success page
#         return redirect("reservation_success")

#     # GET request → render form
#     return render(request, "taxi/reservation.html", {
#         "paypal_client_id": settings.PAYPAL_CLIENT_ID,
#         "paypal_mode": settings.PAYPAL_MODE,
#     })


def reservation(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pickup = request.POST.get('pickup')
        dropoff = request.POST.get('dropoff')
        passengers = request.POST.get('passengers')
        vehicle_class = request.POST.get('vehicle_class')
        service_type = request.POST.get('service_type')
        total_price = request.POST.get('total_price')
        payment_method = request.POST.get('payment_method')
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('card_expiry')
        card_cvv = request.POST.get('card_cvv')
        stops = request.POST.getlist('stops')

        # Here, implement your card processing if payment_method == 'card_on_file'
        # For example, integrate Stripe/PayPal API for card charging

        # Send email
        message = f"""
Reservation Details:

Name: {first_name} {last_name}
Phone: {phone}
Email: {email}
Pickup: {pickup}
Dropoff: {dropoff}
Passengers: {passengers}
Vehicle: {vehicle_class}
Service Type: {service_type}
Extra Stops: {', '.join(stops) if stops else 'None'}
Total Price: ${total_price}
Payment Method: {payment_method}
"""

        try:
            send_mail(
                subject="New Reservation",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Reservation submitted successfully!")
        except Exception as e:
            messages.error(request, f"Reservation submitted, but email failed: {e}")

        return redirect('reservation')

    return render(request, 'taxi/reservation.html', {
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    })
    
def reservation_success(request):
    return render(request, "taxi/reservation_success.html")
    
def fleet(request):
    categories = FleetCategory.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        fleet_list = Fleet.objects.filter(category_id=selected_category).prefetch_related('images')
    else:
        fleet_list = Fleet.objects.all().prefetch_related('images')
    return render(request, 'taxi/fleet.html', {
        'fleet_list': fleet_list,
        'categories': categories,
        'selected_category': selected_category
    })