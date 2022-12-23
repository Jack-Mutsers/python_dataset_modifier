# import os,sys,inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0,parentdir) 

from glob import glob
import random
import numpy as np
import shutil
import cv2

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

csv_filename = "letter_e.csv"

images = glob("letter_cropper/dataset/*/*.png")

for i in range(0, 15):
    random.shuffle(images)

for image in images:
    dest = r"letter_cropper/dataset/merged/"
    name = len(glob(dest + "*.png"))
    shutil.copy(image, dest + str(name)+".png")
    

images = glob("letter_cropper/dataset/merged/*.png")

csv = []
for file in images:
    print(file)
    # 1. Read image
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(gray, (28, 28))
    
    # 2. Convert image to NumPy array
    arr = np.asarray(image)

    # 3. Convert 3D array to 2D list of lists
    lst = []
    for row in arr:
        tmp = []
        for col in row:
            tmp.append(str(col))
        lst.append(tmp)

    tmp = []
    for row in lst:
        tmp.append(",".join(row))
        
    record = str(labelNames.index("e")) +","+ ",".join(tmp)

    csv.append(record)

# 4. Save list of lists to CSV
with open("output/" + csv_filename, 'w') as f:
    for row in csv:
        f.write(row + '\n')