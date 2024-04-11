from django.forms import ModelForm
from .models import Room


# generating form fields based on Room model
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["host", "participants"]
