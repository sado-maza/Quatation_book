from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from Quatation_book import settings
from .forms import AddQuoteForm
from .sum_like_dislike import sumLike
from .utils import DataMixin, QuotesContextService
from .models import Quotes, Like, Category


class QuotesFeed(DataMixin, ListView):
    model = Quotes
    template_name = 'quotes/quotes.html'
    title_page = 'Цитаты'
    context_object_name = "quotes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = QuotesContextService(user=self.request.user)
        # передаём extra_context через DataMixin
        return self.get_mixin_content(
            service.get_context(self.object_list, extra_context={
                'title_page': self.title_page,

            })
        )

    def get_queryset(self):
        qs = super().get_queryset()

        sort = self.request.GET.get('sort')

        if sort == 'new':
            qs = qs.order_by('-time_created')  # новые сверху
        elif sort == 'old':
            qs = qs.order_by('time_created')  # старые сверху
        elif sort == 'likes':
            from django.db.models import Q
            qs = qs.annotate(
                like_count=Count('likes', filter=Q(likes__type='like'))
            ).order_by('-like_count')
        return qs

class Authors(DataMixin, LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'quotes/authors.html'
    context_object_name = "authors"
    title_page = "Авторы"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sumLike()
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


@login_required
def toggle_vote_ajax(request, quote_id, action):
    if request.method == "POST":
        quote = get_object_or_404(Quotes, id=quote_id)

        try:
            like = Like.objects.get(user=request.user, quote=quote)
            if like.type == action:
                # снимаем голос
                like.delete()
                user_state = "none"
            else:
                like.type = action
                like.save()
                user_state = action
        except Like.DoesNotExist:
            Like.objects.create(user=request.user, quote=quote, type=action)
            user_state = action

        data = {
            "likes": quote.number_of_likes,
            "dislikes": quote.number_of_dislikes,
            "state": user_state
        }
        return JsonResponse(data)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def categors(request, cat):
    mixin = DataMixin()
    slug = Category.objects.get(slug=cat).pk
    qs = Quotes.objects.filter(category_id=slug)
    sort = request.GET.get('sort')
    if sort == 'new':
        qs = qs.order_by('-time_created')
    elif sort == 'old':
        qs = qs.order_by('time_created')
    elif sort == 'likes':
        qs = qs.annotate(like_count=Count('likes', filter=Q(likes__type='like'))).order_by('-like_count')
    service = QuotesContextService(user=request.user)
    context = service.get_context(qs, extra_context={'title_page': f'Категория {cat}'})
    context = mixin.get_mixin_content(context)
    return render(request, 'quotes/quotes.html', context)
