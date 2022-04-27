from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from base.models import Post, Like, Notification


### Notification_function ###
def notification_function(request_profile, request_user):
    try:
        count = 0
        last_time = request_profile.last_time
        notifications = Notification.objects.filter(receiver=request_user)

        for notification in notifications:
            if last_time.time < notification.created:
                if notification.server != notification.receiver:
                    count += 1
            if notification.server == notification.receiver:
                notification.delete()
    except:
        pass

    return count, last_time, notifications


### Paginator ###
def Paginator_function(post, count, page):
    paginator = Paginator(post, count)

    try:
        page_obj = paginator.page(page)
        posts = page_obj.object_list
    except PageNotAnInteger:
        page_obj = paginator.page(1)
        posts = page_obj.object_list
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        posts = page_obj.object_list

    return page_obj, posts


### Like_function ###
def like_function(user, post_id):
    post_obj = Post.objects.get(id=post_id)
    if user in post_obj.liked.all():
        post_obj.liked.remove(user)
        post_obj.like_count = - 1
        post_obj.save()
    else:
        post_obj.liked.add(user)
        post_obj.like_count = + 1
        post_obj.save()
        notification = Notification.objects.get_or_create(
            server=user,
            receiver=post_obj.host,
            post=post_obj,
            value='like'
        )

        like, created = Like.objects.get_or_create(
            user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
