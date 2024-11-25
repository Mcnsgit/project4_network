from django.contrib import admin
from .models import Post, User, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'created_at', 'total_likes')
    
    def total_likes(self, obj):
        return obj.likes.count()
    admin.site.register(Post,)
    admin.site.register(User,)
    admin.site.register(Comment,)
