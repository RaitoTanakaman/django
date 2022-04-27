
from django.shortcuts import redirect
from base.models import Profile, Notification


def follow_unfollow_profile(request):

    if request.method == 'POST':
        my_profile = Profile.objects.get(user=request.user)
        if request.POST.get('profile_pk'):
            profile_pk = request.POST.get('profile_pk')
            obj = Profile.objects.get(pk=profile_pk)
            if obj.user in my_profile.following.all():
                my_profile.following.remove(obj.user)
                obj.follower.remove(my_profile.user)
            else:
                my_profile.following.add(obj.user)
                obj.follower.add(my_profile.user)
                notification = Notification.objects.get_or_create(
                    server=request.user,
                    receiver=obj.user,
                    post=None,
                    profile=obj,
                    value='follower'
                )
        elif request.POST.get('fm_profile_pk'):
            fm_profile_pk = request.POST.get('fm_profile_pk')
            fm_obj = Profile.objects.get(pk=fm_profile_pk)
            print(fm_obj)
            print(my_profile.following.all())
            if fm_obj.user in my_profile.following.all():
                my_profile.following.remove(fm_obj.user)
                fm_obj.follower.remove(my_profile.user)
            else:
                my_profile.following.add(fm_obj.user)
                fm_obj.follower.add(my_profile.user)
                notification = Notification.objects.get_or_create(
                    server=request.user,
                    receiver=fm_obj.user,
                    post=None,
                    profile=fm_obj,
                    value='follower'
                )
                print(my_profile.following.all())
        elif request.POST.get('fwm_profile_pk'):
            fwm_profile_pk = request.POST.get('fwm_profile_pk')
            fwm_obj = Profile.objects.get(pk=fwm_profile_pk)
            print(fwm_obj)
            print(my_profile.following.all())
            if fwm_obj.user in my_profile.following.all():
                my_profile.following.remove(fwm_obj.user)
                fwm_obj.follower.remove(my_profile.user)
            else:
                my_profile.following.add(fwm_obj.user)
                fwm_obj.follower.add(my_profile.user)
                notification = Notification.objects.get_or_create(
                    server=request.user,
                    receiver=fwm_obj.user,
                    post=None,
                    profile=fwm_obj,
                    value='follower'
                )
                print(my_profile.following.all())
        elif request.POST.get('nsp_pk'):
            nsp_pk = request.POST.get('nsp_pk')
            nsp_obj = Profile.objects.get(pk=nsp_pk)
            print(nsp_obj)
            print(my_profile.following.all())
            if nsp_obj.user in my_profile.following.all():
                my_profile.following.remove(nsp_obj.user)
                nsp_obj.follower.remove(my_profile.user)
            else:
                my_profile.following.add(nsp_obj.user)
                nsp_obj.follower.add(my_profile.user)
                notification = Notification.objects.get_or_create(
                    server=request.user,
                    receiver=nsp_obj.user,
                    post=None,
                    profile=nsp_obj,
                    value='follower'
                )
                print(my_profile.following.all())
        elif request.POST.get('plu_pk'):
            plu_pk = request.POST.get('plu_pk')
            plu_obj = Profile.objects.get(pk=plu_pk)
            print(plu_obj)
            print(my_profile.following.all())
            if plu_obj.user in my_profile.following.all():
                my_profile.following.remove(plu_obj.user)
                plu_obj.follower.remove(my_profile.user)
            else:
                my_profile.following.add(plu_obj.user)
                plu_obj.follower.add(my_profile.user)
                notification = Notification.objects.get_or_create(
                    server=request.user,
                    receiver=plu_obj.user,
                    post=None,
                    profile=plu_obj,
                    value='follower'
                )
                print(my_profile.following.all())

        return redirect(request.META.get('HTTP_REFERER'))
