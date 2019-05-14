import nested_admin
from django.contrib import admin

from apps.comment.models import Comment, A, B, C


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


class CInline(nested_admin.NestedTabularInline):
    model = C
    extra = 0


class BInline(nested_admin.NestedStackedInline):
    model = B
    inlines = [CInline]
    extra = 0


@admin.register(A)
class AAdmin(nested_admin.NestedModelAdmin):
    inlines = [BInline]
