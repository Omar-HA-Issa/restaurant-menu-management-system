import fitz  # PyMuPDF
from google.cloud import vision
from google.oauth2 import service_account
import io
from PIL import Image
import os

def extract_text_from_pdf(pdf_file_path):
    """Extract text from a PDF file using PyMuPDF."""
    try:
        # Verify the file exists
        if not os.path.exists(pdf_file_path):
            print(f"File not found: {pdf_file_path}")
            return None
            
        # Print file info for debugging
        print(f"Attempting to open PDF file: {pdf_file_path}")
        
        # Open the PDF file using PyMuPDF
        doc = fitz.open(pdf_file_path)
        text = []
        
        # Extract text from each page
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page_text = page.get_text("text").strip()
            if page_text:  # Only add non-empty pages
                text.append(page_text)
        
        # Close the document
        doc.close()
        
        # Combine all text with proper spacing
        combined_text = "\n\n".join(text).strip()
        
        # Debug print
        print("Extracted text length:", len(combined_text))
        print("First 200 characters of extracted text:", combined_text[:200])
        
        if not combined_text:
            print("No text extracted from PDF")
            return None
            
        return combined_text
        
    except fitz.FileDataError as e:
        print(f"PDF file is corrupted or invalid: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while extracting text from the PDF: {type(e).__name__}: {e}")
        return None

def extract_text_from_image(image_path):
    """Extract text from an image using Google Cloud Vision API."""
    try:
        # Verify the file exists
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return None
            
        # Set up credentials for Google Cloud Vision API
        credentials_path = r"C:\Users\User\Downloads\output-results_output-1-to-1.json"
        if not os.path.exists(credentials_path):
            print("Google Cloud credentials file not found")
            return None
            
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = vision.ImageAnnotatorClient(credentials=credentials)
        
        # Read image into memory
        with open(image_path, "rb") as image_file:
            content = image_file.read()
            
        # Create image object
        image = vision.Image(content=content)
        
        # Perform text detection
        response = client.text_detection(image=image)
        
        # Check for errors
        if response.error.message:
            print(f"Error from Google Vision API: {response.error.message}")
            return None
            
        texts = response.text_annotations
        if texts:
            extracted_text = texts[0].description.strip()
            print("Extracted text length from image:", len(extracted_text))
            print("First 200 characters of extracted text from image:", extracted_text[:200])
            return extracted_text
        else:
            print("No text found in the image")
            return None
            
    except Exception as e:
        print(f"An error occurred while extracting text from the image: {type(e).__name__}: {e}")
        return None

def save_text_to_file(text, output_file_path):
    """Save extracted text to a file."""
    try:
        if not text:
            print("No text to save")
            return False
            
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Text successfully saved to {output_file_path}")
        return True
        
    except Exception as e:
        print(f"An error occurred while saving the text: {type(e).__name__}: {e}")
        return False