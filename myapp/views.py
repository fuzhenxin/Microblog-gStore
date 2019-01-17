from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from .weibo import Weibo
from .userrelation import User
from database.gstore import GstoreConnector

gstore = GstoreConnector("127.0.0.1", 2567, "root", "123456")
weibo = Weibo(gstore)
user = User(gstore)

def get_my_weibo(request):
    return weibo.get_my_weibo(request)

def get_vis(request):
    return weibo.get_ana(request)

def get_my_follow_weibo(request):
    return weibo.get_my_follow_weibo(request)

def get_my_follow_user(request):
    return user.get_my_follow_user(request)
	
def get_follow_user(request, uid):
    return user.get_follow_user(request, uid)
	
def delete_follow_user(request, uid):
    return user.delete_follow_user(request, uid)
	
def add_follow_user(request, uid):
    return user.add_follow_user(request, uid)
	
def get_my_fan(request):
    return user.get_my_fan(request)
	
def get_fan(request, uid):
    return user.get_fan(request, uid)

def send_weibo(request):
    return weibo.send_weibo(request)

def delete_weibo(request):
    return weibo.delete_weibo(request)

def get_home(request):
    context_dict = dict()
    context_dict["myhomepage"] = "Y"
    return render(request, 'myapp/weibo.html', context_dict)
    #return render_to_response('myapp/weibo.html', RequestContext(request, {}))


def get_my_home(request):
    return user.get_my_home(request)

def get_user_homepage(request, user_id):
    print("user_id", user_id)
    context_dict = dict()
    context_dict["user_id"] = user_id
    return render(request, 'myapp/weibo.html', context_dict)

def get_user_home(request, uid):
    return user.get_user_home(request, uid)

def index(request):
    response = render(request, 'myapp/index.html')
    #response.set_cookie("user", "1749705962")
    return response


def detail(request, name):
    #if "user" in request.COOKIES:
    #    print("Gookie got", request.COOKIES.get("user"))
    _name = request.session['uid']
    print(_name, request.session)
    context = {'names': _name}
    return render(request, 'myapp/detail.html', context)
	

