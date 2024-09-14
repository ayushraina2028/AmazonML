import easyocr
import re

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])  # specify the language

def extract_weight_from_image(image_path):
    # Perform OCR on the image
    result = reader.readtext(image_path, detail=0)

    # Combine all the detected text
    extracted_text = ' '.join(result)
    
    # Use regex to extract weight information (e.g., 1.5 kg, 500 g)
    weight_pattern = re.compile(r'\d+(\.\d+)?\s*(kg|g|lb|oz)', re.IGNORECASE)
    weights = weight_pattern.findall(extracted_text)
    
    if weights:
        return weights[0]  # return the first match (if multiple)
    else:
        return "Weight not found"

# Example usage
image_path = '71Xmkf5qsHL.jpg'
weight = extract_weight_from_image(image_path)
print(f'Extracted weight: {weight}')
