import json
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from pdf_to_image import pdf_to_images
import numpy as np
import cv2

# Initialize TrOCR model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-handwritten")

def segment_lines(image):
    """
    Takes a PIL Image, uses OpenCV to detect lines, and returns a list of PIL Images (one per line).
    """
    # 1. Convert PIL image to OpenCV format (NumPy array, BGR)
    open_cv_image = np.array(image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    # 2. Convert to grayscale
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # 3. Threshold (invert if needed)
    #    - THRESH_BINARY_INV is used here because dark text on a light background
    #      often works better for line detection.
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 4. Morphological dilation to merge text into horizontal lines
    #    - The kernel size can be tuned depending on your text size and spacing.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (gray.shape[1] // 40, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # 5. Find contours of these text regions
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 6. Get bounding boxes and sort them by y-coordinate (top to bottom)
    line_images = []
    bounding_boxes = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # (Optional) Filter out boxes that are too small or too large
        if h < 10 or w < 10:
            continue
        bounding_boxes.append((x, y, w, h))

    bounding_boxes.sort(key=lambda b: b[1])  # Sort by the 'y' value

    # 7. Crop each region from the original PIL image
    for (x, y, w, h) in bounding_boxes:
        cropped_pil = image.crop((x, y, x + w, y + h))
        line_images.append(cropped_pil)

    return line_images


def extract_text_from_image(image):
    """Extract handwritten text using TrOCR after ensuring the image is in RGB mode."""
    # Check if image is in grayscale (2D) and convert it to RGB (3D)
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return text

def extract_text_from_pdf(pdf_path):
    """Convert PDF pages to images and extract handwritten text"""
    images = pdf_to_images(pdf_path)
    extracted_data = {}

    for i, image in enumerate(images):
        line_images = segment_lines(image)
        page_texts = []

        for line_image in line_images:
            line_text = extract_text_from_image(line_image)
            page_texts.append(line_text)
            extracted_data[f"page_{i + 1}"] = "\n".join(page_texts)
    return extracted_data

def save_to_json(data, output_path="output.json"):
    """Save extracted text to a JSON file"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Run the extraction process
pdf_path = "r.pdf"  # Replace with your PDF file
extracted_text = extract_text_from_pdf(pdf_path)
save_to_json(extracted_text, "output.json")

print("Text extraction complete. Saved to output.json")
