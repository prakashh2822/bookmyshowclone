from django.contrib import admin
from .models import City, Movie, Theatre, Screen, Show, Seat, Booking

admin.site.register(Booking)
admin.site.register(City)
admin.site.register(Theatre)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'rating', 'duration_mins')
    fields = ('title', 'description', 'genre', 'language', 'rating', 'duration_mins', 'trailer_url', 'poster_url', 'poster')



admin.site.register(Movie, MovieAdmin)

class ScreenAdmin(admin.ModelAdmin):
    list_display = ('name', 'theatre', 'rows', 'cols')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # If new screen -> create seats
        if not change:
            seats = [
                Seat(screen=obj, row=r, col=c)
                for r in range(1, obj.rows + 1)
                for c in range(1, obj.cols + 1)
            ]
            Seat.objects.bulk_create(seats)

admin.site.register(Screen, ScreenAdmin)
admin.site.register(Show)
admin.site.register(Seat)
