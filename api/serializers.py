from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Booking


# ==========================
# EVENT SERIALIZER
# ==========================
class EventSerializer(serializers.ModelSerializer):
    available_slots = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "location",
            "date",
            "capacity",
            "available_slots",
            "created_by",
        ]
        read_only_fields = ["id", "available_slots", "created_by"]

    def get_available_slots(self, obj):
        return obj.available_slots()

    def validate(self, data):
        if Event.objects.filter(
            title=data.get("title"),
            date=data.get("date"),
            location=data.get("location"),
        ).exists():
            raise serializers.ValidationError(
                "An event with the same title, date, and location already exists."
            )
        return data


# ==========================
# BOOKING SERIALIZER (USER)
# ==========================
class BookingSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_date = serializers.DateField(source="event.date", read_only=True)
    location = serializers.CharField(source="event.location", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "event",
            "event_title",
            "event_date",
            "location",
            "booked_at",
        ]
        read_only_fields = ["id", "booked_at"]


# ==========================
# REGISTER SERIALIZER
# ==========================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


# ==========================
# ADMIN BOOKING SERIALIZER
# ==========================
class AdminBookingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_date = serializers.DateField(source="event.date", read_only=True)
    location = serializers.CharField(source="event.location", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "username",
            "email",
            "event_title",
            "event_date",
            "location",
            "booked_at",
        ]
