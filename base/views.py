#from email import message
from email import message
from django.http import HttpResponse

from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q

from random import choice

from .models import Room, Topic, Message
from .forms import RoomForm
""" rooms = [
    {'id':0, 'name':'rrr'},
    {'id':1, 'name':'ADjaCka'},
    {'id':2, 'name':'ka'},
    {'id':3, 'name':'Diskeksik'},
] """

# Create your views here.
def home(request):
    q =request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) | 
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
                # works faster
    room_count = rooms.count()

    activity_comments = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context={'rooms':rooms, 'topics': topics, 'room_count':room_count, 'activity_comments':activity_comments}
    return render(request, 'base/home.html',context )

def room(request, pk):
    room = Room.objects.get(id=pk)
                # gets set of child Message
    comments = room.message_set.all()
    participants = room.participants.all()
    if request.method =='POST':
        new_comment = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context={'room': room, 'comments':comments,'participants':participants }
    return render(request, 'base/room.html', context)

def random_room(request):
    
    rooms = Room.objects.all()
    title = choice(rooms)
    
    roomid = Room.objects.get(name=title).id
    
    return redirect('room', roomid)



def user_profile(request, pk):

    user = User.objects.get(id=pk)

    rooms = user.room_set.all()
    comments = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms,'comments':comments, 'topics':topics}
    return render(request, 'base/profile.html',context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return(redirect(home))
    context={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('<h1>Go away!</h1>')

    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context ={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room (request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('<h1>Go away!</h1>')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obg':room})

@login_required(login_url='login')
def delete_comment (request, pk):
    comment = Message.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('<h1>Go away!</h1>')
    
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obg':comment})


def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method =="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "U're not existing! yet.. ")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, "Username or password does not exist ")
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    page = 'register'
    form = UserCreationForm()

    if request.method =="POST":
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username =user.username.lower()
            
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, " registration error ")

    return render(request, 'base/login_register.html', {'form':form})



   
def face_site(request):
    return render(request, 'index.html')