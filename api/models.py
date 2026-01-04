from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    capacity = models.PositiveIntegerField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events",
    )

    class Meta:
        unique_together = ("title", "date", "location")
        ordering = ["date"]

    def available_slots(self):
        return self.capacity - self.bookings.count()

    def __str__(self):
        return f"{self.title} ({self.date})"


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
        ordering = ["-booked_at"]

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"
