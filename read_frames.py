import cv2

vidcap = cv2.VideoCapture('./2G.mp4')

count = 0

success,image = vidcap.read()

# First 16 seconds in my recording were janky, skipping those.
while(count < 16*60 and success):
    success,image = vidcap.read()
    count += 1

count = 1
while(success):
    success,image = vidcap.read()
    digits = len(str(count))
    padding = ''.join(["0" for _ in range(4-digits)])
    name = padding + str(count)
    cv2.imwrite("./frames/frame%s.jpg" % name, image)
    
    # extract 4 frames from each second
    # verify the recorded video fps in vlc and adjust the value if it is less than 60
    for i in range(15):
        success,image = vidcap.read()
    count+=1

