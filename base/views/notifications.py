
from django.shortcuts import redirect
from base.models import NotificationLastTime
from django.utils import timezone


def notification_view(request):

    if request.method == 'POST':
        time = timezone.now()

        old_time = NotificationLastTime.objects.get(user=request.user)
        old_time.time = time
        old_time.save()
    return redirect('home')
