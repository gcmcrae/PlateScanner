import cv2
import os

# Load the image.
image = cv2.imread('C:/Users/gcmcr/OneDrive/Pictures/image202.jpg')

# Convert to grayscale to make it easier to read.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to binarize the image.
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
binary = cv2.medianBlur(binary, 3)

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Specify the Tesseract executable path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Perform OCR on the preprocessed image
text = pytesseract.image_to_string(binary)

# Print the extracted text.
# print("Extracted Text:", text)

# Get bounding boxes for detected text.
h, w, _ = image.shape
boxes = pytesseract.image_to_boxes(binary)

for box in boxes.splitlines():
    b = box.split()
    x, y, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.rectangle(image, (x, h - y), (x2, h - y2), (0, 255, 0), 2)

# Show the image with bounding boxes.
cv2.imshow("Detected Text", image)
cv2.waitKey(0)
cv2.destroyAllWindows() 

def extract_room_number(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image!")
        return None

    # Convert image to grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Thresholding for better text isolation.
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Apply median blur to reduce noise
    binary = cv2.medianBlur(binary, 3)

    # **Crop Region of Interest (ROI)**
    # Assuming the text is roughly in the center of the image:
    height, width = binary.shape
    x_start, y_start = int(0.1 * width), int(0.2 * height)
    x_end, y_end = int(0.9 * width), int(0.8 * height)
    roi = binary[y_start:y_end, x_start:x_end]

    # Perform OCR on the cropped region with configuration.
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(roi, config=custom_config)

    # Display the cropped ROI for debugging.
    cv2.imshow("Cropped ROI", roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # **Draw a rectangle around the ROI on the original image**
    cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

    # Show the original image with the rectangle.
    cv2.imshow("Room Plate with ROI", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return text.strip()

# Example of usage.
room_number = extract_room_number("C:/Users/gcmcr/OneDrive/Pictures/image202.jpg")
print("Room Number:", room_number)
