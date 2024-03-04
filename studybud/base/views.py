from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {"id" : 1, "name" : "Lets learn python"},
#     {"id" : 2, "name" : "Lets learn Machine Learning"},
#     {"id" : 3, "name" : "Lets learn Node.js"}
# ]


def home(request):
    if request.GET.get('q')!= None:
        q =request.GET.get('q')
    else:
        q= ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | #here topic is the var in room model
        Q(name__contains=q) |
        Q(description__contains=q)
        ) 
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {"rooms": rooms, "topics":topics, "room_count":room_count}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})
