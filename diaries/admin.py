from django.contrib import admin

from .models import User, Post, Subscription


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Subscription)

