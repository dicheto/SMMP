from together import Together
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64
from django.shortcuts import render, redirect

genai.configure(api_key="AIzaSyBWrOq65UuHcogPJbS0Rzu3sgnmZcKS6Mw")
model = genai.GenerativeModel("gemini-1.5-flash")

def script_gen (user_input, video_length, tone):    
    prompt = f"""
    You are a model specialized in creating scripts for short-form videos that will be used on platforms like TikTok, Instagram Reels, and YouTube Shorts.
    Here is the user input: {user_input}. Based on the user input and the video length: {video_length}seconds, create a script to be added as a voiceover to the video.
    Ensure the script aligns with the tone: {tone}. Do not add any additional details only and only the exact words
    that the narrator has to say.
    """
    script_response = model.generate_content(prompt)
    script_text = script_response.text

    full_segment_text = model.generate_content(f"""
    You are a model specialized in creating segments out of a given script.You have to analyze the script and break it down into smaller segments based on context and what the
    narrator is talking about. IT IS ABSOLUTELY FORBIDDEN TO CHANGE ANY TEXT OF THE ORIGINAL SCRIPT WHATSOEVER. YOU ONLY HAVE TO ANALYZE IT AND CUT IT INTO MULTIPLE PARTS.
    This is the script: {script_text}
    Each segment should start with "#" and end with "*".It has to be enloclosed with "#" and "*".
    """)
                
    full_segmented_text = full_segment_text.text

    segments = [""]
    current_segment = ""
    inside_segment = False

    for char in full_segmented_text:
        if char == "#": 
            inside_segment = True
            current_segment = ""
        elif char == "*":  
            if inside_segment:
                segments.append(current_segment.strip())
                inside_segment = False
        elif inside_segment:
            current_segment += char

    return segments
 