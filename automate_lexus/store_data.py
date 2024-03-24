import os
import xml.etree.ElementTree as ET
from parse import parse_xml_to_csv,remove_trailing_message
import csv

headers = ['Device', 'CPN', 'Video ID' , 'Video format', 'Audio format', 'Volume/Normalized', 'Bandwidth', 'Readahead', 'Viewport', 'Dropped frames' , 'Mystery Text']


def process_folder(input_folder, output_file):
    # Initialize an empty data object to retrieve column headers
    column_headers = headers

    # Write column headers to the output file
    with open(output_file, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            # Get the full path of the XML file
            xml_file = os.path.join(input_folder, filename)
            
            remove_trailing_message(xml_file)
            # Parse XML file and get CSV record
            csv_record = parse_xml_to_csv(xml_file)
            
            # Append CSV record to the output file
            with open(output_file, "a") as f:
                f.write(csv_record + "\n")


if __name__ == "__main__":
    input_folder = "./data/stats"
    output_file = "output.csv"
    
    # Process the folder
    process_folder(input_folder, output_file)

