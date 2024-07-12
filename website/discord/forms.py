from django.forms import ModelForm
from .models import Room
# from django.contrib.auth.models import User
from discord.models import CustomUser

# Form for creating or updating a Room model instance
class RoomForm(ModelForm):
    class Meta:
         # Specify the model the form is associated with
        model = Room
        # Include all fields of the Room model in the form
        fields = '__all__'
        # Exclude 'host' and 'participants' fields from the form
        exclude = ['host', 'participants']

# Form for updating User model instance
class UserForm(ModelForm):
    class Meta:
        # Specify the model the form is associated with
        model = CustomUser
        # Include only 'username' and 'email' fields in the form
        fields = ['profile_picture','username', 'email']