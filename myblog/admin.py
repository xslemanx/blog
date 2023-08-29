from django.contrib import admin

from myblog.models import Post,Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'post_author', 'post_publish_date', 'post_status')
    list_filter = ('post_status', 'post_create_date', 'post_publish_date', 'post_author')
    search_fields = ('post_title', 'post_body')
    prepopulated_fields = {'post_slug': ('post_title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')