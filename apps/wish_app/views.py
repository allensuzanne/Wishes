from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Wish, Granted
import bcrypt

def index(request):
    print('*'*80)
    print("in the index method")
    if 'user' in request.session:    
        del request.session['user']
    return render (request, 'wish_app/index.html')

def register(request):
    print('*'*80)
    print("in the register method")
    request.session['fn']=request.POST['first_name']
    request.session['ln']=request.POST['last_name']
    request.session['e']=request.POST['email']
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        else:
            password=request.POST['password']
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash.decode())
            request.session['user']=request.POST['first_name']
            request.session['user_id']=new_user.id
            del request.session['ln']
            del request.session['fn']
            del request.session['e']

            return redirect ('/wishes')
    return redirect ('/')

def login(request):
    if request.method =='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user=User.objects.filter(email=request.POST['email'])
            logged_user=user[0]
            request.session['user'] = logged_user.first_name
            request.session['user_id']=logged_user.id
            return redirect ('/wishes')
    else:
        return redirect ('/')

def wishes_new(request):
    return render (request, 'wish_app/wishes_new.html')

def wishes_submit(request):
    print('*'*80)
    print("in the wishes_ad method")
    if request.method =='POST':
        errors = User.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/new')
        else: 
            user_id=request.session['user_id']
            this_wish=Wish.objects.create(item=request.POST['item'], description=request.POST['description'], wished_by=User.objects.get(id=user_id))
            return redirect ('/wishes')
    return redirect ("/wishes")

def remove_id(request, wish_id):
    print('*'*80)
    print("in the remove method")
    deadwish = Wish.objects.get(id=wish_id)
    deadwish.delete()
    return redirect ("/wishes")

def wishes_edit_id(request, wish_id):
    context = {
        'my_wish': Wish.objects.get(id=wish_id)
    }
    return render (request, 'wish_app/wishes_edit.html', context)

def wishes_change_id(request, wish_id):
    print('*'*80)
    print("in the change method")
    if request.method =='POST':
        errors = User.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/edit/'+wish_id)
        else: 
            wish=Wish.objects.get(id=wish_id)
            wish.item = request.POST['item']
            wish.description = request.POST['description']
            wish.save()
            return redirect ('/wishes')
    else:
        return redirect ("/wishes")

# ///////////////////////////////

def wishes(request):
    print('*'*80)
    print("in the wishes method")
    user_object = User.objects.get(id=request.session['user_id'])
    print("user object =", user_object)
    my_wishes = Wish.objects.filter(wished_by = user_object)
    print("my_wishes=",my_wishes)
    context= {
        'my_wishes': my_wishes,
        'all_granted': Granted.objects.all()
    }
    # print("context object, all granted", context)
    return render (request, 'wish_app/wishes.html', context)

# ///////////////////////////////
def wishes_stats(request):
    print('*'*80)
    print("in the stats method")
    all_granted = Granted.objects.all()
    your_granted = Granted.objects.filter(id=request.session['user_id'])
    stat1=all_granted.count
    stat2=your_granted.count

    context = {
        'your_wishes': Wish.objects.filter(wished_by=request.session['user_id']),
        'your_granted': Granted.objects.filter(wished_by=request.session['user_id']),
        'all_granted': Granted.objects.all(),
    }
    print('context object',context)
    return render (request, "wish_app/wishes_stats.html", context)

def granted_id(request, wish_id):
    print('*'*80)
    print("in the granted method")
    this_wish=Wish.objects.get(id=wish_id)
    print('this wish =',this_wish)
    this_granted=Granted.objects.create(item=this_wish.item, description=this_wish.description, wished_by=this_wish.wished_by)
    this_wish.delete()
    return redirect ('/wishes')


def like_id(request, wish_id):
    user_id=request.session['user_id']
    wishobject=Granted.objects.get(id=wish_id)
    this_user=User.objects.get(id=user_id)
    wishobject.wishers_who_like.add(this_user)
    return redirect ("/wishes")
