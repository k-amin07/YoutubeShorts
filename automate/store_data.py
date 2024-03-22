import os
import xml.etree.ElementTree as ET
from parse import parse_xml_to_csv,remove_trailing_message
import csv
import argparse


headers = ['Device', 'CPN', 'Video ID' , 'Video format', 'Resolution', 'Frame Rate', 'Audio format', 'Volume/Normalized', 'Bandwidth', 'Readahead', 'Viewport', 'Dropped frames' , 'Mystery Text']


def process_folder(input_folder, output_file):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", help = "File Name Prefix")
    args = parser.parse_args()

    input_folder = "../data/stats/{}/".format(args.prefix)
    output_file = "../data/processed/output.csv"

    if(not os.path.isfile(output_file)):
        # Write column headers to the output file
        with open(output_file, "a+", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
    
    # Process the folder
    process_folder(input_folder, output_file)

