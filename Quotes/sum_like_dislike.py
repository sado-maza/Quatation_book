from django.contrib.auth import get_user_model
from .models import Like

model = get_user_model()

def countLike(username):
    return Like.objects.filter(
        quote__creator_content=username,
        type='like'
    ).count()

def sumLike():
    for x in model.objects.all():
        x.sum_of_likes = countLike(x)
        x.save()


