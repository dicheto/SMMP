from together import Together
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64
from django.shortcuts import render, redirect
from pexels_api import API
import requests
import time
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
  
genai.configure(api_key="AIzaSyBWrOq65UuHcogPJbS0Rzu3sgnmZcKS6Mw")
model = genai.GenerativeModel("gemini-1.5-flash")


def stock_content_gen(segments, tone):
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
          
    searched_images_urls = ['']

    counter = 0
     
    for image_search_prompt in image_search_prompts:
        if image_search_prompt != '':
            PEXELS_API_KEY = 't5kT5w0zmVw0AdR172RMGlpu128peM0fBMRVJTCHybydoKtj7oXhNfi0'
            api = API(PEXELS_API_KEY)
            print(image_search_prompt)
            api.search(f'{image_search_prompt}', page=1, results_per_page=1)
            photos = api.get_entries()

            for photo in photos:
                print('Photographer: ', photo.photographer)
                print('Photo url: ', photo.url)
                print('Photo original size: ', photo.original)
                searched_images_urls.append(photo.original)

                save_path = f"C:/Users/Radostin Galev/Documents/GitHub/SMMP/assets/images/pexels-photo-144432{counter}.jpeg"

                try:
                  response = requests.get(photo.original)
                  response.raise_for_status()  

                  with open(save_path, 'wb') as file:
                      file.write(response.content)
                  print(f"Image successfully downloaded and saved to {save_path}")
                  counter += 1
                except requests.exceptions.RequestException as e:
                      print(f"An error occurred: {e}")
                
                query = urllib.parse.quote(image_search_prompt)
                url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    image_elements = soup.find_all("img")
                    for img in image_elements:
                        src = img.get("src") or img.get("data-src")
                        if src and src.startswith("http"):
                            searched_images_urls.append(src)
                            save_path = f"C:/Users/Radostin Galev/Documents/GitHub/SMMP/assets/pexels-photo-144432{counter}.jpeg"
                            try:
                                urllib.request.urlretrieve(src, save_path)
                                print(f"Bing image saved: {save_path}")
                                counter += 1
                            except Exception as e:
                                print(f"Error downloading from Bing: {e}")
                        if counter >= len(segments) * 2:
                            break
                else:
                    print("Failed to fetch Bing search results")




            

    print(searched_images_urls)



    


    

   




   


        
     