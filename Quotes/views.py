from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User

import Users
from Quatation_book import settings
from .forms import AddQuoteForm
from .sum_like_dislike import sumLike, sumDisLike
from .utils import DataMixin
from .models import Quotes


class QuotesFeed(DataMixin, ListView):
    model = Quotes
    template_name = 'quotes/quotes.html'
    title_page = 'Цитаты'
    context_object_name = "quotes"



class Authors(DataMixin, LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'quotes/authors.html'
    context_object_name = "authors"
    title_page = "Авторы"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sumLike()
        sumDisLike()
        context['default_img'] = settings.DEFAULT_USER_IMAGE
        return self.get_mixin_content(context)




class AddQuote(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddQuoteForm
    template_name = 'quotes/addquote.html'
    title_page = 'Добовление статей'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.creator_content = self.request.user

        return super().form_valid(form)
