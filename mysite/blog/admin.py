from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")  # side bar
    search_fields = ("title", "body")  # create search bar
    prepopulated_fields = {"slug": ("title",)}  # auto fill slug with title
    raw_id_fields = ("author",)  # lookup field for author rather than dropdown
    date_hierarchy = "publish"  # links to navigate through a date hierarchy
    ordering = ("status", "publish")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created", "updated", "active")
    list_filter = ("active", "created", "updated")
    search_fields = ("name", "email", "body")
