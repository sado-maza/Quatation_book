from django.conf import settings
from django.db import models
from django.db.models import OneToOneField


class Quotes(models.Model):
    creator_content=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author'
                                      )
    title = models.CharField(max_length=100,verbose_name="title")
    content = models.TextField(blank=True, verbose_name="quote")
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__( self ):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            Popular.objects.create(quotes=self)

    @property
    def number_of_likes(self):
        return self.likes.filter(type='like').count()

    @property
    def number_of_dislikes(self):
        return self.likes.filter(type='dislike').count()


class Category(models.Model):
    name = models.CharField(db_index=True)
    slug = models.SlugField(unique=True,db_index=True)

    def __str__( self ):
        return self.name


class Popular(models.Model):
    quotes=OneToOneField(Quotes,on_delete=models.CASCADE)
    number_of_likes = models.IntegerField(default=0)
    number_of_dislikes = models.IntegerField(default=0)




class Like(models.Model):
    LIKE_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quote = models.ForeignKey('Quotes', related_name='likes', on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=LIKE_CHOICES,default='like')

    class Meta:
        unique_together = ('user', 'quote')  # один пользователь = одна реакция
