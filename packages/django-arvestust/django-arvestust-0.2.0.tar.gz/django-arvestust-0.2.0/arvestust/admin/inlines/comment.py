# arvestust:admin:inlines
from django.contrib.contenttypes import admin
from ...models import Comment


class CommentInline(admin.GenericTabularInline):
    model = Comment
    extra = 0
