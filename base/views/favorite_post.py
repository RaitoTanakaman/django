
from django.shortcuts import render

from base.models import Place, Post, Notification, NotificationLastTime
from base.views.home import Paginator_function


def favoritePost(request):
    user = request.user
    page = request.GET.get('page')
    liked_posts = Post.objects.filter(liked=user)
    count = 20

    page_obj, posts = Paginator_function(liked_posts, count, page)
    places = Place.objects.all()

    try:
        count = 0
        last_time = NotificationLastTime.objects.filter(
            user=request.user).last()
        notifications = Notification.objects.all()
        for notification in notifications:
            if notification.receiver == request.user:
                if last_time.time < notification.created:
                    count += 1
    except:
        pass

    context = {'page_obj': page_obj, 'posts': posts, 'places': places,
               'notifications': notifications, 'last_time': last_time, 'count': count}
    return render(request, 'base/favorite_post.html', context)
