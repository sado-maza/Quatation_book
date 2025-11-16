main = [
    {'title': 'Авторы', 'url_name': 'authors'},
    {'title': 'Добавить Цитату', 'url_name': 'addQuote'},


]

class DataMixin:
    title_page = None
    extra_context = None
    def get_mixin_content(self, context, **kwargs):
        context['menu'] = main
        context.update(kwargs)
        return context

    def __init__(self):
        if self.title_page:
            self.extra_context = {'title_page': self.title_page}
        else:
            self.extra_context = {'title_page': None}

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = main


