from rest_framework.serializers import ModelSerializer
from myapp.models import Room


# serializing Room model inorder to send it to frontend
# it is necessary to convert model instance into python datatype to render as json


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        # to serilize few selected fields note: fields variable only take list or tuple
        # option=['id','name']
        # fields = option

        # to serilize all fields
        fields = "__all__"
