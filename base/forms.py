from dataclasses import fields
from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields ='__all__' # it may be a list of fields from Room
        exclude = ['host', 'participants']         
