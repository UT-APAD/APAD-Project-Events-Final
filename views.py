from django.shortcuts import render
import pyrebase
from django.contrib import auth
from django.core.mail import send_mail

config = {

	"apiKey": "AIzaSyDHJUxtsUuIV-j4wguJO841QprGCi7Q5VE",
    "authDomain": "apad-events-app.firebaseapp.com",
    "databaseURL": "https://apad-events-app.firebaseio.com",
    "projectId": "apad-events-app",
    "storageBucket": "apad-events-app.appspot.com",
    "messagingSenderId": "687426306023"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

auth = firebase.auth()

def signIn(request):
	return render(request, "index.html")


def postSign(request):
	email = request.POST.get('form_username')
	password = request.POST.get('form_password')
	try:
	    user = auth.sign_in_with_email_and_password(email,password)
	except:
		message = "Invalid credentials. Please try again."
		return render(request,"events.html",{"messg":message})
	print(user['idToken'])
	session_id = user['idToken']
	request.session['uid']=str(session_id)
	return render(request, "events.html",{"e": email})


def logout(request):
    auth.logout(request)
    return render(request, 'index.html')


def signUp(request):
    return render(request,'signup.html')


def postsignup(request):

    first_nm =request.POST.get('first_nm')
    last_nm = request.POST.get('last_nm')
    email = request.POST.get('new_email')
    passw = request.POST.get('psw')
    subject = "Welcome to UT Events!"
    body = "Today was a great day!"
    from_email = 'mouhamed.ndoye@utexas.edu'
    to_email = [email]

    try:
        user = auth.create_user_with_email_and_password(email,passw)
        uid = user['localId']
        data = {"name":first_nm + " " + last_nm,"status" : "Active"}
        database.child("users").child(uid).child("details").set(data)
    except:
        message = "The account already exists. Please sign in."
        return render(request,"index.html",{"messg":message})
    send_mail(subject, body, from_email, to_email, fail_silently=False)
    return render(request, "welcome.html")

def contact(request):
    name =request.POST.get('name')
    mail =request.POST.get('mail')
    comment =request.POST.get('comment')
    subject = name
    from_email = 'mouhamed.ndoye@utexas.edu'
    to_email = [mail]
    send_mail(subject,comment,from_email,to_email,fail_silently=False)
    return render(request,'contact.html')


def create(request):
    return render(request,"submit_event.html")


def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz

    event_name = request.POST.get('event_name')
    location = request.POST.get('location')
    description = request.POST.get('description')
    event_type = request.POST.get('event_type')
    date_time = request.POST.get('date_time')
    event_tag = request.POST.get('event_tag')
    tz = pytz.timezone('America/Chicago')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    url = request.POST.get('url')
    idtoken = request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        'event_name':event_name,
        'location':location,
        'event_type':event_type,
        'description':description,
        'date_time':date_time,
        'event_tag':event_tag,
        'url':url,
        'user':a,
        'lat': '30.267153',
        'long': '-97.743061'
    }
    database.child('events').child(event_type).child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'events.html', {'e':name})


