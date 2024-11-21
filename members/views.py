from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import ChatForm
from datetime import datetime
import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .nlp import Chatbot
from .nlp1 import nlp_match_intent
from datetime import datetime

from django.shortcuts import render
from .nlp import Chatbot  # Import the chatbot class
from django.utils.safestring import mark_safe

# Initialize the chatbot instance

chatbot_instance = Chatbot()
chatbot_instance.load()

chat_history = []


from django.shortcuts import render
from .models import ChatHistory  # Import the model
from django.utils.safestring import mark_safe
from datetime import datetime

# Initialize the chatbot instance
chatbot_instance = Chatbot()
chatbot_instance.load()

def chatbots(request):
    # If the user is authenticated, retrieve their chat history from the database
    if request.user.is_authenticated:
        chat_history = ChatHistory.objects.filter(user=request.user).order_by('timestamp')
    else:
        chat_history = []

    if request.method == "POST":
        user_input = request.POST.get("message", "").strip()

        # Get the bot response
        bot_response = chatbot_instance.start_chatbot(user_input)

        # Append to chat history for display purposes (on the page)
        chat_history_display = list(chat_history)  # Copy existing chat history to preserve DB records
        chat_history_display.append({
            "user_query": user_input,
            "bot_response": mark_safe(bot_response),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Store the chat in the database for signed-in users
        if request.user.is_authenticated:
            ChatHistory.objects.create(
                user=request.user,
                user_query=user_input,
                bot_response=bot_response
            )
        else:
            # Store for anonymous users (user is null)
            ChatHistory.objects.create(
                user=None,
                user_query=user_input,
                bot_response=bot_response
            )

        return render(request, "chat1.html", {"chat_history": chat_history_display})

    return render(request, "chat1.html", {"chat_history": chat_history})





def signin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=uname, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('/')
        error = 'Username or password is incorrect'
        return render(request, 'login.html', {'error': error, 'username': uname})
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            error = 'Passwords do not match'
            return render(request, 'signup.html', {'error': error, 'username': uname, 'email': email})
        if User.objects.filter(username=uname).exists():
            error = 'Username already exists'
            return render(request, 'signup.html', {'error': error, 'username': uname, 'email': email})
        if User.objects.filter(email=email).exists():
            error = 'Email already registered'
            return render(request, 'signup.html', {'error': error, 'username': uname, 'email': email})
        user = User.objects.create(username=uname, email=email)
        user.set_password(pass1)
        user.save()
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('signin')
    return render(request, 'signup.html')



def home(request):
   # path=os.path.normpath('C:/Users/Smile/Documents/Chatbot_Project/college_chatbot/templates/home.html')
    return render(request, "home.html")