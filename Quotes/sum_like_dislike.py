from django.contrib.auth import get_user_model

from .models import Quotes,Popular
from django.db.models import Sum

model = get_user_model()

def countLike(username):
    quotes = Quotes.objects.filter(creator_content=username)
    total_like = Popular.objects.filter(quotes__in=quotes).aggregate(total=Sum('number_of_likes'))['total'] or 0
    return total_like

def sumLike():
    for x in model.objects.all():
        x.sum_of_likes = countLike(x)
        x.save()


def countDisLike(username):
    quotes = Quotes.objects.filter(creator_content=username)
    total_like = Popular.objects.filter(quotes__in=quotes).aggregate(total=Sum('number_of_dislikes'))['total'] or 0
    return total_like

def sumDisLike():
    for x in model.objects.all():
        x.sum_of_dislikes = countLike(x)
        x.save()
