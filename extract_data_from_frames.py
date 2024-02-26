# use python 3.7+ as dict keys are not guaranteed to preserve order in older python versions


from PIL import Image
import subprocess

import pytesseract
import re
import pickle
import difflib

ps = subprocess.Popen(('ls','-1','./frames'),stdout = subprocess.PIPE)
count = subprocess.check_output(('wc','-l'),stdin=ps.stdout)
count = int(count.strip())

digits = len(str(count))

starting_frame = 52
# These are the values that stats for nerds displays. 
key_list = ['DEVICE', 'CPN', 'VIDEO ID', 'VIDEO FORMAT', 'AUDIO FORMAT', 'VOLUME/NORMALIZED', 'BANDWIDTH', 'READAHEAD', 'VIEWPORT', 'DROPPED FRAMES', 'MYSTERY TEXT']

all_data = {}
for i in range(starting_frame,count+1,4):
    exception_count = 0
    for j in range(4): 
        frame_number = i+j
        print("Processing Frame {}...".format(frame_number))
        padding = ''.join(["0" for _ in range(digits-len(str(frame_number)))])
        name = 'frame' + padding + str(i)
        
        image = Image.open('./frames/%s.jpg' % name)
        image = image.convert('L')
        image = image.point(lambda p: p>128 and 255)
        custom_config = r'--psm 6 --oem 2 -l eng'

        image_text = pytesseract.image_to_string(image,config=custom_config)

        lines = list(filter(lambda x: len(x)!=0, image_text.split('\n')))    
    
        vid_data = {}
    
        if('Sponsored' in image_text):
            vid_data['IS_AD'] = True
        else:
            vid_data['IS_AD'] = False
        for line in lines:
            if(':' not in line and ';' not in line):
                continue
            
            data = line.strip().split(':')
            if(data[0] == line.strip() and ';' in data[0]):
                data = data[0].split(';')
            try:
                key,value = data[0].strip().upper(), data[-1].strip()
                closest_keys = difflib.get_close_matches(key,key_list)
                if(not len(closest_keys)):
                    continue
                key = closest_keys[0]
                vid_data[key] = value
                if(key == 'MYSTERY TEXT'):
                    break
            except Exception as e:
                exception_count += 1
                # we must get data from at least one frame in a given second
                if(exception_count == 4):
                    print(name)
                    print(e)
                    raise e
        try:
            vid_data['VIDEO ID'] = vid_data['VIDEO ID'].replace('[X]','').strip()
            vid_data['RESOLUTION'], vid_data['FRAME_RATE'] = re.findall(r'(\d+x\d+)@(\d+)',vid_data['VIDEO FORMAT'])[0]
            print(vid_data['BANDWIDTH'])
            bandwidth = re.findall(r'([-+]?\d*\.?\d+)',vid_data['BANDWIDTH'])   
            readahead = re.findall(r'([-+]?\d*\.?\d+)',vid_data['READAHEAD'])
            if(len(bandwidth)):
                bandwidth = bandwidth[0]
                if(len(vid_data['BANDWIDTH'].split(bandwidth))):
                   bandwidth += vid_data['BANDWIDTH'].split(bandwidth)[-1].strip()
                print(bandwidth)
            if(len(readahead)):
                readahead = readahead[0]
                if(len(readahead.split(' '))):
                    readahead = readahead.split(' ')[-1]
            vid_data['BANDWIDTH'] = bandwidth
            vid_data['READAHEAD'] = readahead
        except Exception as e:
            exception_count += 1
            if(exception_count == 4):
                #raise(e)
                print(name)
                print(e)
                exception_count = 0
        if('VIDEO ID' in vid_data):
            vid_id = vid_data['VIDEO ID'].split(' ')[0]
            if(vid_id not in all_data):
                all_data[vid_id] = []
            all_data[vid_id].append(vid_data)
    if(i%100 == 0):
        with open('stats_for_nerds.pkl', 'wb') as handle:
            pickle.dump(all_data,handle)

print(all_data)

with open('stats_for_nerds.pkl', 'wb') as handle:
    pickle.dump(all_data,handle)

