from django.urls import path
from . import views
from . import account

app_name = 'myapp'
urlpatterns = [
    path('index', views.index, name='index'),
    path('login', account.login, name='login'),
    path('profile', account.profile, name='profile'),
    path('edit_profile', account.edit_profile, name='edit_profile'),
    path('update_profile', account.update_profile, name='update_profile'),
    path('register', account.register, name='register'),
    path('check_register', account.check_register, name='check_register'),
    path('get_my_weibo', views.get_my_weibo, name="get_my_weibo"),
    path('get_my_follow_weibo', views.get_my_follow_weibo, name="get_my_follow_weibo"),
    path('get_my_follow_user', views.get_my_follow_user, name="get_my_follow_user"),
    path('get_follow_user/<str:uid>', views.get_follow_user, name="get_follow_user"),	
    path('delete_follow_user/<str:uid>', views.delete_follow_user, name="delete_follow_user"),
    path('get_user_home/<str:uid>add_follow_user', views.add_follow_user, name="add_follow_user"),
    path('get_my_fan', views.get_my_fan, name="get_my_fan"),
    path('get_fan/<str:uid>', views.get_fan, name="get_fan"),	
    path('send_weibo', views.send_weibo, name="send_weibo"),
    path('weibo.html', views.get_home, name="get_home"),
    path('vis.html', views.get_vis, name="get_vis"),
    path('my.html', views.get_my_home, name="get_my_home"),
    path('get_user_home/<str:uid>', views.get_user_home, name="get_user_home"),
    path('user<str:user_id>.html', views.get_user_homepage, name="get_user_homepage"),
    path('delete_weibo', views.delete_weibo, name="delete_weibo")
]
