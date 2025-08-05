import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()  # this loads variables from .env into environment

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
)

folder_path = r"C:\Users\louis\OneDrive\Desktop\Resin Treasures\store\static\images"


for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        file_path = os.path.join(folder_path, filename)
        print(f"Uploading {filename} ...")
        response = cloudinary.uploader.upload(file_path, folder="resin_treasures_images")
        print(f"Uploaded to {response['secure_url']}")
