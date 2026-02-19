from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-room/', views.create_room, name='create_room'),
    path('join-room/<str:session_id>/', views.join_room, name='join_room'),
    path('classroom/<str:session_id>/', views.classroom, name='classroom'),
    path('api/execute/', views.execute_code, name='execute_code'),
    path('api/save/', views.save_code, name='save_code'),
    path('api/session/<str:session_id>/', views.get_session_data, name='get_session_data'),
]