def my_events(request):
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        search = search.lower()
        uid = request.GET.get('uid')
        idtoken = request.session['uid']
        a = auth.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        print(search)
        print(idtoken)
        discounted_type = database.child('events').child('discounted').get().val()
        free_type = database.child('events').child('free').get().val()
        full_type = database.child('events').child('full_price').get().val()

        something = []

        for i in discounted_type:
            something.append(i)
        print(something)

        for i in free_type:
            something.append(i)
        print(something)

        for i in full_type:
            something.append(i)
        print(something)

        my_split = []

        for i in something:
            d_try = database.child('events').child('discounted').child(i).child('user').get().val()
            f_try = database.child('events').child('free').child(i).child('user').get().val()
            ft_try = database.child('events').child('full_price').child(i).child('user').get().val()
            if a == d_try:
                my_split.append(i)
            elif a == f_try:
                my_split.append(i)
            elif a == ft_try:
                my_split.append(i)
            else:
                pass
        print(my_split)

        my_list = []

        for i in my_split:
            free_tag = database.child('events').child('free').child(i).child('event_tag').shallow().get().val()
            discounted_tag = database.child('events').child('discounted').child(i).child('event_tag').shallow().get().val()
            full_tag = database.child('events').child('full_price').child(i).child('event_tag').shallow().get().val()
            free_split = free_tag.split(',')
            discounted_split = discounted_tag.split(',')
            full_split = full_tag.split(',')
            free_split = [x.strip(' ') for x in free_split]
            discounted_split = [x.strip(' ') for x in discounted_split]
            full_split = [x.strip(' ') for x in full_split]
            print(free_split)
            print(discounted_split)
            print(full_split)
            print(search)
            if search in free_split:
                my_list.append(i)
            elif search in discounted_split:
                my_list.append(i)
            elif search in full_split.append(i):
                my_list.append(i)

        print(my_list)

        location = []

        for i in my_list:
            loc = database.child('events').child('free').child(i).child('location').get().val()
            location.append(loc)
            loc_2 = database.child('events').child('discounted').child(i).child('location').get().val()
            location.append(loc_2)
            loc_3 = database.child('events').child('full_price').child(i).child('location').get().val()
            location.append(loc_3)
        location = [i for i in location if i is not None]
        print(location)

        event_type = []

        for i in my_list:
            et = database.child('events').child('free').child(i).child('event_type').get().val()
            event_type.append(et)
            et_2 = database.child('events').child('discounted').child(i).child('event_type').get().val()
            event_type.append(et_2)
            et_3 = database.child('events').child('full_price').child(i).child('event_type').get().val()
            event_type.append(et_3)
        event_type = [i for i in event_type if i is not None]
        print(event_type)

        event_name = []

        for i in my_list:
            en = database.child('events').child('free').child(i).child('event_name').get().val()
            event_name.append(en)
            en_2 = database.child('events').child('discounted').child(i).child('event_name').get().val()
            event_name.append(en_2)
            en_3 = database.child('events').child('full_price').child(i).child('event_name').get().val()
            event_name.append(en_3)
        event_name = [i for i in event_name if i is not None]
        print(event_name)

        date_time = []

        for i in my_list:
            dt = database.child('events').child('free').child(i).child('date_time').get().val()
            date_time.append(dt)
            dt_2 = database.child('events').child('discounted').child(i).child('date_time').get().val()
            date_time.append(dt_2)
            dt_3 = database.child('events').child('full_price').child(i).child('date_time').get().val()
            date_time.append(dt_3)
        date_time = [i for i in date_time if i is not None]
        print(date_time)

        event_tag = []

        for i in my_list:
            e_tag = database.child('events').child('free').child(i).child('event_tag').get().val()
            event_tag.append(e_tag)
            tag_2 = database.child('events').child('discounted').child(i).child('event_tag').get().val()
            event_tag.append(tag_2)
            tag_3 = database.child('events').child('full_price').child(i).child('event_tag').get().val()
            event_tag.append(tag_3)
        event_tag = [i for i in event_tag if i is not None]
        print(event_tag)

        description = []

        for i in my_list:
            desc = database.child('events').child('free').child(i).child('description').get().val()
            description.append(desc)
            desc_2 = database.child('events').child('discounted').child(i).child('description').get().val()
            description.append(desc_2)
            desc_3 = database.child('events').child('full_price').child(i).child('description').get().val()
            description.append(desc_3)
        description = [i for i in description if i is not None]
        print(description)

        url = []

        for i in my_list:
            urls = database.child('events').child('free').child(i).child('url').get().val()
            url.append(urls)
            urls_2 = database.child('events').child('discounted').child(i).child('url').get().val()
            url.append(urls_2)
            urls_3 = database.child('events').child('full_price').child(i).child('url').get().val()
            url.append(urls_3)
        url = [i for i in url if i is not None]
        print(url)

        comb_lis = zip(my_list, event_name, date_time, event_type, location, description, event_tag, url)
        name = database.child('users').child(a).child('details').child('name').get().val()

        return render(request, 'my_events.html', {'comb_lis': comb_lis, 'e': name, 'uid': a})


    else:
        idtoken = request.session['uid']
        a = auth.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        discounted_type = database.child('events').child('discounted').get().val()
        free_type = database.child('events').child('free').get().val()
        full_type = database.child('events').child('full_price').get().val()

        something = []

        for i in discounted_type:
            something.append(i)
        print(something)

        for i in free_type:
            something.append(i)
        print(something)

        for i in full_type:
            something.append(i)
        print(something)

        my_list = []

        for i in something:
            d_try = database.child('events').child('discounted').child(i).child('user').get().val()
            f_try = database.child('events').child('free').child(i).child('user').get().val()
            ft_try = database.child('events').child('full_price').child(i).child('user').get().val()
            if a == d_try:
                my_list.append(i)
            elif a == f_try:
                my_list.append(i)
            elif a == ft_try:
                my_list.append(i)
            else:
                pass
        print(my_list)

        location = []

        for i in my_list:
            loc = database.child('events').child('free').child(i).child('location').get().val()
            location.append(loc)
            loc_2 = database.child('events').child('discounted').child(i).child('location').get().val()
            location.append(loc_2)
            loc_3 = database.child('events').child('full_price').child(i).child('location').get().val()
            location.append(loc_3)
        location = [i for i in location if i is not None]
        print(location)

        event_type = []

        for i in my_list:
            et = database.child('events').child('free').child(i).child('event_type').get().val()
            event_type.append(et)
            et_2 = database.child('events').child('discounted').child(i).child('event_type').get().val()
            event_type.append(et_2)
            et_3 = database.child('events').child('full_price').child(i).child('event_type').get().val()
            event_type.append(et_3)
        event_type = [i for i in event_type if i is not None]
        print(event_type)

        event_name = []

        for i in my_list:
            en = database.child('events').child('free').child(i).child('event_name').get().val()
            event_name.append(en)
            en_2 = database.child('events').child('discounted').child(i).child('event_name').get().val()
            event_name.append(en_2)
            en_3 = database.child('events').child('full_price').child(i).child('event_name').get().val()
            event_name.append(en_3)
        event_name = [i for i in event_name if i is not None]
        print(event_name)

        date_time = []

        for i in my_list:
            dt = database.child('events').child('free').child(i).child('date_time').get().val()
            date_time.append(dt)
            dt_2 = database.child('events').child('discounted').child(i).child('date_time').get().val()
            date_time.append(dt_2)
            dt_3 = database.child('events').child('full_price').child(i).child('date_time').get().val()
            date_time.append(dt_3)
        date_time = [i for i in date_time if i is not None]
        print(date_time)

        event_tag = []

        for i in my_list:
            e_tag = database.child('events').child('free').child(i).child('event_tag').get().val()
            event_tag.append(e_tag)
            tag_2 = database.child('events').child('discounted').child(i).child('event_tag').get().val()
            event_tag.append(tag_2)
            tag_3 = database.child('events').child('full_price').child(i).child('event_tag').get().val()
            event_tag.append(tag_3)
        event_tag = [i for i in event_tag if i is not None]
        print(event_tag)

        description = []

        for i in my_list:
            desc = database.child('events').child('free').child(i).child('description').get().val()
            description.append(desc)
            desc_2 = database.child('events').child('discounted').child(i).child('description').get().val()
            description.append(desc_2)
            desc_3 = database.child('events').child('full_price').child(i).child('description').get().val()
            description.append(desc_3)
        description = [i for i in description if i is not None]
        print(description)

        url = []

        for i in my_list:
            urls = database.child('events').child('free').child(i).child('url').get().val()
            url.append(urls)
            urls_2 = database.child('events').child('discounted').child(i).child('url').get().val()
            url.append(urls_2)
            urls_3 = database.child('events').child('full_price').child(i).child('url').get().val()
            url.append(urls_3)
        url = [i for i in url if i is not None]
        print(url)

        comb_lis = zip(my_list, event_name, date_time, event_type, location, description, event_tag, url)
        name = database.child('users').child(a).child('details').child('name').get().val()

        return render(request,'my_events.html',{'comb_lis':comb_lis,'e':name,'uid':a})

