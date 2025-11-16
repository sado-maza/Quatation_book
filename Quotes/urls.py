from django.urls import path

from Quotes import views

urlpatterns = [
    path('',views.QuotesFeed.as_view(), name='feed'),
    path('authors', views.Authors.as_view(), name='authors'),
    path('AddQuote', views.AddQuote.as_view(), name='addQuote'),
]