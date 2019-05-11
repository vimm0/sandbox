from django.contrib import admin

# Register your models here.
from apps.blog.models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author',)
    # search_fields = ['title', 'byline', 'symbol']
    # list_filter = ['publish_on', 'created_on']
    # date_hierarchy = 'pub_date'
