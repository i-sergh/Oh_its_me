from django.shortcuts import render, redirect
from django.http import HttpResponse
from random import randint

rooms = [
    {'id':0, 'name':'rrr'},
    {'id':1, 'name':'ADjaCka'},
    {'id':2, 'name':'ka'},
    {'id':3, 'name':'Diskeksik'},
]

# Create your views here.
def home(request):
    context={'rooms':rooms}
    return render(request, 'base/home.html',context )
def room(request, pk):
    
    context={'room': rooms[int(pk)]['name']  }
    print(context)
    return render(request, 'base/room.html', context)

def random_room(request):

    return redirect('room', randint(0,len(rooms)-1))

