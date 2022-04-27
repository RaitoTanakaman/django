from django.urls import path
from .views import home, login_register, post, user_profile, follow_unfollow_profile, post_form, delete_message, favorite_post, update_user, like_post, notifications, tag
from django.views.decorators.cache import cache_page

urlpatterns = [
    #     path('', cache_page(60 * 1)(views.home), name='home'),
    path('', home.home, name='home'),
    #     path('post-load-chunk', home.home.post_load_chunk, name='post_load_chunk'),
    path('post/<str:pk>', post.post, name='post'),
    path('profile/<str:username>', user_profile.userProfile, name='user-profile'),
    path('switch_follow/', follow_unfollow_profile.follow_unfollow_profile,
         name='follow-unfollow-view'),
    path("create-post/", post_form.createPost, name="create-post"),
    path("update-post/<str:pk>", post_form.updatePost, name="update-post"),
    path("delete-post/<str:pk>", post_form.deletePost, name="delete-post"),
    path("login/", login_register.loginPage, name='login'),
    path("logout/", login_register.logoutUser, name='logout'),
    path("register/", login_register.registerPage, name='register'),
    path("delete-message/<str:pk>",
         delete_message.deleteMessage, name='delete-message'),
    path("favorite-post/", favorite_post.favoritePost, name='favorite-post'),
    path("update-user", update_user.updateUser, name='update-user'),
    path('like/', like_post.like_post, name='like-post'),
    path('api/city/get/', post_form.ajax_get_city, name='ajax_get_city'),
    path('api/place/get/', post_form.ajax_get_place, name='ajax_get_place'),
    path('api/campsite/get/', post_form.ajax_get_campsite,
         name='ajax_get_campsite'),
    path('notification/', notifications.notification_view,
         name='notification-view'),
    path('activate-user/<uidb64>/<token>',
         login_register.activate_user, name='activate'),
    path('tags/<str:tag>', tag.tag_view, name='tag-view'),
    path('api/post-img/get', post_form.ajaxGetPostImage,
         name='ajax_get_post_image'),
    path('api/post-img/back', post_form.ajaxBackPostImage,
         name='ajax_back_post_image'),


]
