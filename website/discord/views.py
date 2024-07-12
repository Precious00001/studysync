from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
# from django.contrib.auth.models import CustomUser
from .models import Room, Topic, Message, CustomUser
from .forms import RoomForm, UserForm

# Create your views here.

# Define the view for the home page
def home(request):
    # Get the value of 'q' from the query parameters, defaulting to an empty string if not present
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    # Filter rooms based on search query
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |  # Filter rooms by topic name containing the search query
        Q(name__icontains=q) |          # Filter rooms by name containing the search query
        Q(description__icontains=q)     # Filter rooms by description containing the search query
    )

    # Retrieve the first 5 topics
    topics = Topic.objects.all()[0:5]

    # Count the number of filtered rooms
    room_count = rooms.count()

    # Filter messages based on the search query
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    # Prepare the context to be passed to the template
    context = {
        'rooms': rooms,                 # Filtered rooms
        'topics': topics,               # First 5 topics
        'room_count': room_count,       # Number of filtered rooms
        'room_messages': room_messages  # Filtered messages
    }

    # Render the home template with the provided context
    return render(request, 'discord/home.html', context)

# Define the view for a specific chat room
def room(request, pk):
    # Retrieve the room object with the specified primary key (pk)
    room = Room.objects.get(id=pk)
    
    # Retrieve all messages associated with the room
    room_messages = room.message_set.all()
    
    # Retrieve all participants in the room
    participants = room.participants.all()

    # If the request method is POST (i.e., form submission)
    if request.method == 'POST':
        # Create a new message object with the submitted data
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # Add the current user to the participants of the room
        room.participants.add(request.user) 
        # Redirect the user back to the current room page
        return redirect('discord:room', pk=room.id)

    # Prepare the context to be passed to the template
    context = {
        'room': room,                         # The current room
        'room_messages': room_messages,       # Messages in the current room
        'participants': participants          # Participants in the current room
    }

    # Render the room template with the provided context
    return render(request, 'discord/room.html', context)

# Define the view for creating a room
@login_required(login_url='login')  # Ensure that the user is logged in before accessing this view
def createRoom(request):
    # Create an instance of RoomForm
    form = RoomForm()
    
    # Retrieve all topics
    topics = Topic.objects.all()
    
    # If the request method is POST (i.e., form submission)
    if request.method == 'POST':
        # Retrieve the topic name from the form data
        topic_name = request.POST.get('topic')
        # Get or create a topic object with the retrieved name
        topic, created = Topic.objects.get_or_create(name=topic_name)

        # Create a new room object with the submitted data
        Room.objects.create(
            host=request.user,                          # The user creating the room
            topic=topic,                                # The topic associated with the room
            name=request.POST.get('name'),              # The name of the room
            description=request.POST.get('description') # The description of the room
        )
        
        # Redirect the user to the home page after creating the room
        return redirect('discord:home')

    # Prepare the context to be passed to the template
    context = {
        'form': form,     # Room creation form
        'topics': topics  # All topics
    }
    
    # Render the room creation form template with the provided context
    return render(request, 'discord/room_form.html', context)


# View for updating user profile
@login_required(login_url='login')  # Ensure that the user is logged in before accessing this view
def updateUser(request):
    # Retrieve the current user
    user = request.user
    # Create a form instance for updating the user profile with existing data
    form = UserForm(instance=user)

    # If the request method is POST (i.e., form submission)
    if request.method == 'POST':
        # Bind the form with the POST data
        form = UserForm(request.POST, request.FILES, instance=user)
        # Check if the form data is valid
        if form.is_valid():
            # Save the form data to update the user profile
            form.save()
            # Redirect the user to their profile page after updating the profile
            return redirect('discord:user-profile', pk=user.id)

    # Render the user profile update form template with the provided context
    return render(request, 'discord/update-user.html', {'form': form})

# View for displaying topics
def topicsPage(request):
    # Get the value of 'q' from the query parameters, defaulting to an empty string if not present
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    # Filter topics based on search query
    topics = Topic.objects.filter(name__icontains=q)
    # Render the topics template with the provided context
    return render(request, 'discord/topics.html', {'topics': topics})

# View for displaying activity
def activityPage(request):
    # Retrieve all messages
    room_messages = Message.objects.all()
    # Render the activity template with the provided context
    return render(request, 'discord/activity.html', {'room_messages': room_messages})

