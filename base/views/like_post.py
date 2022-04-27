
from django.shortcuts import redirect
from base.models import Post, Like, Notification


def like_post(request):

    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        print(post_id)
        post_obj = Post.objects.get(id=post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
            post_obj.like_count -= 1
            post_obj.save()
        else:
            post_obj.liked.add(user)
            post_obj.like_count += 1
            post_obj.save()
            notification = Notification.objects.get_or_create(
                server=request.user,
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

    return redirect(request.META.get('HTTP_REFERER'))
