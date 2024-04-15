import pandas as pd
from scipy.spatial import distance

# Function to calculate the Hamming distance between two strings
def hamming_distance(s1, s2):
    # Ensure both strings are the same length
    if len(s1) != len(s2):
        l = min(len(s1), len(s2))
        s1, s2 = s1[:l], s2[:l]
    return distance.hamming(list(s1), list(s2))

# Function to assign Short Numbers to OCR data based on the most similar Video ID from ADB data
def assign_short_number(adb_data, ocr_data):
    # Map to store the best match for each OCR Short ID
    short_number_map = {}
    for short_id in ocr_data['Short ID'].unique():
        min_distance = float('inf')
        best_match = None
        for video_id in adb_data['Video ID'].unique():
            dist = hamming_distance(short_id, video_id)
            if dist < min_distance:
                min_distance = dist
                best_match = video_id
        # Assign the Short Number from the best match
        if best_match:
            short_number = adb_data.loc[adb_data['Video ID'] == best_match, 'Short Number'].values[0]
            short_number_map[short_id] = short_number
    ocr_data['Short Number'] = ocr_data['Short ID'].map(short_number_map)
    return ocr_data

# Load the CSV files
adb_data = pd.read_csv('pak_adb.csv')
ocr_data = pd.read_csv('pak_OCR.csv')

# Assign a unique short number to each unique Video ID in the ADB data
unique_video_ids = adb_data['Video ID'].unique()
video_id_to_short_number = {vid: idx + 1 for idx, vid in enumerate(unique_video_ids)}
adb_data['Short Number'] = adb_data['Video ID'].map(video_id_to_short_number)

# Apply the function to assign short numbers
ocr_data_assigned = assign_short_number(adb_data, ocr_data)

# Remove duplicates in the OCR data
ocr_data_cleaned = ocr_data_assigned.drop_duplicates(subset=['Time (s)', 'Short ID', 'Short Number'])

# Save the cleaned and updated OCR data to a new CSV file
ocr_data_cleaned.to_csv('updated_ocr_data.csv', index=False)
