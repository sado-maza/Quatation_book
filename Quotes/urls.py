from django.urls import path

from Quotes import views

urlpatterns = [
    path('',views.QuotesFeed.as_view(), name='feed'),
]