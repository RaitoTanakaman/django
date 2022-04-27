
from django import forms
from django.forms import ModelForm, fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, PostImage, User, RATE_CHOICE
import json


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']


class PostForm(ModelForm):
    # img = forms.ImageField(
    #     widget=forms.ClearableFileInput(
    #         attrs={'multiple': True, 'accept': "image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"}),
    # )
    score = forms.ChoiceField(
        choices=RATE_CHOICE, widget=forms.Select(), required=True)

    class Meta:
        model = Post
        fields = ['title', 'local', 'place',
                  'city', 'campsite', 'score', 'category', 'description', ]


class UserForm(ModelForm):
    username = forms.CharField(max_length=50)
    name = forms.CharField(max_length=20, required=False)
    bio = forms.CharField(max_length=80, required=False)

    class Meta:
        model = User
        fields = ['username', 'name', 'bio']


# class PostImageForm(ModelForm):
#     image = forms.ImageField(
#         widget=forms.ClearableFileInput(
#             attrs={'multiple': True, 'accept': "image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"}),
#     )

#     class Meta:
#         model = PostImage
#         fields = ['image']
