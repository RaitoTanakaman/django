import datetime
from django.utils import timezone

from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import redirect, render
from django.db.models import Q
from base.models import Campsite, Local, Post, Place, Profile, Notification, HomeLastTime, UserInterestPost
import pandas as pd
from tqdm import tqdm
from . import auto_system
from base.scraping import scraping
from base.views.common import notification_function, Paginator_function, like_function


def home(request):

    if request.user.is_anonymous:
        return redirect('login')
    else:
        path = request.build_absolute_uri()
        user = request.user
        profile = Profile.objects.get(user=user)
        page = request.GET.get('page')

        if 'q' not in request.GET:

            user_following = profile.following.all()

            ### MakeHomeLastTime ###
            time = timezone.now()
            week = datetime.timedelta(days=3)
            home_last_time = HomeLastTime.objects.get(user=user)
            plus_week = home_last_time.time + week

            ### Recommendation system, interest_posts ###
            if time > plus_week:
                users = Profile.objects.all()[:50]
                dict = {}

                for user_i in tqdm(users):
                    dict_second = {}
                    liked_posts = Post.objects.filter(
                        liked=user_i.id).select_related('campsite')[:20]

                    for lp in liked_posts:
                        dict_second[lp.campsite.campsite] = lp.score
                        dict[user_i.id] = dict_second

                df = pd.DataFrame(dict).fillna(0).T

                def standardize(row):
                    new_row = (row - row.mean()) / (row.max() - row.min())
                    return new_row

                score_std = df.apply(standardize)
                item_similarity = cosine_similarity(score_std.T)
                item_similarity_df = pd.DataFrame(
                    item_similarity, index=df.columns, columns=df.columns)

                def get_similar_campsites(campsite_name, user_score):
                    similar_score = item_similarity_df[campsite_name]*user_score
                    similar_score = similar_score.sort_values(ascending=False)
                    return similar_score

                similar_campsites = pd.DataFrame()
                request_user_posts = Post.objects.filter(
                    liked=user).select_related('campsite')

                for rul in request_user_posts:
                    try:
                        similar_campsites = similar_campsites.append(
                            get_similar_campsites(rul.campsite.campsite, 4), ignore_index=True)
                    except:
                        pass

                sc = similar_campsites.sum().sort_values(ascending=False)
                campsites = Campsite.objects.filter(
                    campsite__in=sc.index[:10])
                interest_posts = Post.objects.filter(
                    campsite__in=campsites, score__gte=5).order_by('created')
                item_count = 10
                interest_page_obj, p_interest_posts = Paginator_function(
                    interest_posts, item_count, page)

                try:
                    exist_uip = UserInterestPost.objects.get(user=user)
                    exist_uip.delete()
                except:
                    pass

                uip = UserInterestPost.objects.create(user=user)

                for intpost in interest_posts:
                    uip.post.add(intpost)

                home_last_time.time = time
                home_last_time.save()

            else:
                try:
                    interest_posts = UserInterestPost.objects.get(
                        user=user).post.all()
                    item_count = 10
                    interest_page_obj, p_interest_posts = Paginator_function(
                        interest_posts, item_count, page)
                except:
                    high_liked_posts = Post.objects.order_by(
                        '-like_count')[:100]

                    item_count = 10
                    interest_page_obj, p_interest_posts = Paginator_function(
                        high_liked_posts, item_count, page)
                    # interest_page_obj = None
                    # p_interest_posts = None

            ###following_user_posts###
            if user_following:
                following_users_posts = Post.objects.filter(
                    host__in=user_following)
                item_count = 10
                page_obj, posts = Paginator_function(
                    following_users_posts, item_count, page)
            else:
                page_obj = None
                posts = None

            q = None

        else:
            q = request.GET.get('q')
            q_posts = Post.objects.filter(
                Q(host__name__icontains=q) |
                Q(host__username__icontains=q) |
                Q(local__local__icontains=q) |
                Q(place__name__icontains=q) |
                Q(city__city__icontains=q) |
                Q(category__category__icontains=q) |
                Q(campsite__campsite__icontains=q) |
                Q(description__icontains=q)
            )

            item_count = 16
            page_obj, posts = Paginator_function(
                q_posts, item_count, page)

            interest_page_obj = None
            p_interest_posts = None

        locals = Local.objects.all()
        for l in locals:
            places = l.place_set.all()
            for p in places:
                cities = p.city_set.all()

        count, last_time, notifications = notification_function(profile, user)

        active_profile = profile.following.all()

    context = {
        'q': q,
        'page': page,
        'page_obj': page_obj,
        'posts': posts,
        'interest_page_obj': interest_page_obj,
        'p_interest_posts': p_interest_posts,
        'places': places,
        'notifications': notifications,
        'last_time': last_time,
        'count': count,
        'active_profile': active_profile,
        'path': path,
        'locals': locals
    }
    return render(request, 'base/home.html', context)


# auto_system.auto_create_post()
# auto_system.auto_score()
