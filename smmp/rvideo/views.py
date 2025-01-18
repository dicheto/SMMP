import google.generativeai as genai
from django.shortcuts import render
import base64
from io import BytesIO
from PIL import Image
from together import Together


def home(request):
   return render(request, 'index.html')

def dashboard(request): 
     if request.method == 'POST':
        user_input = request.POST.get('script_input')
        video_length = request.POST.get('video_length')
        tone = request.POST.get('tone')

        if user_input and video_length and tone:
                genai.configure(api_key="AIzaSyBWrOq65UuHcogPJbS0Rzu3sgnmZcKS6Mw")

                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"""
                You are a model specialized in creating scripts for short-form videos that will be used on platforms like TikTok, Instagram Reels, and YouTube Shorts.
                Here is the user input: {user_input}. Based on the user input and the video length: {video_length}s, create a script to be added as a voiceover to the video.
                Ensure the script aligns with the tone: {tone}. Do not add any additional details only and only the exact words
                that the narrator has to say.
                """
                script_response = model.generate_content(prompt)
                script_text = script_response.text

                full_segment_text = model.generate_content(f"""sumary_line
                You are a model specialized in creating segments out of a given script.You have to analyze the script and brake it down into smaller segments based on context and what the
                narrator is talking about. IT IS ABSOLUTELY FORBIDDEN TO CHANGE ANY TEXT OF THE ORIGINAL SCRIPT WHATSOEVER. YOU ONLY HAVE TO ANALYZE IT AND CUT IT INTO MULTIPLE PARTS.
                This is the script: {script_text}
                Each segment should start with "#" and end with "*".It has to be enloclosed with "#" and "*".
                """)
                
                full_segmented_text = full_segment_text.text

                segments = [""]
                current_segment = ""
                inside_segment = False

                for char in full_segmented_text:
                    if char == "#":  # Start of a segment
                       inside_segment = True
                       current_segment = ""
                    elif char == "*":  
                        if inside_segment:
                           segments.append(current_segment.strip())
                           inside_segment = False
                    elif inside_segment:
                        current_segment += char
 
                
                client = Together()
                image_generation_prompt = ""

                image_gen_prompts = ['']
                for segment in segments:
                    if segment != "":
                        image_generation_prompt = model.generate_content(f'''
                        You are a model that is spezialized in creating image generation prompts based on a given text.
                        The prompt should be very descriptive and as detailed as possible for the ai to understand.
                        This is the text: {segment}. Do not add any maps or text to the images whatsoever.
                    ''')
                    image_gen_prompts.append(image_generation_prompt)

                print(image_gen_prompts)
                 
                for image_gen_prompt in image_gen_prompts:
                    print(segment)
                    if image_gen_prompt != "":
                         response = client.images.generate(
                         prompt=f"{image_gen_prompt} Do not add any maps or text to the images whatsoever.",
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

 
                return render(request, 'dashboard.html', {'script': script_text, 'segments': full_segmented_text, 'edited_segments': segments})
        else:
            return render(request, 'dashboard.html', {'error': 'Please fill all fields'})
     else:
        return render(request, 'dashboard.html')





