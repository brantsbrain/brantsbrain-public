import requests, json
from creds import token
from pathlib import Path

# Define the URL and headers
url = 'https://image.groupme.com/pictures'
headers = {
    'X-Access-Token': token,
}

# Define image formats you want to process
image_formats = ['.jpg', '.jpeg', '.png', '.gif']

# Get all image files in the current directory
current_directory = Path('.')
image_files = [f for f in current_directory.iterdir() if f.suffix.lower() in image_formats]
image_dict = {}

# Loop through each image and upload
for image_path in image_files:
    # Set the appropriate content type for each image format
    content_type = f'image/{image_path.suffix[1:]}'
    headers['Content-Type'] = content_type

    with open(image_path, 'rb') as img_file:
        response = requests.post(url, headers=headers, data=img_file)
    
    # Check and log the response for each image
    print(f"Uploading {image_path.name}: {response.status_code}")
    if response.status_code == 200:
        print(f"Success: {response.json()}")
        image_dict[image_path.name] = response.json()["payload"]["url"]
    else:
        print(f"Failed to upload {image_path.name}")

with open("imageresults.json", "w") as outfile:
    json.dump(image_dict, outfile)