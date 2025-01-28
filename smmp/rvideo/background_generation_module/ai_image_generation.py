from together import Together
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64
from django.shortcuts import render, redirect
  
genai.configure(api_key="AIzaSyBWrOq65UuHcogPJbS0Rzu3sgnmZcKS6Mw")
model = genai.GenerativeModel("gemini-1.5-flash")


def ai_image_gen(segments,tone):

    client = Together(api_key="a1d7f4fa1976a1eff3d991f0df4eba0f2419b2922ae586a6aabd559ca816fead")
    image_generation_prompt = ""

    image_gen_prompts = ['']
    for segment in segments:
        if segment != "":
            image_generation_prompt = model.generate_content(f'''
            You are a model that is spezialized in creating image generation prompts based on a given text.
            The prompt should be very descriptive and as detailed as possible for the ai to understand.
            This is the text: {segment}. Do not add any maps or text to the images whatsoever.
            You also need to take into account the tone of the whole text which is given here: {tone}
        ''')
            image_gen_prompts.append(image_generation_prompt.text)

    
                 
    for image_gen_prompt in image_gen_prompts:
        if image_gen_prompt != "":
                print(image_gen_prompt)
                response = client.images.generate(
                prompt=f"{image_gen_prompt} Do not add any maps or text to the images whatsoever.The image has to be continous and connected.It cant look like it is comprised of multiple images",
                model="black-forest-labs/FLUX.1-schnell-Free",
                width=1008,
                height=1792,
                steps=1,
                n=1,
                response_format="b64_json"
                )
        
                b64_image = response.data[0].b64_json
                image_data = base64.b64decode(b64_image)
                image = Image.open(BytesIO(image_data))
                image.show()
                