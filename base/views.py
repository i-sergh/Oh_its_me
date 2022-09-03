from django.shortcuts import render, redirect
from django.http import HttpResponse
from random import randint
from .models import Room
""" rooms = [
    {'id':0, 'name':'rrr'},
    {'id':1, 'name':'ADjaCka'},
    {'id':2, 'name':'ka'},
    {'id':3, 'name':'Diskeksik'},
] """

# Create your views here.
def home(request):
    rooms = Room.objects.all()

    print(rooms, len(rooms))
    context={'rooms':rooms}
    return render(request, 'base/home.html',context )
def room(request, pk):
    room = Room.objects.get(id=pk)
    context={'room': room  }
    print(context)
    return render(request, 'base/room.html', context)

def random_room(request):
    rooms = Room.objects.all()
    return redirect('room', randint(1,len(rooms)))

