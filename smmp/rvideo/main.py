from together import Together
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64
from django.shortcuts import render, redirect
from rvideo.script_generation_module.script_generation import script_gen
from .background_generation_module.ai_image_generation import ai_image_gen
from django.http import HttpResponse

user_input = ''
video_lenght = 0
tone = ''
request = None
session_username = ''
video_gen_type = ''

def processing_user_data(user_input, video_length, tone, request, session_username, video_gen_type):
    user_input = user_input
    video_length = video_length
    tone = tone
    request = request
    session_username = session_username
    video_gen_type = video_gen_type

    if video_gen_type == "AI Generation":
        script_segments = script_gen(user_input, video_length, tone)
        ai_image_gen(script_segments, tone)
        return render(request, 'dashboard.html', {"username" : session_username})
    elif video_gen_type == "Script Generation":
        pass
    else:
        return HttpResponse("Invalid video generation type")





