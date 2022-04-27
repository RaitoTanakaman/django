
from pickle import NONE

from django.shortcuts import render, redirect
from django.contrib import messages


from base.forms import MyUserCreationForm
from base.models import HomeLastTime, User, NotificationLastTime, Profile
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from base.utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings


def send_action_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account.'
    email_body = render_to_string('base/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject,
                         body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    email.send()


# **********LOGIN**********


def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'ユーザーが存在しません。')

        user = authenticate(request, username=username, password=password)

        if not user.is_email_verified:
            messages.add_message(
                request, messages.ERROR, 'Email is not verified, Please check your email inbox')

            send_action_email(user, request)

            return render(request, 'base/login_register.html', {'data': request.POST})

        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'ユーザーかパスワードが存在しません。')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


# **********LOGOUT**********
def logoutUser(request):
    logout(request)
    return redirect('login')


# **********REGISTER**********
def registerPage(request):
    form = MyUserCreationForm()
    time = timezone.now()

    if request.method == 'POST':

        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            HomeLastTime.objects.create(user=user, time=time)
            nt = NotificationLastTime.objects.create(user=user, time=time)
            p = Profile.objects.get(user=user)
            p.last_time = nt
            p.save()
            send_action_email(user, request)

            if 'favorite-post/register' in request.path:
                login(request, user)
                return redirect('favorite-post')
            else:
                return render(request, 'base/check-email.html')
        else:
            messages.error(request, '登録中にエラーが発生しました。')

    return render(request, 'base/login_register.html', {'form': form})


def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = NONE

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, You are login.')
        return redirect('login')
    return render(request, 'base/activate-failed.html', {'user': user})
