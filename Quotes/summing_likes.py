from django.contrib.auth import get_user_model

from .models import Quotes,Popular
from django.db.models import Sum

def sumLike(username):
    quotes = Quotes.objects.filter(creator_content=username)
    total_like = Popular.objects.filter(quotes__in=quotes).aggregate(Sum('number_of_likes'))['number_of_likes__sum']
    return total_like


# print(sumLike(get_user_model().objects.get(pk=1)))
