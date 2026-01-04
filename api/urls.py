from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)
from .views import (
    register,
    event_list,
    create_event,
    book_event,
    my_bookings,
    me,
    delete_event,
    update_event,
    admin_dashboard,
    admin_all_bookings,
    
)

urlpatterns = [
    # AUTH
    path("register/", register),
    path("login/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),

    # BOOKINGS (⚠️ PUT THIS FIRST)
    path("my-bookings/", my_bookings),

    # EVENTS
    path("events/", event_list),
    path("events/create/", create_event),
    path("events/<int:event_id>/book/", book_event),
    path("me/", me),
    path("events/<int:event_id>/delete/", delete_event),
    path("events/<int:event_id>/update/", update_event),
    path("admin/dashboard/", admin_dashboard),
    path("admin/bookings/", admin_all_bookings),




    

]
