import xml.etree.ElementTree as ET


#defining the column headers here
headers = ['Device', 'CPN', 'Video ID' , 'Video format', 'Audio format', 'Volume/Normalized', 'Bandwidth', 'Readahead', 'Viewport', 'Dropped frames' , 'Mystery Text']
resources = ['device_info','cpn','video_id','video_format','audio_format','volume','bandwidth_estimate','readahead', 'viewport', 'dropped_frames','mystery_text']

class data:
    def __init__(self,device_info,cpn,video_id,video_format,audio_format,volume,bandwidth_estimate,readahead,viewport,dropped_frames,mystery_text):
        self.device_info = device_info
        self.cpn = cpn
        self.video_id = video_id
        self.video_format = video_format
        self.audio_format = audio_format
        self.volume = volume
        self.bandwidth_estimate = bandwidth_estimate
        self.readahead = readahead
        self.viewport = viewport
        self.dropped_frames = dropped_frames
        self.mystery_text = mystery_text

    def add_value(self,attribute,value):
        if hasattr(self, attribute):
            # Set the attribute to the new value
            setattr(self, attribute, value)
            print(f"Attribute '{attribute}' updated to '{value}'")
        else:
            print(f"Attribute '{attribute}' does not exist in the class")

    def to_csv_record(self):
    # Get class attributes in the order they are defined
        attribute_values = [str(getattr(self, attr)) for attr in ['device_info', 'cpn', 'video_id', 'video_format', 'audio_format', 'volume', 'bandwidth_estimate', 'readahead', 'viewport', 'dropped_frames', 'mystery_text']]
    
    # Construct CSV record with only attribute values
        csv_record = ','.join(attribute_values)

        return csv_record




def parse_xml_to_csv(xml_file):

    # Initialize an empty data object
    current_data = data('', '', '', '', '', '', '', '', '', '', '')

    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Iterate over relevant nodes
    for node in root.iter():
        if (node.attrib.get('resource-id') and (node.attrib.get('text'))):
            parts = node.attrib.get('resource-id').split('/')
            # Get the last part after the last '/'
            last_part = parts[-1]
            # Extract the letters after the last '/'
            param = last_part[last_part.rfind('/') + 1:]
            if (param in resources):
                current_data.add_value(param, node.attrib.get('text'))

    # Generate CSV record
    csv_record = current_data.to_csv_record()
    
    return csv_record

def remove_trailing_message(xml_file):
    # Read the XML file
    with open(xml_file, 'r') as file:
        xml_data = file.read()
        modified_xml = xml_data

    # Remove the trailing message
    if 'UI hierchary dumped to: /dev/tty' in xml_data:
        modified_xml = xml_data.replace('UI hierchary dumped to: /dev/tty', '')


    # Write the modified XML back to the file
    with open(xml_file, 'w') as file:
        file.write(modified_xml)



