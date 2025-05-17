from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_or_signup),
    path('logout/', views.logout_view),
    path('check_login/', views.check_login),
    path('follow/', views.follow_tag),
    path('unfollow/', views.unfollow_tag),
    path('get_profile/', views.get_profile),
    path('tags/', views.get_tags),
    path('feed/random/', views.random_feed),
    path('feed/custom/', views.custom_feed),
]