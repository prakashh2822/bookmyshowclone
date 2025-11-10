from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_mins = models.PositiveIntegerField()

    genre = models.CharField(max_length=100, blank=True)       # NEW
    language = models.CharField(max_length=50, blank=True)  # NEW
    
    rating = models.FloatField(default=0, blank=True)  # ⭐ NEW
    trailer_url = models.URLField(blank=True)

    poster_url = models.URLField(blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)

    def __str__(self):
        return self.title




class Theatre(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class Screen(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField(default=10)
    cols = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.theatre.name} ({self.name})"

class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()
    
    def row_label(self):
        return chr(64 + self.row)

    def __str__(self):
        return f"R{self.row}C{self.col} - {self.screen}"



class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} @ {self.screen} on {self.start_time}"
    
class Booking(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    name = models.CharField(max_length=100)  # who booked
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.show.movie.title} at {self.show.screen.theatre.name}"


