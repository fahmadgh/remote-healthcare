from django.urls import path
from . import views

app_name = 'consultation'

urlpatterns = [
    path('notes/', views.consultation_notes_list, name='notes_list'),
    path('notes/<int:pk>/', views.consultation_note_detail, name='note_detail'),
    path('notes/create/<int:appointment_id>/', views.create_consultation_note, name='create_note'),
    path('chat/<int:appointment_id>/', views.chat_interface, name='chat'),
    path('video/<int:appointment_id>/', views.video_session, name='video_session'),
    path('video/<int:appointment_id>/start/', views.start_video_session, name='start_video'),
    path('video/<int:appointment_id>/end/', views.end_video_session, name='end_video'),
]
