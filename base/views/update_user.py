
from django.shortcuts import render, redirect
from base.forms import UserForm
from base.models import Notification, NotificationLastTime
from django.contrib.auth.decorators import login_required
import tempfile
from PIL import Image
from datetime import datetime
import os
from django.core.files import File


@ login_required(login_url='login')
def updateUser(request):

    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        if request.POST.get('name') or request.POST.get('username') or request.POST.get('bio'):
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()

        elif request.POST.get('delete-avatar'):
            form = UserForm(request.POST, request.FILES, instance=user)
            delete_avatar = request.POST.get('delete-avatar')
            print(delete_avatar)
            try:
                os.remove('static' + str(delete_avatar))
            except:
                pass
            user.avatar = 'avatar.png'
            user.save()

        elif request.FILES:
            if os.path.exists(os.path.exists('static/images/' + str(user.avatar))) and user.avatar != 'avatar.png':
                print('delete')
                os.remove('static/images/' + str(user.avatar))

            def handle_uploaded_file(f, path):
                with open(path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            FILE_NAME = 'uploaded%s.png' % datetime.now().strftime('%Y-%m%d-%H%M')

            with tempfile.TemporaryDirectory() as tmp_directory:
                UPLOADED_PATH = '%s%s' % (tmp_directory, FILE_NAME)

                handle_uploaded_file(
                    request.FILES['avatar'], UPLOADED_PATH)
                img = Image.open(UPLOADED_PATH)
                if 'exif' in img.info:
                    img.info['exif'] = {}

                w, h = img.size
                if w < h:
                    if 1000 <= h:
                        x = h / 1000
                        w = w / x
                        h = h / x
                elif h < w:
                    if 1000 <= w:
                        x = w / 1000
                        w = w / x
                        h = h / x
                else:
                    if 1000 <= h:
                        w = 1000
                        h = 1000
                resized_img = img.resize((int(w), int(h)))

                UPLOADED_PATH_WITH_RESIZED_IMG = '%s%s' % (
                    tmp_directory, 'resized.png')
                resized_img.save(UPLOADED_PATH_WITH_RESIZED_IMG)

                f = open(UPLOADED_PATH_WITH_RESIZED_IMG, mode='rb')
                user.avatar = File(f)
                user.save()

                return redirect('update-user')

        return redirect('user-profile', username=user.username)

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
    context = {'form': form, 'notifications': notifications,
               'last_time': last_time, 'count': count, 'user': user}
    return render(request, 'base/update_user.html', context)
