"""
URL configuration for bms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import home, movie_detail,show_detail,checkout,confirm_booking,download_ticket,my_bookings,register,profile
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('movie/<int:id>/', movie_detail, name='movie_detail'),
    path('show/<int:id>/', show_detail, name='show_detail'),
    path('checkout/<int:id>/', checkout, name='checkout'),
    path('confirm-booking/<int:id>/', confirm_booking, name='confirm_booking'),
    path('ticket/<int:booking_id>/', download_ticket, name='download_ticket'),
    path('profile/', profile, name='profile'),

    
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)