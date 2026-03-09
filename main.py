import ssl
import cv2
from ultralytics import YOLO
import easyocr
import csv
from datetime import datetime

# 1. Mac SSL Fix
ssl._create_default_https_context = ssl._create_unverified_context

# 2. Setup OCR and Model
print("Initializing System...")
reader = easyocr.Reader(['en'])
model = YOLO('yolov8n.pt') 

# 3. Run Detection on your file
image_path = 'test.jpg'
results = model(image_path)

# Prepare to save data to a CSV file
with open('plate_log.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    # If file is empty, you could write a header: writer.writerow(["Timestamp", "Plate Number"])

    for result in results:
        img = cv2.imread(image_path)
        
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Crop the detected area
            crop = img[y1:y2, x1:x2]
            
            # Run OCR on the crop
            ocr_results = reader.readtext(crop)
            
            for (bbox, text, prob) in ocr_results:
                # Basic cleaning: Plates usually have at least 5 characters
                if len(text) > 4 and prob > 0.20:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] FOUND PLATE: {text}")
                    
                    # Save to CSV
                    writer.writerow([timestamp, text])

    result.show()