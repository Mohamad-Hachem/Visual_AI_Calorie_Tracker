from PIL import Image
import os
import base64
import io

def encode_image_to_base64(image_path_or_pil):
    """
        # This function converts an image into a special text format (called base64)
        # This is used if we want to send an image to OpenAI’s API

        # This function works with two types of inputs: 
        # (1) A file path: a string that tells the function where the image is stored on your computer.
        # (2) An image object: a photo already loaded in memory using the PIL library (Python Imaging Library).
    """
    if isinstance(image_path_or_pil, str):  # If it's a file path
        # Check if the file exists
        if not os.path.exists(image_path_or_pil):
            raise FileNotFoundError(f"Image file not found at: {image_path_or_pil}")
        with open(image_path_or_pil, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
            
    elif isinstance(image_path_or_pil, Image.Image):  # If it's a PIL Image object
        buffer = io.BytesIO()
        image_format = image_path_or_pil.format or "JPEG"  # Default to JPEG if format unknown
        image_path_or_pil.save(buffer, format=image_format)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    else:
        raise ValueError("Input must be a file path (str) or a PIL Image object.")