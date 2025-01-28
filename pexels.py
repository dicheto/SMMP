# Import API class from pexels_api package
from pexels_api import API
import requests
# Type your Pexels API
PEXELS_API_KEY = 't5kT5w0zmVw0AdR172RMGlpu128peM0fBMRVJTCHybydoKtj7oXhNfi0'
# Create API object
api = API(PEXELS_API_KEY)
# Search five 'kitten' photos
api.search('bulgaria', page=1, results_per_page=1)
# Get photo entries
photos = api.get_entries()
# Loop the five photos
for photo in photos:
  # Print photographer
  print('Photographer: ', photo.photographer)
  # Print url
  print('Photo url: ', photo.url)
  # Print original size url
  print('Photo original size: ', photo.original)



def download_image(image_url, save_path):
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Write the content of the response to a file
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded and saved to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# URL of the image
image_url = "https://images.pexels.com/photos/1444321/pexels-photo-1444321.jpeg"

# Path where you want to save the image
save_path = "C:/Users/Radostin Galev/Downloads/pexels-photo-1444321.jpeg"

# Call the function to download the image
download_image(image_url, save_path)