def specific_event(request):

    import datetime

    time = request.GET.get('z')
    e_type = request.GET.get('e')

    idtoken = request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    event_name = database.child('events').child(e_type).child(time).child('event_name').get().val()
    description = database.child('events').child(e_type).child(time).child('description').get().val()
    event_type = database.child('events').child(e_type).child(time).child('event_type').get().val()
    date_time = database.child('events').child(e_type).child(time).child('date_time').get().val()
    event_tag = database.child('events').child(e_type).child(time).child('event_tag').get().val()
    location = database.child('events').child(e_type).child(time).child('location').get().val()
    img_url = database.child('events').child(e_type).child(time).child('url').get().val()
    i = str(time)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,'specific_event.html',{'l':location,'en':event_name,'desc':description,'et':event_type,'dt':date_time,'e_tag':event_tag,'i':img_url})


def free(request):
    idtoken = request.session['uid']
    free_sub = 'FREE'
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        'FREE': a
    }
    database.child('users').child(a).child('Subscriptions').child(free_sub).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'free_events.html', {'e': name})


def discounted(request):
    idtoken = request.session['uid']
    discounted_sub = 'DISCOUNTED'
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        'DISCOUNTED': a
    }
    database.child('users').child(a).child('Subscriptions').child(discounted_sub).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'discounted_events.html', {'e': name})

