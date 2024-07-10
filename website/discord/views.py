from django.shortcuts import render

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