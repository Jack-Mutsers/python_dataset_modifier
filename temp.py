
import helpers.csv_manipulator as manipulator
import os
import shutil
from glob import glob

temp_path = "temp"

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

if os.path.exists(temp_path) is False:
		os.makedirs(temp_path)

for character in labelNames:
    character_index = labelNames.index(character)

    # skip characters until desired character is reached
    if character_index < labelNames.index("A"):
        continue

    # stop looping when numbers and all letters have been ran
    if character_index > labelNames.index("L"):
        break

    print("current character: " + character)

    character_index = labelNames.index(character)

    row_list = manipulator.read_csv("/upper_lower.csv", temp_path+"/"+character)

    unknown_images = glob(temp_path+"/"+character+"/unkown/*.png")

    for image_path in unknown_images:
        filename = image_path.split("\\")[-1]
        image_index = int(filename.split(".")[0]) - 1

        row = row_list[image_index]

        copy_path = temp_path+"/"+ character + "/"

        expected_letter_index = int(row[0])
        letter = labelNames[expected_letter_index]
        if expected_letter_index > labelNames.index("Z"):
            copy_path += "unkown/lowercase/"
        else:
            copy_path += "unkown/uppercase/"

        if os.path.exists(copy_path) is False:
            os.makedirs(copy_path)

        # copy file to new directory
        shutil.move(image_path, copy_path)