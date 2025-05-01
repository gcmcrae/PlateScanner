import cv2

# Load the image (replace 'room_plate.jpg' with your image path)
image = cv2.imread('room_plate.jpg')

# Display the image
cv2.imshow("Room Plate", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to binarize the image
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Optional: Denoise the image
binary = cv2.medianBlur(binary, 3)

# Show the preprocessed image
cv2.imshow("Preprocessed", binary)
cv2.waitKey(0)
cv2.destroyAllWindows()

import pytesseract

# Specify the Tesseract executable path if needed (Windows only)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Perform OCR on the preprocessed image
text = pytesseract.image_to_string(binary)

# Print the extracted text
print("Extracted Text:", text)

# Get bounding boxes for detected text
h, w, _ = image.shape
boxes = pytesseract.image_to_boxes(binary)

for box in boxes.splitlines():
    b = box.split()
    x, y, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.rectangle(image, (x, h - y), (x2, h - y2), (0, 255, 0), 2)

# Show the image with bounding boxes
cv2.imshow("Detected Text", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import pytesseract

def extract_room_number(image_path):
    # Load image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    binary = cv2.medianBlur(binary, 3)

    # Perform OCR
    text = pytesseract.image_to_string(binary)
    
    # Get bounding boxes
    h, w, _ = image.shape
    boxes = pytesseract.image_to_boxes(binary)
    for box in boxes.splitlines():
        b = box.split()
        x, y, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(image, (x, h - y), (x2, h - y2), (0, 255, 0), 2)

    # Show the image
    cv2.imshow("Room Plate", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return text

# Example usage
room_number = extract_room_number("room_plate.jpg")
print("Room Number:", room_number)
