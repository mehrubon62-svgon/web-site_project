from django.urls import path

from ai_consultant import views

urlpatterns = [
    path('messages/', views.chat_messages, name='ai_chat_messages'),
    path('send/', views.send_message, name='ai_chat_send'),
    path('clear/', views.clear_chat, name='ai_chat_clear'),
    path('product/messages/', views.product_chat_messages, name='product_ai_chat_messages'),
    path('product/send/', views.product_chat_send, name='product_ai_chat_send'),
    path('product/clear/', views.product_chat_clear, name='product_ai_chat_clear'),
]
