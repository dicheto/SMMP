import google.generativeai as genai
from django.shortcuts import render, redirect
import base64
from io import BytesIO
from PIL import Image
from together import Together
from supabase import create_client, Client
from . import main
from django.http import HttpResponse
import bcrypt


SUPABASE_URL = "https://lnitjdoumoecovyrmdgi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxuaXRqZG91bW9lY292eXJtZGdpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzcyNzk3ODEsImV4cCI6MjA1Mjg1NTc4MX0.TG4eJS00hHnqdVHc2tRp0Lyr3GO75KDjLL3cTsSONvA"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
video_gen_type = ""

def chooseGeneration(request):
    session_username = request.session.get('username')
    
    if request.method == "POST":
        video_gen_type_btn = request.POST.get('choose-btn')
        request.session['video_gen_type'] = video_gen_type_btn  # Store in session
    else:
        video_gen_type_btn = request.session.get('video_gen_type', '')

    return render(request, 'dashboard.html', {
        'username': session_username,
        'video_gen_type': video_gen_type_btn
    })

def dashboard(request): 
    session_username = request.session.get('username', '')
    video_gen_type = request.session.get('video_gen_type', '')

    if not session_username:
        return HttpResponse("You have to be logged in to see the dashboard")

    if request.method == 'POST':
        user_input = request.POST.get('script_input')
        video_length = request.POST.get('video_length')
        tone = request.POST.get('tone')

        if user_input and video_length and tone and video_gen_type:
            main.processing_user_data(user_input, video_length, tone, request, session_username, video_gen_type)
        else:
            return render(request, 'dashboard.html', {
                'username': session_username,
                'video_gen_type': video_gen_type,
                'error': 'Please fill all fields'
            })

    return render(request, 'dashboard.html', {
        'username': session_username,
        'video_gen_type': video_gen_type
    })

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        response = supabase.table("user_information") \
                           .select("user_id, username, password") \
                           .eq("username", username) \
                           .execute()
        if response.data:
            user_data = response.data[0]
            stored_hashed_password = user_data['password']

            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                # Store user details in the session
                request.session['user_id'] = user_data['user_id']
                request.session['username'] = user_data['username']

                return render(request, 'dashboard.html', {"username": request.session.get('username')})
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

def sign_in (request):

    if request.method == 'POST':
       username = request.POST.get ('username')
       password = request.POST.get ('password')
       confirm_password = request.POST.get ('confirm_password')


       if password != confirm_password:
           error_message = "Password do not match"
           return render(request , 'sign_in.html', {'error_message' : error_message})
       
       else:
           hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
           response = (
                supabase.table("user_information")
                .insert({'username': username, 'password': hashed_password.decode('utf-8')})
                .execute()
            )
           error_message = "Password match"
           return render(request , 'login.html', {'error_message' : error_message})

    return render(request, 'sign_in.html')

def logout (request):
    request.session.flush()
    return render(request, 'index.html')

