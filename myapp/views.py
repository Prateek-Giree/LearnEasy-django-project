from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm

rooms = [
    # {'id':1,'name':'Python'},
    # {'id':2,'name':'Java'},
    # {'id':3,'name':'C'},
    # {'id':4,'name':'Php'},
]


def index(request):
    return render(request, "index.html")


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

    context = {}
    return render(request, "myapp/login_register.html", context)


def home(request):
    # for searching on the basis of topic or room or description
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__startswith=q)
        | Q(name__startswith=q)
        | Q(description__startswith=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()

    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
    return render(request, "myapp/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "myapp/room.html", context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "myapp/room_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "myapp/room_form.html", context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "myapp/delete.html", {"obj": room})
