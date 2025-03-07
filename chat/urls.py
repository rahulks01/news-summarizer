from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('chat-list/', views.chat_list, name='chat_list'),
    path('register/', views.register, name='register'),
    path('new-chat/', views.chat, name='new_chat'),  # Changed from chat/ to new-chat/
    path('chat/<int:conversation_id>/', views.chat, name='chat'),
    path('chat/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('logout/', views.logout_view, name='logout'),
]