def full_price(request):
    idtoken = request.session['uid']
    full_price = 'FULL PRICE'
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        'FULL PRICE': a
    }
    database.child('users').child(a).child('Subscriptions').child(full_price).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'fullprice_events.html', {'e': name})

def free_page(request):
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        search = search.lower()
        uid = request.GET.get('uid')
        print(search)
        print(uid)
        timestamps = database.child('events').child('free').get().val()
        et_id = []

        for i in timestamps:
            e_tag = database.child('events').child('free').child(i).child('event_tag').shallow().get().val()
            et_split = e_tag.split(',')
            et_split = [x.strip(' ') for x in et_split]
            print(et_split)
            print(search)
            if search in et_split:
                et_id.append(i)
        print(et_id)

        location = []

        for i in et_id:
            loc = database.child('events').child('free').child(i).child('location').get().val()
            location.append(loc)
        print(location)

        event_tag = []

        for i in et_id:
            et = database.child('events').child('free').child(i).child('event_tag').get().val()
            event_tag.append(et)
        print(event_tag)

        event_type = []

        for i in et_id:
            et = database.child('events').child('free').child(i).child('event_type').get().val()
            event_type.append(et)
        print(event_type)

        event_name = []

        for i in et_id:
            en = database.child('events').child('free').child(i).child('event_name').get().val()
            event_name.append(en)
        print(event_name)

        date_time = []

        for i in et_id:
            dt = database.child('events').child('free').child(i).child('date_time').get().val()
            date_time.append(dt)
        print(date_time)

        description = []

        for i in et_id:
            desc = database.child('events').child('free').child(i).child('description').get().val()
            description.append(desc)
        print(description)

        url = []

        for i in et_id:
            desc = database.child('events').child('free').child(i).child('url').get().val()
            url.append(desc)
        print(url)

        comb_lis = zip(et_id, event_name, date_time, event_type, location, description, event_tag, url)
        name = database.child('users').child(uid).child('details').child('name').get().val()

        return render(request, 'free_events.html', {'comb_lis': comb_lis, 'e': name})

    else:

        idtoken = request.session['uid']
        a = auth.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']

        timestamps = database.child('events').child('free').shallow().get().val()
        lis_time = []
        for i in timestamps:
            lis_time.append(i)

        lis_time.sort(reverse=True)

        print(lis_time)
        location = []

        for i in lis_time:
            loc = database.child('events').child('free').child(i).child('location').get().val()
            location.append(loc)
        print(location)

        event_type = []

        for i in lis_time:
            et = database.child('events').child('free').child(i).child('event_type').get().val()
            event_type.append(et)
        print(event_type)

        event_name = []

        for i in lis_time:
            en = database.child('events').child('free').child(i).child('event_name').get().val()
            event_name.append(en)
        print(event_name)

        date_time = []

        for i in lis_time:
            dt = database.child('events').child('free').child(i).child('date_time').get().val()
            date_time.append(dt)
        print(date_time)

        event_tag = []

        for i in lis_time:
            e_tag = database.child('events').child('free').child(i).child('event_tag').get().val()
            event_tag.append(e_tag)
        print(event_tag)

        description = []

        for i in lis_time:
            desc = database.child('events').child('free').child(i).child('description').get().val()
            description.append(desc)
        print(description)

        url = []

        for i in lis_time:
            desc = database.child('events').child('free').child(i).child('url').get().val()
            url.append(desc)
        print(url)

        comb_lis = zip(lis_time, event_name, date_time, event_type, location, description, event_tag, url)
        name = database.child('users').child(a).child('details').child('name').get().val()

        return render(request, 'free_events.html', {'comb_lis': comb_lis, 'e': name, 'uid': a})

