from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path('', views.search_view, name='search'),
    path('results/', views.results_view, name="results"),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path("hotel/<int:hotel_id>/add_review/", views.add_review, name="add_review"),
    path("review/<int:review_id>/reply/", views.reply_to_review, name="reply_to_review"),
    path("review/<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path('trip/<int:pk>/', views.transportation_detail, name='transportation_detail'),
    path('book/room/<int:room_type_id>/', views.book_room, name='book_room'),
    path('book/trip/<int:trip_id>/', views.book_trip, name='book_trip'),
    path('toggle-darkmode/', views.toggle_darkmode, name='toggle_darkmode'),
    
    # Manager URLs
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/hotel/add/', views.add_hotel, name='add_hotel'),
    path('manager/hotel/<int:hotel_id>/edit/', views.edit_hotel, name='edit_hotel'),
    path('manager/hotel/<int:hotel_id>/delete/', views.delete_hotel, name='delete_hotel'),
    path('manager/hotel/<int:hotel_id>/room/add/', views.add_room, name='add_room'),
    path('manager/transportation/add/', views.add_transportation, name='add_transportation'),
    path('manager/transportation/<int:trip_id>/edit/', views.edit_transportation, name='edit_transportation'),
    path('manager/transportation/<int:trip_id>/delete/', views.delete_transportation, name='delete_transportation'),
]