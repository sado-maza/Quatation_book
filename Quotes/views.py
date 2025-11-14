from django.views.generic import ListView
from .utils import DataMixin
from .models import Quotes


class QuotesFeed(DataMixin, ListView):
    model = Quotes
    template_name = 'quotes/quotes.html'
    title_page = 'Цитаты'
    context_object_name = "quotes"