def discounted_page(request):

    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        search = search.lower()
        uid = request.GET.get('uid')
        print(search)
        print(uid)
        timestamps = database.child('events').child('discounted').get().val()
        et_id = []

        for i in timestamps:
            e_tag = database.child('events').child('discounted').child(i).child('event_tag').shallow().get().val()
            et_split = e_tag.split(',')
            et_split = [x.strip(' ') for x in et_split]
            print(et_split)
            print(search)
            if search in et_split:
                et_id.append(i)
        print(et_id)

        location = []

        for i in et_id:
            loc = database.child('events').child('discounted').child(i).child('location').get().val()
            location.append(loc)
        print(location)

        event_tag = []

        for i in et_id:
            et = database.child('events').child('discounted').child(i).child('event_tag').get().val()
            event_tag.append(et)
        print(event_tag)

        event_type = []

        for i in et_id:
            et = database.child('events').child('discounted').child(i).child('event_type').get().val()
            event_type.append(et)
        print(event_type)

        event_name = []

        for i in et_id:
            en = database.child('events').child('discounted').child(i).child('event_name').get().val()
            event_name.append(en)
        print(event_name)

        date_time = []

        for i in et_id:
            dt = database.child('events').child('discounted').child(i).child('date_time').get().val()
            date_time.append(dt)
        print(date_time)

        description = []

        for i in et_id:
            desc = database.child('events').child('discounted').child(i).child('description').get().val()
            description.append(desc)
        print(description)

        url = []

        for i in et_id:
            desc = database.child('events').child('discounted').child(i).child('url').get().val()
            url.append(desc)
        print(url)

        comb_lis = zip(et_id, event_name, date_time, event_type, location, description, event_tag, url)
        name = database.child('users').child(uid).child('details').child('name').get().val()

        return render(request, 'discounted_events.html', {'comb_lis': comb_lis, 'e': name})

    else:

        idtoken = request.session['uid']
        a = auth.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']

        timestamps = database.child('events').child('discounted').shallow().get().val()
        lis_time = []
        for i in timestamps:
            lis_time.append(i)

        lis_time.sort(reverse=True)

        print(lis_time)
        location = []

        for i in lis_time:
            loc = database.child('events').child('discounted').child(i).child('location').get().val()
            location.append(loc)
        print(location)

        event_type = []

        for i in lis_time:
            et = database.child('events').child('discounted').child(i).child('event_type').get().val()
            event_type.append(et)
        print(event_type)

        event_name = []

        for i in lis_time:
            en = database.child('events').child('discounted').child(i).child('event_name').get().val()
            event_name.append(en)
        print(event_name)

        date_time = []

        for i in lis_time:
            dt = database.child('events').child('discounted').child(i).child('date_time').get().val()
            date_time.append(dt)
        print(date_time)

        event_tag = []

        for i in lis_time:
            e_tag = database.child('events').child('discounted').child(i).child('event_tag').get().val()
            event_tag.append(e_tag)
        print(event_tag)

        description = []

        for i in lis_time:
            desc = database.child('events').child('discounted').child(i).child('description').get().val()
            description.append(desc)
        print(description)

        url = []

        for i in lis_time:
            desc = database.child('events').child('discounted').child(i).child('url').get().val()
            url.append(desc)
        print(url)

        comb_lis = zip(lis_time, event_name, date_time, event_type, location, description, event_tag, url)
        name = database.child('users').child(a).child('details').child('name').get().val()

        return render(request, 'discounted_events.html', {'comb_lis': comb_lis, 'e': name, 'uid': a})

