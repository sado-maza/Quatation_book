from Quotes.models import Category

main = [
    {'title': 'Авторы', 'url_name': 'authors'},
    {'title': 'Добавить Цитату', 'url_name': 'addQuote'},]

class DataMixin:
    title_page = None
    extra_context = None

    def get_mixin_content(self, context, **kwargs):
        context.update(kwargs)
        context.setdefault('menu', main)
        return context


class QuotesContextService:
    """Готовит контекст для страницы с цитатами, учитывая лайки пользователя"""

    def __init__(self, user=None):
        self.user = user

    def add_user_votes(self, quotes_queryset):
        """Добавляет поле user_vote для каждого объекта Quotes"""
        quotes = list(quotes_queryset)  # обязательно превращаем в список, чтобы не было повторных запросов
        for quote in quotes:
            if self.user and self.user.is_authenticated:
                try:
                    like = quote.likes.get(user=self.user)
                    quote.user_vote = like.type
                except quote.likes.model.DoesNotExist:
                    quote.user_vote = 'none'
            else:
                quote.user_vote = 'none'
        return quotes

    def get_context(self, quotes_queryset, extra_context=None):
        """Возвращает готовый контекст для шаблона"""
        context = extra_context.copy() if extra_context else {}
        context['quotes'] = self.add_user_votes(quotes_queryset)
        context['cat'] = Category.objects.all()
        return context




