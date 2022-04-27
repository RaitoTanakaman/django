
from pyexpat import model
from statistics import mode
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import hashlib
import uuid


def user_profile_avator_upload_to(instance, filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s%s' % (instance.id, filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(
        pre_hash_name.encode()).hexdigest(), extension)
    saved_path = 'images/'
    return '%s%s' % (saved_path, hs_filename)


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=True)
    name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(null=True)
    is_email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(
        null=True, upload_to=user_profile_avator_upload_to, default="avatar.png")
    bio = models.CharField(max_length=80, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class NotificationLastTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(auto_now=True)


class HomeLastTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(auto_now=True)


class Category(models.Model):
    category = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.category


class Local(models.Model):
    local = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.local


class Place(models.Model):
    name = models.CharField(max_length=200)
    local = models.ForeignKey(Local, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    place = models.ForeignKey(Place, null=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.city


class Campsite(models.Model):
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    campsite = models.CharField(
        max_length=50, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.campsite


RATE_CHOICE = [
    (1, '1 - 良くない'),
    (2, '2 - あまり良くない'),
    (3, '3 - 普通'),
    (4, '4 - 良い'),
    (5, '5 - とても良い'),

]


class CampsiteScore(models.Model):
    campsite = models.ForeignKey(Campsite, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=RATE_CHOICE, null=True)


class Hashtag(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


def post_image_upload_to(instance, filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s%s' % (instance.id, filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(
        pre_hash_name.encode()).hexdigest(), extension)
    saved_path = 'post_images/'
    return '%s%s' % (saved_path, hs_filename)


class PostImage(models.Model):
    filename = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, upload_to=post_image_upload_to)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    img = models.ManyToManyField(
        PostImage, blank=True)
    host = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name='host', null=True)
    title = models.CharField(max_length=22, null=True)
    local = models.ForeignKey(Local, null=True, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    campsite = models.ForeignKey(
        Campsite, null=True, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=RATE_CHOICE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    liked = models.ManyToManyField(
        User, blank=True, related_name='liked')
    like_count = models.IntegerField(default=0)
    tag = models.ManyToManyField(Hashtag, blank=True, related_name='hashtag')
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.title)

    @property
    def num_likes(self):
        return self.liked.all().count()

    def __str__(self):
        return str(self.pk)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, null=True, blank=True, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='like', max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)


class UserInterestPost(models.Model):
    post = models.ManyToManyField(Post)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        User, related_name='following', blank=True)
    follower = models.ManyToManyField(
        User, related_name='follower', blank=True)
    last_time = models.ForeignKey(
        NotificationLastTime, on_delete=models.CASCADE, related_name='notification_last_time', null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def profiles_posts(self):
        return self.post_set.all()

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ('-created',)

    @property
    def num_following(self):
        return self.following.all().count()

    @property
    def num_follower(self):
        return self.follower.all().count()


NOTIFICATION_CHOICES = (
    ('message', 'message'),
    ('like', 'like'),
    ('follower', 'follower'),
    ('reply', 'reply'),
    ('mention', 'mention')
)


class Notification(models.Model):
    server = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='server')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='receiver')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, related_name='post')
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, related_name='profile')
    value = models.CharField(choices=NOTIFICATION_CHOICES, max_length=10)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
