from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from datetime import datetime, timedelta
from django.utils import timezone

rooms = []


def index(request):
    return render(request, "index.html")


def loginPage(request):
    page = "login"
    # if user is already logged in then redirect to home. Prevent relogin
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)  # create session
                return redirect("home")
            else:
                messages.error(request, "Username or password does not match")
        except User.DoesNotExist:
            messages.error(request, "User does not exist")

    context = {"page": page}
    return render(request, "myapp/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("index")


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)  # save but not save in db
            user.username = user.username.lower()
            user.save()  # save in db
            login(request, user)
            return redirect("home")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return render(request, "myapp/login_register.html", {"form": form})


@login_required(login_url="login")  # only logged in user can access
def home(request):
    # for searching on the basis of topic or room or description
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__startswith=q)
        | Q(name__startswith=q)
        | Q(description__startswith=q)
    )

    room_count = rooms.count()
    topics = Topic.objects.all()[0:4]

    # current_time = datetime.now()
    # cutoff_time = current_time - timedelta(days=2)
    # room_messages = Message.objects.filter(
    #     created__gt=cutoff_time,
    #     created__lte=cutoff_time
    #     + timedelta(days=1),  # Filters messages posted exactly 2 days ago
    #     room__topic__name__startswith=q,  # Filters messages according to topic
    # )
    room_messages = Message.objects.filter(room__topic__name__startswith=q).order_by(
        "-created"
    )[:10]

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    return render(request, "myapp/home.html", context)


@login_required(login_url="login")
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()

    participants = room.participants.all()  # get all participants of room
    # messaging feature
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get(
                "body"
            ),  # get message from form. 'body' is the name attribute of tag
        )
        # add user to participants
        room.participants.add(request.user)
        # Reloding page after message is sent to show message
        return redirect("room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "myapp/room.html", context)


@login_required(login_url="login")
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        # if topic already exists then get else create
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")
    context = {"form": form, "topics": topics}
    return render(request, "myapp/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    # only host can update
    if request.user != room.host:
        return HttpResponse("Only host can update room")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        # if topic already exists then get else create
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("home")

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "myapp/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("Only host can delete room")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "myapp/delete.html", {"obj": room})


@login_required(login_url="login")
def deleteMessage(request, room_id, pk):
    message = Message.objects.get(id=pk)

    if request.method == "POST":
        message.delete()
        return redirect("room", pk=room_id)  # pk is parameter in room url

    return render(request, "myapp/delete.html", {"obj": message})


@login_required(login_url="login")
def deleteActivityMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == "POST":
        message.delete()
        return redirect("home")  # pk is parameter in room url
    return render(request, "myapp/delete.html", {"obj": message})


@login_required(login_url="login")
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    # fetches all the rooms associated with a particular user
    rooms = user.room_set.all()
    # fetches all the messages associated with a particular user
    room_messages = user.message_set.all()
    # fetch all the topics
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "myapp/profile.html", context)


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)
    return render(request, "myapp/update_user.html", {"form": form})


@login_required(login_url="login")
def topicPage(request):
    rooms = Room.objects.all()
    room_count = rooms.count()

    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    return render(
        request, "myapp/topics.html", {"topics": topics, "room_count": room_count}
    )


@login_required(login_url="login")
def activityPage(request):
    room_messages = Message.objects.order_by("-created")[:10]
    return render(request, "myapp/activity.html", {"room_messages": room_messages})
