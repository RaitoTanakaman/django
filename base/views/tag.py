
from django.shortcuts import render
from base.models import Hashtag, Post


def tag_view(request, tag):
    plus_tag = '#' + tag
    hash = Hashtag.objects.get(tag=plus_tag)
    posts = Post.objects.filter(tag=hash)
    context = {'posts': posts}
    return render(request, 'base/tag.html', context)
