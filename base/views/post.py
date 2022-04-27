
from django.shortcuts import render, redirect
from base.models import Message, Post, Profile, User, Notification
from base.views.common import notification_function
import json


def post(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user
    profile = Profile.objects.get(user=user)
    post_images = post.img.all()
    post_campsite_latitude = post.campsite.latitude
    post_campsite_longitude = post.campsite.longitude
    post_messages = post.message_set.all().order_by(
        '-created')
    post_liked_users = post.liked.all()
    message_all = Message.objects.all()
    message_parent = Message.objects.exclude(parent=None).order_by('-created')
    plu_list = []
    user_following = profile.following.all()
    n = 0
    for plu in post_liked_users:
        if plu in user_following:
            plu_list.append(plu)
            n += 1
            if n == 3:
                break
    try:
        plu_one = plu_list[0]
    except:
        plu_one = False
    try:
        plu_two = plu_list[1]
    except:
        plu_two = False
    try:
        plu_three = plu_list[2]
    except:
        plu_three = False

    if post_liked_users.count() >= 2:
        post_liked_users_count = post_liked_users.count() - 1
    else:
        post_liked_users_count = post_liked_users.count()

    if request.method == 'POST':
        if request.POST.get('comment'):
            message = Message.objects.create(
                user=user,
                post=post,
                body=request.POST.get('comment') + ' '
            )
            Notification.objects.create(
                server=user,
                receiver=post.host,
                post=post,
                value='message')

            body = request.POST.get('comment')
            split = body.split(' ')
            for s in split:
                if '@' in s:
                    s_replace = s.replace('@', '')
                    split_user = User.objects.get(username=s_replace)
                    if user != split_user and post.host != split_user or message.user == post.host:
                        Notification.objects.create(
                            server=user,
                            receiver=split_user,
                            post=post,
                            value='mention'
                        )

        elif request.POST.get('reply'):
            message_pk = request.POST.get('parent-pk')
            parent = Message.objects.get(pk=message_pk)
            if parent.parent == None:
                Message.objects.create(
                    user=user,
                    post=post,
                    parent=parent,
                    body=request.POST.get('reply') + ' '
                )
            else:
                Message.objects.create(
                    user=user,
                    post=post,
                    parent=parent.parent,
                    body=request.POST.get('reply') + ' '
                )
            if parent.user != user:
                Notification.objects.create(
                    server=user,
                    receiver=parent.user,
                    post=post,
                    value='reply')
            body = request.POST.get('reply')
            split = body.split(' ')
            for s in split:
                if '@' in s:
                    s_replace = s.replace('@', '')
                    split_user = User.objects.get(username=s_replace)
                    if user != split_user:
                        Notification.objects.create(
                            server=user,
                            receiver=split_user,
                            post=post,
                            value='mention'
                        )
        return redirect('post', pk=post.id)

    count, last_time, notifications = notification_function(profile, user)

    context = {'post': post,
               'post_campsite_latitude': json.dumps(post_campsite_latitude),
               'post_campsite_longitude': json.dumps(post_campsite_longitude),
               'post_images': post_images,
               'post_messages': post_messages,
               'post_liked_users': post_liked_users,
               'post_liked_users_count': post_liked_users_count,
               'notifications': notifications,
               'last_time': last_time,
               'count': count,
               'plu_list': plu_list,
               'plu_one': plu_one,
               'plu_two': plu_two,
               'plu_three': plu_three,
               'user_following': user_following,
               'message_all': message_all,
               'message_parent': message_parent
               }
    return render(request, 'base/post.html', context)
