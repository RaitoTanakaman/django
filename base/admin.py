
from django.contrib import admin

# Register your models here.
from .models import CampsiteScore, Category, Hashtag, Post, Place, Message, Like, PostImage, User, Campsite, City, Local, Profile, Notification, NotificationLastTime, UserInterestPost, HomeLastTime

admin.site.register(Post)
admin.site.register(Place)
admin.site.register(Message)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(User)
admin.site.register(Campsite)
admin.site.register(City)
admin.site.register(Local)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(NotificationLastTime)
admin.site.register(Hashtag)
admin.site.register(PostImage)
admin.site.register(CampsiteScore)
admin.site.register(UserInterestPost)
admin.site.register(HomeLastTime)