def fullprice_page(request):
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        search = search.lower()
        uid = request.GET.get('uid')
        print(search)
        print(uid)
        timestamps = database.child('events').child('full_price').get().val()
        et_id = []

        for i in timestamps:
            e_tag = database.child('events').child('full_price').child(i).child('event_tag').shallow().get().val()
            et_split = e_tag.split(',')
            et_split = [x.strip(' ') for x in et_split]
            print(et_split)
            print(search)
            if search in et_split:
                et_id.append(i)
        print(et_id)

        location = []

        for i in et_id:
            loc = database.child('events').child('full_price').child(i).child('location').get().val()
            location.append(loc)
        print(location)

        event_tag = []

        for i in et_id:
            et = database.child('events').child('full_price').child(i).child('event_tag').get().val()
            event_tag.append(et)
        print(event_tag)

        event_type = []

        for i in et_id:
            et = database.child('events').child('full_price').child(i).child('event_type').get().val()
            event_type.append(et)
        print(event_type)

        event_name = []

        for i in et_id:
            en = database.child('events').child('full_price').child(i).child('event_name').get().val()
            event_name.append(en)
        print(event_name)

        date_time = []

        for i in et_id:
            dt = database.child('events').child('full_price').child(i).child('date_time').get().val()
            date_time.append(dt)
        print(date_time)

        description = []

        for i in et_id:
            desc = database.child('events').child('full_price').child(i).child('description').get().val()
            description.append(desc)
        print(description)

        url = []

        for i in et_id:
            desc = database.child('events').child('full_price').child(i).child('url').get().val()
            url.append(desc)
        print(url)

        comb_lis = zip(et_id, event_name,date_time,event_type,location,description,event_tag,url)
        name = database.child('users').child(uid).child('details').child('name').get().val()

        return render(request, 'fullprice_events.html', {'comb_lis': comb_lis, 'e': name})

    else:

        idtoken = request.session['uid']
        a = auth.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']

        timestamps = database.child('events').child('full_price').shallow().get().val()
        lis_time = []
        for i in timestamps:
            lis_time.append(i)

        lis_time.sort(reverse=True)

        print(lis_time)
        location = []

        for i in lis_time:
            loc = database.child('events').child('full_price').child(i).child('location').get().val()
            location.append(loc)
        print(location)

        event_type = []

        for i in lis_time:
            et = database.child('events').child('full_price').child(i).child('event_type').get().val()
            event_type.append(et)
        print(event_type)

        event_name = []

        for i in lis_time:
            en = database.child('events').child('full_price').child(i).child('event_name').get().val()
            event_name.append(en)
        print(event_name)

        date_time = []

        for i in lis_time:
            dt = database.child('events').child('full_price').child(i).child('date_time').get().val()
            date_time.append(dt)
        print(date_time)

        event_tag = []

        for i in lis_time:
            e_tag = database.child('events').child('full_price').child(i).child('event_tag').get().val()
            event_tag.append(e_tag)
        print(event_tag)

        description = []

        for i in lis_time:
            desc = database.child('events').child('full_price').child(i).child('description').get().val()
            description.append(desc)
        print(description)

        url = []

        for i in lis_time:
            desc = database.child('events').child('full_price').child(i).child('url').get().val()
            url.append(desc)
        print(url)

        comb_lis = zip(lis_time, event_name, date_time, event_type, location, description, event_tag, url)
        name = database.child('users').child(a).child('details').child('name').get().val()

        return render(request, 'fullprice_events.html', {'comb_lis': comb_lis, 'e': name, 'uid': a})