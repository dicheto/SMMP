import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image
from together import Together

user_input = input()

video_length = 30
# tone could be happy, scary, creepy, realstic, cartoon, etc.
tone = ""


genai.configure(api_key="AIzaSyBWrOq65UuHcogPJbS0Rzu3sgnmZcKS6Mw")
model = genai.GenerativeModel("gemini-1.5-flash")
script_response = model.generate_content(f'''
You are a model specizialized in creating scripts for short form videos that will be used in platforms like TikTok, Instagram Reels, YouTube Shorts.
You will be given a user input which will contain data about the topic of the video. Here is the user input: {user_input}. Based on the user input and on the video length: {video_length}s
you have to create a script that will be added as a voiceover to the video.It should contain the exact words that the spokesperson has to say without any additional details or text
no info about when they should be said or what kind of music is appropariate only and only the text which is suposed to be said. 
Make the scripts engaging with the audience and use phrases like "Did you know" if necessary.
                                  ''')
output_script = script_response.text




image_generation_response = model.generate_content(f'''
You are a modezl specialied in creating image generation prompts based on a given script: {output_script}.The script contains only the text that will be said by the narrator.
You have to create image generation prompts that will be aligned with the topic of the script and should be very detailed (we are using flux 1.0 schell model) and descriptive
to generate the most appropriate image according to the script.You also have to take into account the length of the video that the script is based on here it is:{video_length}s.
Every image generation prompt should both start  with "#" and end with "*". You have give only and only the image generation prompts that will be given to the ai (enclosed with "#" and "*") no additional
details are allowed ot should be added.I suggest to make the images more realistic for the most part (of course if the topic is allowing it) but you can have that in mind.
Do not create maps do it only if it is specified in the user_input: {user_input} otherwise just don't create image prompts featuring maps.Make each image distinct and not 
all that close to the previous one (of course if not speciffically specified). Every image should feel different to the previous one(of course keeping the same tone and being
inline with the scripts and its topic).
''')

image_gen_prompts_text = str(image_generation_response.text)
image_generation_prompts = {""}
image_generation_prompts.clear()

for counter in range(len(image_gen_prompts_text)):
    prompt_start = 0
    prompt_end = 0

    if image_gen_prompts_text[counter] == "#":
        prompt_start = counter

    if image_gen_prompts_text[counter] == "*":
        prompt_end = counter
        image_prompt = ""
        for index in range(prompt_start + 1, prompt_end):
            image_prompt += image_gen_prompts_text[index]
        image_generation_prompts.add(image_prompt)
        prompt_start = 0
        prompt_end = 0
    
client = Together()


filtered_prompts = {prompt.strip() for prompt in image_generation_prompts if prompt.strip()}
print("Filtered Prompts:", filtered_prompts)


for image_prompt in filtered_prompts:
    try:

        response = client.images.generate(
            prompt=f"{image_prompt} The image should be one, continious and it should fill the screen. Do not make it look like that it is comprised of more than one image.Do not add any text whatsoever to the images.",
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

    except Exception as e:
        print(f"Error generating image for prompt '{image_prompt}': {e}")


                                    


