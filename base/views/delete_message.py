from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from base.models import Message, Notification, NotificationLastTime
from django.contrib.auth.decorators import login_required


@ login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('post', message.post)

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
    return render(request, 'base/delete.html', {'obj': message, 'notifications': notifications, 'last_time': last_time, 'count': count})
