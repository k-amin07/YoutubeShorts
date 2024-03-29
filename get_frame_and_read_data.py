# this file extracts 10 fps from the video, crops sections for bandwidth and readahead, reads these using OCR and saves result in csv
# readings are saved in dictionary: {time: [bandwidth, readahead, sponsor]}
import cv2
import pytesseract
import csv
import numpy as np
import os

# Bounding boxes for relavant data fields (change based on your device)
# stored as: left, top, right, bottom
id_bb = [86, 204, 236, 236]
bandwidth_bb = [297, 315, 422, 346]
readahead_bb = [296, 342, 382, 373]
sponsored_bb = [55, 844, 599, 1056]
dropped_bb = [157, 399, 238, 428]

bounding_boxes = [id_bb, bandwidth_bb, readahead_bb, dropped_bb, sponsored_bb]

# Path to the video file (change based on your file path)
video_path = '../../Downloads/cropped.mp4'

# Custom configuration
custom_config = r'--psm 6 -l eng'
# custom_config = r'--psm 6 --oem 2 -l eng'     # for tesseract legacy engine

# Open the video file
cap = cv2.VideoCapture(video_path)

# Calculate frames per second (FPS) and total number of frames
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate the frame interval to get approximately 10 frames per second (can adjust to get more or less frames)
frame_interval = int(fps / 10)

# Initialize variables
current_frame = 0
all_data = {}
prev_readahead = "0" #holds previous readahead value
prev_id = "" #holds previous id value
short_num = 0 #short number -> which short is being viewed

# Function to extract text from image using OCR
def extract_text_from_image(image, bb, i, prev_readahead):
    cropped_image = image[bb[1]:bb[3], bb[0]:bb[2]]
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(
        gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    text = pytesseract.image_to_string(threshold_image, config=custom_config)

    # this is for readahead as OCR often misreads 's' as '$', '8', or '¥' and often doesn't read the decimal 
    # in readahead either the number is '0.xyz' or 1.xy' where x, y, z are digits
    #so accordingly we split the text and remove the potentially misread leaving just the numeric seconds reading
    if i == 2:
        if text[0] == '0':
            if text[1] == '.':
                text = text[:5]
            else:
                text = text[0] + '.' + text[1:4]
            
            if len(text) > 5:
                text = text[:5]
        else:
            if '.' in text:
                text = text[:4]
            else:
                try:
                    prev = float(prev_readahead)
                    if prev < 10:
                        text = text[0] + '.' + text[1:3]
                    else:
                        text = text[0:2] + '.' + text[2:4]
                except:
                    pass
            if len(text) > 4:
                text = text[:4]
    #OCR often misreads 'B' as '8', '4' as 'A', 'O' as '0' and 'o' as '0'
    if i==2 or i==1:
        text = text.replace('B', '8')
        text = text.replace('A', '4')
        text = text.replace('O', '0')
        text = text.replace('o', '0')

    if i == 4: #sponsored check
        if "sponsored" in text.lower() or "install" in text.lower():
            return "Sponsored"
        else:
            return "Not Sponsored"
            
    return text.strip()

#Function checks if the id is similar to previous id or not
def check_id(current, prev_id, short_num):

    similarity_threshold = 0.8  #threshold for similarity

    #if current is empty or only has spaces, return short_num
    if not current or current.isspace():
        return short_num
    
    #remove spaces in current and prev_id
    current = current.replace(' ', '')
    prev_id = prev_id.replace(' ', '')
    
    distance = 0
    if len(current) == len(prev_id):
        distance = sum(c1 != c2 for c1, c2 in zip(current, prev_id))
    else:
        distance = max(len(current), len(prev_id))
    # Calculate the similarity ratio
    similarity = (max(len(current), len(prev_id)) - distance) / max(len(current), len(prev_id))
  
    # If similarity is above threshold -> same short being viewed
    if similarity >= similarity_threshold:
        return short_num
    
    return short_num + 1


# Iterate through video frames
while current_frame < total_frames:
    # Set frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

    # Read the frame
    ret, frame = cap.read()

    # Check if frame was read successfully
    if not ret:
        break

    # Get time in seconds
    current_time_sec = current_frame / fps

    # Check if current frame is within the interval for desired FPS
    if current_frame % frame_interval == 0:
        readings = []
        # Iterate through bounding boxes
        for i, bbox in enumerate(bounding_boxes):
            # Extract text from image region defined by bounding box
            text = extract_text_from_image(frame, bbox, i, prev_readahead)
            if i == 0:
                short_num = check_id(text, prev_id, short_num)
                prev_id = text
                readings.append(short_num)

            if i == 2:
                prev_readahead = text
            print(text)

            readings.append(text)

        # Store readings in dictionary with time as key
        all_data[current_time_sec] = readings

    # Move to next frame
    current_frame += frame_interval

# Release the video capture object
cap.release()

# Save the data to a CSV file
csv_file_path = 'OCR_data.csv'
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time (s)', 'Short Number', 'Short ID' , 'Bandwidth', 'Readahead (s)', 'Dropped Frames', 'Sponsored'])
    for time, readings in all_data.items():
        writer.writerow([time] + readings)

print(f"Data saved to {csv_file_path}")
