from django.contrib import admin
from .models import Quotes, Category, Popular



class QuotesAdmin(admin.ModelAdmin):
    list_display = ('id','creator_content', 'title', 'time_created')
    list_display_links = ('id', 'title')
admin.site.register(Quotes,QuotesAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','slug')
    list_display_links = ('id', 'name')
admin.site.register(Category, CategoryAdmin)

class PopularAdmin(admin.ModelAdmin):
    list_display = ('id', 'quotes','number_of_likes','number_of_dislikes',)
    list_display_links = ('id', 'quotes')

admin.site.register(Popular, PopularAdmin)