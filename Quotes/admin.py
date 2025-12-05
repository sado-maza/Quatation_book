from django.contrib import admin
from .models import Quotes, Category



class QuotesAdmin(admin.ModelAdmin):
    list_display = ('id','creator_content','title','content', 'category','time_created')
    list_display_links = ('id', 'title','category')
admin.site.register(Quotes,QuotesAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','slug')
    list_display_links = ('id', 'name')
admin.site.register(Category, CategoryAdmin)

