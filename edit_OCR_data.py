import csv
from Levenshtein import distance

#ADB pauses the short to extract data. This code removes duplicates from exracted OCR data based on bandwidth and readahead values.
#this means that we ignore the records extracted when the short was paused

def are_similar(id1, id2, threshold=3):
    """
    Check if two IDs are similar based on Levenshtein distance.
    """
    return distance(id1, id2) <= threshold

def remove_duplicates(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        
        if len(rows) < 2:
            print("No duplicates to remove.")
            return
        
        clean_rows = [rows[0]]  # Keep the first row
        
        for i in range(1, len(rows)):
            prev_row = clean_rows[-1]
            current_row = rows[i]
            
            if (prev_row['Bandwidth'] == current_row['Bandwidth'] and
                prev_row['Readahead (s)'] == current_row['Readahead (s)']):
                if are_similar(prev_row['Short ID'], current_row['Short ID']):
                    current_row['Short Number'] = prev_row['Short Number']
                    
            clean_rows.append(current_row)
        
        if len(clean_rows) == len(rows):
            print("No duplicates found.")
        else:
            print(f"Removed {len(rows) - len(clean_rows)} duplicates.")
        
        # Write back to CSV
        with open(csv_file, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(clean_rows)

# Example usage:
csv_file = 'OCR_data.csv'  # Replace with your CSV file path
remove_duplicates(csv_file)