from glob import glob
import random
import numpy as np
import cv2

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

multiplication_count = 3 # 0=1 -> 1=2 -> 2=4 -> 3=8 -> 4=16
invert_image = True
# csv_filename = "perfect_joined_letters_sm.csv"
csv_filename = "typed_letters_sm.csv"

print("loading images")
images = glob("input/images/*.png")

if len(images) < 1:
    exit("no images found to make a dataset out of")

print("building dataset")
for i in range(0, multiplication_count):
    images = images + images
    random.shuffle(images)

print("shuffling records")
random.shuffle(images)
random.shuffle(images)
random.shuffle(images)

def show_image(image):
    cv2.imshow("Image", image)
    cv2.waitKey(0)

print("building CSV")
csv = []
count = 0
for file in images:
    character = file.split(".")[0]
    character = character.replace("/", "\\").split("\\")[-1]
    character = character.split("_")[-1]
    label = labelNames.index(character)

    count += 1
    print(str(count)+" / "+ str(len(images)) + " file: " + file)
    # 1. Read image
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(gray, (28, 28))

    if invert_image and (label == labelNames.index("i") or label == labelNames.index("j")):
        image = (255-image)

    # show_image(image)

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
    
    

    record = str(label) +","+ ",".join(tmp)

    csv.append(record)


print("writing CSV to file")
# 4. Save list of lists to CSV
with open("output/" + csv_filename, 'w') as f:
    for row in csv:
        f.write(row + '\n')