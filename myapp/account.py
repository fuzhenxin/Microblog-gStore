from django.shortcuts import render, redirect
from database.gstore import GstoreConnector
from django.http import HttpResponseNotFound
from django.urls import reverse
from hashlib import sha256
from datetime import datetime
from .userrelation import User as SX_User

gstore = GstoreConnector("*", 2567, "root", "123456")
prefix = "prefix wb: <file:///D:/d2rq-0.8.1/vocab/> "


class User:
    def __init__(self, uid, name="", screen_name="", location="", gender="", created="", passwd=""):
        self.uid = uid
        self.name = name
        self.screen_name = screen_name
        self.location = location
        self.gender = gender
        self.created_at = created
        self.password = passwd
        self.predicates = ['user_name', 'user_screen_name', 'user_location',
                           'user_gender', 'user_created_at']

    def load_from_db(self):
        template = prefix + ' select ?m where {{ ?x wb:{} ?m . ?x wb:user_uid "{}" .}}'
        queries = [template.format(pred, self.uid) for pred in self.predicates]

        results = [gstore.query('weibo', query)['results']['bindings'] for query in queries]
        print('load from db success', results[1])
        results = [r[0]['m']['value'] for r in results]
        self.name = results[0]
        self.screen_name = results[1]
        self.location = results[2]
        self.gender = results[3]
        self.created_at = results[4]
        query = template.format('user_password', self.uid)
        res = gstore.query('weibo', query)['results']['bindings']
        if len(res) > 0:
            self.password = res[0]['m']['value']
        else:
            self.password = self.uid
            user_entity = '<file:///D:/d2rq-0.8.1/weibo.nt#user/{}>'.format(self.uid)
            query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
                prefix, user_entity, 'user_password', self.password)
            gstore.query('weibo', query)
            print('first insert password when load user.')

    def save_to_db(self):
        user_entity = '<file:///D:/d2rq-0.8.1/weibo.nt#user/{}>'.format(self.uid)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
                prefix, user_entity, 'user_uid', self.uid)
        print(query)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
                prefix, user_entity, 'user_name', self.name)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
            prefix, user_entity, 'user_password', self.password)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
            prefix, user_entity, 'user_screen_name', self.screen_name)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
                prefix, user_entity, 'user_gender', self.gender)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
            prefix, user_entity, 'user_location', self.location)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .}}'.format(
            prefix, user_entity, 'user_created_at', self.created_at)
        gstore.query('weibo', query)


def login(request):
    try:
        name = request.POST['username']
        password = str(request.POST['password'])
    except KeyError:
        return HttpResponseNotFound("No username or password send")
    else:
        sparql = '''{} select ?m where {{ ?x wb:user_name "{}". 
                    ?x wb:user_uid ?m .}}'''.format(prefix, name)
        result = gstore.query('weibo', sparql)['results']['bindings']
        print('get uid', result)
        if not result:
            return HttpResponseNotFound('User name or password is not correct!')

        uid = result[0]['m']['value']
        sparql = '''{} select ?m where {{ ?x wb:user_password ?m. 
                            ?x wb:user_uid "{}" .}}'''.format(prefix, uid)
        result = gstore.query('weibo', sparql)['results']['bindings']
        print('get password', result)
        if not result:
            if uid != password:
                return HttpResponseNotFound('User name or password is not correct!')
        else:
            true_passwd = result[0]['m']['value']
            if true_passwd != password:

                return HttpResponseNotFound('User name or password is not correct!')

        request.session['uid'] = uid
        #return redirect(reverse('myapp:profile'))
        return redirect(reverse('myapp:get_home'))
        # response.set_cookie("user", "1749705962")


def profile(request):
    uid = request.session['uid']
    print(uid, request.session)

    user = User(uid)
    user.load_from_db()

    s_user = SX_User(gstore)
    weibo_num = s_user.get_weibo_num(uid)
    follow_num = s_user.get_follow_num(uid)
    fan_num = s_user.get_fan_num(uid)
    context = {'user': user, 'weibo_num': weibo_num, 'follow_num': follow_num, 'fan_num': fan_num}
    return render(request, 'myapp/profile.html', context)


def register(request):
    return render(request, 'myapp/register.html')


def check_register(request):
    name = request.POST['name']
    password = request.POST['password']
    print('check name: ', name)
    sparql = '''{} select ?m where {{ ?x wb:user_name "{}". 
                        ?x wb:user_uid ?m .}}'''.format(prefix, name)
    result = gstore.query('weibo', sparql)['results']['bindings']
    if len(result) > 0:
        print(result)
        return HttpResponseNotFound('User name already exist.')

    sha_hex = sha256(name.encode('utf-8')).hexdigest()
    uid = int(sha_hex, 16) % 10**10
    uid = str(uid)
    print('new uid: ', uid)

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = User(uid, name, request.POST['screen_name'], request.POST['location'],
                request.POST['gender'], date, password)
    user.save_to_db()
    request.session['uid'] = uid
    return redirect(reverse('myapp:profile'))


def edit_profile(request):
    uid = request.session['uid']
    user = User(uid)
    user.load_from_db()
    context = {'user': user}
    return render(request, 'myapp/edit_profile.html', context)


def update_profile(request):
    uid = request.POST['uid']
    screen_name = request.POST['screen_name']
    password = request.POST['password']
    gender = request.POST['gender']
    location = request.POST['location']
    query = '''{} 
                delete {{ ?user wb:user_screen_name ?s }}
                insert {{ ?user wb:user_screen_name "{}" }}
                where {{ ?user wb:user_uid "{}" .
                        ?user wb:user_screen_name ?s}} 
                '''.format(prefix, screen_name, uid)
    gstore.query('weibo', query)
    query = '''{} 
                    delete {{ ?user wb:user_password ?s }}
                    insert {{ ?user wb:user_password "{}" }}
                    where {{ ?user wb:user_uid "{}" .
                            ?user wb:user_password ?s}} 
                    '''.format(prefix, password, uid)
    gstore.query('weibo', query)
    query = '''{} 
            delete {{ ?user wb:user_gender ?g }}
            insert {{ ?user wb:user_gender "{}" }}
            where {{ ?user wb:user_uid "{}" .
                    ?user wb:user_gender ?g}} 
            '''.format(prefix, gender, uid)
    gstore.query('weibo', query)
    query = '''{} 
                delete {{ ?user wb:user_location ?l }}
                insert {{ ?user wb:user_location "{}" }}
                where {{ ?user wb:user_uid "{}" .
                        ?user wb:user_location ?l}} 
                '''.format(prefix, location, uid)
    response = gstore.query('weibo', query)
    print(response)
    request.session['uid'] = uid
    return redirect(reverse('myapp:profile'))
