from together import Together
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64
from django.shortcuts import render, redirect
from pexels_api import API
import requests
  
genai.configure(api_key="AIzaSyBWrOq65UuHcogPJbS0Rzu3sgnmZcKS6Mw")
model = genai.GenerativeModel("gemini-1.5-flash")


def stock_content_gen(segments, tone):
    PEXELS_API_KEY = 't5kT5w0zmVw0AdR172RMGlpu128peM0fBMRVJTCHybydoKtj7oXhNfi0'

    api = API(PEXELS_API_KEY)

    print("The function")
    image_search_prompt = ""

    image_search_prompts = ['']
    for segment in segments:
        if segment != "":
            image_search_prompt = model.generate_content(f'''
            You are a model that is spezialized in creating image search prompts based on a given text.
            Your image search prompts have to be very, very short maximum 3 word length.
            In image search prompts you have to add the most appropriate text so that it is 
            as compatible as possible with the text that you are given. Here it is: {segment}.
            You also need to take into account the tone of the whole text which is given here: {tone}
            In you response you have to provide only the text that will be sent to the search engine.
            Three words is max it is recommented to use one or two words.
        ''')
            image_search_prompts.append(image_search_prompt.text)
          
     
    # for image_search_prompt in image_search_prompts:
    #  print(image_search_prompt)
    # api.search(f'{image_search_prompt}', page=1, results_per_page=1)


    

    # photos = api.get_entries()

    # for photo in photos:
    #     print('Photographer: ', photo.photographer)
    #     print('Photo url: ', photo.url)
    #     print('Photo original size: ', photo.original)




   


        
     