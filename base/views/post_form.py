
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from base.forms import PostForm
from base.models import Post, Campsite, CampsiteScore, City, Hashtag, Place, User,  Notification, NotificationLastTime, PostImage, Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import tempfile
from PIL import Image
from datetime import datetime
import os
from django.core.files import File
from base.views.common import notification_function


path_list = []


@ login_required(login_url='login')
def createPost(request):
    form = PostForm()
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.host = user
            post.save()

            for path in path_list:
                post_image = PostImage.objects.get(filename=path)
                post.img.add(post_image)

            description = request.POST.get('description')

            CampsiteScore.objects.create(
                campsite=post.campsite,
                user=user,
                score=post.score
            )

            if '#' in description or '@' in description:
                word_list = description.split()
                for word in word_list:
                    if '#' in word:
                        tag, created = Hashtag.objects.get_or_create(tag=word)
                        post.tag.add(tag)
                    elif '@' in word:

                        reword = str(word).replace('@', '')
                        receiver = User.objects.get(username=reword)
                        notification = Notification.objects.create(
                            server=user,
                            receiver=receiver,
                            post=post,
                            value='mention'
                        )
            return redirect('home')

    count, last_time, notifications = notification_function(profile, user)

    context = {'form': form,
               'notifications': notifications,
               'last_time': last_time,
               'count': count
               }
    return render(request, 'base/post_form.html', context)


def ajaxGetPostImage(request):
    global path_list
    path_list.clear()
    for img in request.FILES.getlist('img'):

        def handle_uploaded_file(f, path):
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        FILE_NAME = 'uploaded%s.png' % datetime.now().strftime('%Y-%m%d-%H%M')

        with tempfile.TemporaryDirectory() as tmp_directory:
            UPLOADED_PATH = '%s%s' % (tmp_directory, FILE_NAME)
            handle_uploaded_file(
                img, UPLOADED_PATH)
            file = Image.open(UPLOADED_PATH)
            if 'exif' in file.info:
                file.info['exif'] = {}

            w, h = file.size
            if w < h:
                if 1441 <= h:
                    ratio = h / 1440
                    w = w / ratio
                    h = 1440
            elif h < w:
                if 1441 <= w:
                    ratio = w / 1440
                    w = 1440
                    h = h / ratio
            else:
                if 1441 <= h:
                    w = 1440
                    h = 1440

            resized_file = file.resize((int(w), int(h)))
            resized_file_p = resized_file.convert('RGBA')
            UPLOADED_PATH_WITH_RESIZED_IMG = '%s%s' % (
                tmp_directory, 'postimage.png')
            resized_file_p.save(UPLOADED_PATH_WITH_RESIZED_IMG)
            f = open(UPLOADED_PATH_WITH_RESIZED_IMG, mode='rb')

            post_image_path = os.path.basename(UPLOADED_PATH_WITH_RESIZED_IMG)
            post_image_path = post_image_path[:-5]
            path_list.append(post_image_path)
            image_instance = PostImage.objects.create(
                filename=post_image_path, image=File(f))
    d = {'path_list': path_list}
    return JsonResponse(d)


def ajaxBackPostImage(request):
    for pl in path_list:
        pl_img = PostImage.objects.get(filename=pl)
        os.remove('static/images/' + str(pl_img.image))
        pl_img.delete()

    d = {}
    return JsonResponse(d)


def ajax_get_place(request):
    pk = request.GET.get('pk')
    if not pk:
        place_list = Place.objects.all()
    else:
        place_list = Place.objects.filter(local__pk=pk)

    place_list = [{'pk': place.pk, 'place': place.name}
                  for place in place_list]

    return JsonResponse({'placeList': place_list})


def ajax_get_city(request):
    pk = request.GET.get('pk')
    if not pk:
        category_list = City.objects.all()
    else:
        category_list = City.objects.filter(place__pk=pk)
    category_list = [{'pk': city.pk, 'city': city.city}
                     for city in category_list]

    return JsonResponse({'categoryList': category_list})


def ajax_get_campsite(request):
    pk = request.GET.get('pk')
    if not pk:
        campsite_list = Campsite.objects.all()
    else:
        campsite_list = Campsite.objects.filter(city__pk=pk)

    campsite_list = [{'pk': campsite.pk, 'campsite': campsite.campsite}
                     for campsite in campsite_list]

    return JsonResponse({'campsiteList': campsite_list})


@ login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user
    form = PostForm(instance=post)
    if request.method == 'POST':
        print(path_list)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save(commit=False)
            post.img.clear()
            for path in path_list:
                post_image = PostImage.objects.get(filename=path)
                post.img.add(post_image)
            form.save()
            return redirect('home')

    try:
        count = 0
        last_time = NotificationLastTime.objects.filter(
            user=user).last()
        notifications = Notification.objects.all()
        for notification in notifications:
            if notification.receiver == user:
                if last_time.time < notification.created:
                    count += 1
    except:
        pass

    context = {'form': form, 'post': post, 'notifications': notifications,
               'last_time': last_time,
               'count': count}
    return render(request, 'base/post_form.html', context)


@ login_required(login_url='login')
def deletePost(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')

    try:
        count = 0
        last_time = NotificationLastTime.objects.filter(
            user=user).last()
        notifications = Notification.objects.all()
        for notification in notifications:
            if notification.receiver == user:
                if last_time.time < notification.created:
                    count += 1
    except:
        pass
    return render(request, 'base/delete.html', {'obj': post, 'notifications': notifications, 'last_time': last_time, 'count': count})
