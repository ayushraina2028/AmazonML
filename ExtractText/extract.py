import os
import easyocr
import pandas as pd
from colorama import Fore, Style, init
import random
from PIL import Image

# Use multi-threading to improve performance
import multiprocessing as mp
mp.set_start_method('spawn', force=True)

# Directory to save grayscale images
grayscale_folder = 'grayscale_images/'
os.makedirs(grayscale_folder, exist_ok=True)

# Function to convert image to grayscale
def convert_to_grayscale(img_path, grayscale_path):
    with Image.open(img_path) as img:
        grayscale_img = img.convert('L')
        grayscale_img.save(grayscale_path)

# Initialize colorama
init(autoreset=True)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])  # You can add more languages if needed

# Directory containing images
image_folder = '../66e31d6ee96cd_student_resource_3/student_resource/train_images/'

# Initialize an empty list to store OCR results
ocr_results = []

# Initialize a counter
count = 0
max_images = 50  # Limit the processing to 10 images

# Supported image formats
supported_formats = [".jpg", ".png"]

# Iterate through the images in the folder
for filename in random.sample(os.listdir(image_folder), k=max_images):
    # Check for supported file formats
    if any(filename.endswith(ext) for ext in supported_formats):
        # Full path to the image
        img_path = os.path.join(image_folder, filename)
        grayscale_path = os.path.join(grayscale_folder, filename)

        convert_to_grayscale(img_path, grayscale_path)
        
        try:
            # Perform OCR on the image using EasyOCR
            results = reader.readtext(grayscale_path,rotation_info=[90,270],link_threshold=0.15,y_ths=.8,batch_size=12)
            
            # Prepare lists to aggregate data for each image
            texts = []
            bounding_boxes = []
            confidences = []
            
            # Process each result (bounding box, text, confidence)
            for res in results:
                bbox, text, confidence = res
                
                texts.append(text)
                bounding_boxes.append(bbox)
                confidences.append(confidence)
            
            # Append the aggregated data for the image to the list
            ocr_results.append({
                "filename": filename,
                "ocr_text": " | ".join(texts),  # Concatenate all text with a separator
                "bounding_boxes": str(bounding_boxes),  # Store bounding boxes as a string
                "confidences": str(confidences)  # Store confidence scores as a string
            })
            
            # Increment the counter
            count += 1
            print(f"{Fore.GREEN}Processed {count} images: {Fore.CYAN}{filename}")
        
        except Exception as e:
            # Handle any errors during processing
            print(f"{Fore.RED}Error processing {filename}: {Fore.YELLOW}{str(e)}")
            continue



# Create a pandas DataFrame from the list
df = pd.DataFrame(ocr_results)

# Save the dataframe to a CSV file (optional)
df.to_csv('easyocr_results_100.csv', index=False)

# Display the first few rows of the DataFrame
print(df.head())
