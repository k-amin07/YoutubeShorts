from PIL import Image

import json
import subprocess
import pytesseract
import re
import pickle
import difflib
import os


ps = subprocess.Popen(('ls', '-1', './frames'), stdout=subprocess.PIPE)
count = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
count = int(count.strip())

digits = len(str(count))

starting_frame = 1  # can be adjusted to start from a different frame

# These are the values that stats for nerds displays.
key_list = ['DEVICE', 'CPN', 'VIDEO ID', 'VIDEO FORMAT', 'AUDIO FORMAT', 'VOLUME/NORMALIZED',
            'BANDWIDTH', 'READAHEAD', 'VIEWPORT', 'DROPPED FRAMES', 'MYSTERY TEXT', 'SPONSOR/AD']

valid_chars_for_id = list(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

# Adjust according to specific bounding boxes:
# stored as: left, top, right, bottom
device_bb = [70, 141, 256, 178]
cpn_bb = [50, 175, 319, 205]
video_id_bb = [86, 199, 234, 236]
video_format_bb = [131, 232, 355, 261]
audio_format_bb = [130, 254, 403, 290]
volume_normalized_bb = [198, 288, 522, 318]
bandwidth_bb = [300, 313, 422, 347]
readahead_bb = [299, 345, 394, 372]
viewport_bb = [93, 373, 292, 399]
dropped_frames_bb = [153, 400, 258, 430]
mystery_text_bb = [129, 423, 218, 457]

sponsor_bb = [4, 844, 338, 950]

bounding_boxes = [device_bb, cpn_bb, video_id_bb, video_format_bb, audio_format_bb, volume_normalized_bb,
                  bandwidth_bb, readahead_bb, viewport_bb, dropped_frames_bb, mystery_text_bb, sponsor_bb]

# Define key list and bounding boxes
# Your existing key_list and bounding_boxes definitions here...


all_data = {}
for i in range(starting_frame, count + 1, 4):
    print("Processing Frames {} to {}...".format(i, i + 3))
    exception_count = 0
    for j in range(4):
        frame_number = i + j
        if frame_number > count:
            break

        # Construct frame name
        # Adjust according to the actual naming convention
        name = 'frame{:04d}'.format(frame_number)

        image_path = os.path.join('./frames', '{}.jpg'.format(name))
        if not os.path.exists(image_path):
            continue

        image = Image.open(image_path)
        # custom_config = r'--psm 6 --oem 2 -l eng'     # for tesseract legacy engine
        custom_config = r'--psm 6 -l eng'
        vid_data = {}

        try:
            for box in range(len(bounding_boxes)):
                bb = bounding_boxes[box]
                if any(coordinate < 0 for coordinate in bb) or any(
                        coordinate > max(image.size) for coordinate in bb):
                    # Skip if bounding box coordinates are invalid
                    continue

                cropped_image = image.crop((bb[0], bb[1], bb[2], bb[3]))
                cropped_image = cropped_image.convert('L')
                cropped_image = cropped_image.point(lambda p: p > 128 and 255)

                image_text = pytesseract.image_to_string(
                    cropped_image, config=custom_config)

                if image_text.strip() and box != 12:  # For all cases besides sponsor
                    key = key_list[box]
                    vid_data[key] = image_text.strip()
                    if (key == "VIDEO ID"):
                        # TO DO: Replace this with the last example in Tesseract Documentation.
                        # OCR confuses 7 with ? in frame0002 for example. Get closest matches does not pick that up, even with very low cutoff
                        # Last example here may help https://github.com/sirfz/tesserocr?tab=readme-ov-file#advanced-api-examples
                        image_text = ''.join(map(lambda x: difflib.get_close_matches(
                            x, valid_chars_for_id, cutoff=0.1)[0], vid_data[key]))
                    print(image_text.strip())

                elif image_text.strip() and box == 12:  # For sponsor case
                    #check if 'Sponsored' is in the text
                    if 'Sponsored' in image_text:
                        vid_data[key] = 'Yes'
                    else:
                        vid_data[key] = 'No'

        except Exception as e:
            exception_count += 1
            if exception_count == 4:
                print('Exception:', name)
                print('Exception:', e)
                exception_count = 0

        if 'VIDEO ID' in vid_data:
            vid_id = vid_data['VIDEO ID'].split(' ')[0]
            if vid_id not in all_data:
                all_data[vid_id] = []
            all_data[vid_id].append(vid_data)

    if i % 100 == 0:
        with open('stats_for_nerds.pkl', 'wb') as handle:
            pickle.dump(all_data, handle)

print(json.dumps(all_data, indent=4))

with open('./stats/sample_stats.pkl', 'wb') as handle:
    pickle.dump(all_data, handle)
