from django.shortcuts import render, redirect
from django.db.models import Q


from random import randint

from .models import Room, Topic
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

    context={'rooms':rooms, 'topics': topics, 'room_count':room_count}
    return render(request, 'base/home.html',context )

def room(request, pk):
    room = Room.objects.get(id=pk)
    context={'room': room  }
    print(context)
    return render(request, 'base/room.html', context)

def random_room(request):
    rooms = Room.objects.all()
    return redirect('room', randint(1,len(rooms)))

def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return(redirect(home))
    context={'form':form}
    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room)

    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context ={'form':form}
    return render(request, 'base/room_form.html', context)


def delete_room (request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obg':room})
