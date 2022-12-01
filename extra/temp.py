
import helpers.csv_manipulator as manipulator
import os
import shutil
from glob import glob

temp_path = "temp"

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

for character in labelNames:
    character_index = labelNames.index(character)

    # skip characters until desired character is reached
    if character_index < labelNames.index("M"):
        continue

    # stop looping when numbers and all letters have been ran
    if character_index > labelNames.index("Z"):
        break

    path = "temp/"+character+"/"

    folder_names = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

    csv = manipulator.read_csv("upper_lower.csv", path)
    character_size = len(str(len(csv)))

    for folder_name in folder_names:
        images = glob(path + folder_name + "/*.png")

        for image_path in images:
            current_path = "\\".join(image_path.split("\\")[:-1]) + "\\"
            filename = image_path.split("\\")[-1]
            index = int(filename.split(".")[0])

            newname = str(index).zfill(character_size)
            newname = filename.replace(str(index), newname)

            record = csv[index-1]
            label = int(record[0])

            if label > labelNames.index("Z"):
                move_path = current_path + "labeled_lowercase\\"
            else:
                move_path = current_path + "labeled_uppercase\\"

            if os.path.exists(move_path) is False:
                os.mkdir(move_path)

            shutil.move(image_path, move_path + newname)