
from django.shortcuts import render
from base.models import Profile, User, Notification, NotificationLastTime
from base.views.common import notification_function, Paginator_function


def userProfile(request, username):
    user_username = User.objects.prefetch_related('host').select_related(
        'profile').get(username=username)
    page = request.GET.get('page')
    user = request.user
    profile = Profile.objects.get(user=user)
    profile_user = user_username.profile
    profile_posts = user_username.host.all()
    # try:

    #     if user == user_username:
    #         profile = Profile.objects.get_or_create(user=user)
    # except:
    #     pass
    if user.username == request.path:
        main_profile = profile
    else:
        main_profile = profile_user

    user_pk = user_username.pk
    active_profile = profile.following.all()

    count, last_time, notifications = notification_function(profile, user)

    p_count = 16
    page_obj, posts = Paginator_function(profile_posts, p_count, page)

    context = {'user': user_username, 'posts': posts,
               'main_profile': main_profile,
               'user_pk': user_pk,
               'profile_user': profile_user,
               'active_profile': active_profile,
               'notifications': notifications,
               'last_time': last_time,
               'count': count,
               'page_obj': page_obj
               }
    return render(request, 'base/profile.html', context)
