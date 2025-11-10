from django.shortcuts import render,get_object_or_404
from .models import Movie, City,Show, Seat,Booking
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Exists, OuterRef
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import qrcode
from io import BytesIO
import base64
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def home(request):
    selected_city = request.GET.get("city")
    selected_genre = request.GET.get("genre")
    selected_language = request.GET.get("language")
    search = request.GET.get("search", "")

    cities = City.objects.all()

    movies = Movie.objects.all()

    # City Filter
    if selected_city:
        movies = movies.filter(show__screen__theatre__city__id=selected_city).distinct()

    # Search Filter
    if search:
        movies = movies.filter(title__icontains=search)

    # Genre Filter
    if selected_genre:
        movies = movies.filter(genre__icontains=selected_genre)

    # Language Filter
    if selected_language:
        movies = movies.filter(language__icontains=selected_language)

    return render(request, 'home.html', {
        'cities': cities,
        'movies': movies,
        'selected_city': selected_city,
        'selected_genre': selected_genre,
        'selected_language': selected_language,
        'search': search
    })


@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})


def movie_detail(request, id):
    movie = Movie.objects.get(id=id)
    shows = Show.objects.filter(movie=movie)
    return render(request, 'movie_detail.html', {'movie': movie, 'shows': shows})

def show_detail(request, id):
    show = get_object_or_404(Show, id=id)
    seats = Seat.objects.filter(screen=show.screen).order_by('row', 'col')

    # Fetch which seats are booked for this show
    booked_seats = set(
        show.booking_set.values_list('seats__id', flat=True)
    )
    col_range = range(1, show.screen.cols + 1)

    return render(request, 'show_detail.html', {
        'show': show,
        'seats': seats,
        'booked_seats': booked_seats,
        'col_range':col_range
    })

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, "register.html", {"form": form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(name=request.user.username)
    return render(request, "my_bookings.html", {"bookings": bookings})


def checkout(request, id):
    show = Show.objects.get(id=id)
    selected_seat_ids = [s for s in request.POST.get("selected_seats", "").split(",") if s]

    seats = Seat.objects.filter(id__in=selected_seat_ids)

    amount = len(seats) * 150  # ₹150 per seat, change if needed

    # YOUR UPI ID HERE ↓↓↓
    upi_id = "prakiom@ybl"

    # Generate UPI payment link
    payment_link = f"upi://pay?pa={upi_id}&pn=TicketPayment&am={amount}&cu=INR"

    # Generate QR Image
    qr = qrcode.make(payment_link)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_data = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "checkout.html", {
        "show": show,
        "seats": seats,
        "amount": amount,
        "qr_data": qr_data,
        "payment_link": payment_link,
    })

def confirm_booking(request, id):
    show = Show.objects.get(id=id)

    if request.method == "POST":
        seat_ids = request.POST.get('seat_ids', '').strip(',').split(',')
        seats = Seat.objects.filter(id__in=seat_ids)

        # If user logged in → use username, else take manual input
        name = request.user.username if request.user.is_authenticated else request.POST.get('name')

        booking = Booking.objects.create(show=show, name=name)
        booking.seats.set(seats)

        return render(request, 'booking_success.html', {'booking': booking})

    return redirect('checkout', id=id)


def download_ticket(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ booking.id }.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 800, "🎟 Movie Ticket Confirmation")

    p.setFont("Helvetica", 14)
    p.drawString(100, 760, f"Movie: {booking.show.movie.title}")
    p.drawString(100, 740, f"Theatre: {booking.show.screen.theatre.name}")
    p.drawString(100, 720, f"Screen: {booking.show.screen.name}")

    seat_list = ", ".join([f"{seat.row}-{seat.col}" for seat in booking.seats.all()])
    p.drawString(100, 700, f"Seats: {seat_list}")

    p.drawString(100, 680, f"Booked By: {booking.name}")
    p.drawString(100, 660, f"Time: {booking.created_at.strftime('%Y-%m-%d %H:%M')}")

    p.showPage()
    p.save()
    return response


