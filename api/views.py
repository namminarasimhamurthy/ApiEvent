from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer, RegisterSerializer


# -----------------------------
# EVENTS
# -----------------------------

@api_view(["GET"])
def event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    serializer = EventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return Response({"message": "Event deleted successfully"})


# -----------------------------
# BOOKINGS
# -----------------------------

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # ❌ Already booked
    if event.bookings.filter(user=request.user).exists():
        return Response(
            {"error": "You already booked this event"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ❌ Capacity full
    if event.bookings.count() >= event.capacity:
        return Response(
            {"error": "Event is fully booked"},
            status=status.HTTP_400_BAD_REQUEST
        )

    Booking.objects.create(
        user=request.user,
        event=event
    )

    return Response(
        {
            "message": "Event booked successfully",
            "remaining_slots": event.available_slots(),
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


# -----------------------------
# AUTH
# -----------------------------

@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user:
        return Response({"message": "Login successful"})
    return Response(
        {"error": "Invalid username or password"},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        "username": request.user.username,
        "is_admin": request.user.is_staff
    })


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_dashboard(request):
    return Response({
        "total_users": User.objects.count(),
        "total_events": Event.objects.count(),
        "total_bookings": Booking.objects.count(),
    })


from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import AdminBookingSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_all_bookings(request):
    bookings = Booking.objects.select_related("user", "event").all()
    serializer = AdminBookingSerializer(bookings, many=True)
    return Response(serializer.data)
