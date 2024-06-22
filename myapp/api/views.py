from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import Room
from .serializers import RoomSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "GET /api",
        "GET /api/rooms",
        "GET /api/rooms/:id",
    ]
    return Response(routes)


# to get all the rooms
@api_view(["GET"])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)  # many = true for multiple rooms
    return Response(serializer.data)


# to get selected room
@api_view(["GET"])
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
