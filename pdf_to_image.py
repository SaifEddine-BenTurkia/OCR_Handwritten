import fitz  # PyMuPDFdef preprocess_image(image):
from PIL import Image,ImageOps
import io

def pdf_to_images(pdf):
    # Open the PDF file
    pdf_document = fitz.open(pdf)
    images = []

    # Iterate through each page
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        
        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Convert image bytes into a PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            image = ImageOps.grayscale(image)
            images.append(image)  # Store PIL Image object in list

    return images  # List of PIL Image objects

# Example Usage:
# images = pdf_to_images("example.pdf")
# images[0].show()  # Display the first image
