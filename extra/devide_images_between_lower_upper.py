
import random
import math
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
    if character_index < labelNames.index("Z"):
        continue

    # stop looping when numbers and all letters have been ran
    if character_index > labelNames.index("Z"):
        break

    path = "temp/"+character+"/"
    images = glob(path + "*/*.png")

    random.shuffle(images)

    total_images = math.ceil(len(images) / 2)
    image_path_groups = [images[x:x+total_images] for x in range(0, len(images), total_images)]

    count = 0
    for image_path_group in image_path_groups:
        move_path = "lowercase\\"
        if count > 0:
            move_path = "uppercase\\"

        for image_path in image_path_group:
            current_path = "\\".join(image_path.split("\\")[:-1]) + "\\"
            filename = image_path.split("\\")[-1]
            
            filename = filename.replace("lowercase", "").replace("uppercase", "")
            
            index = filename.split(".")[0]

            newname = str(index).zfill(5)
            newname = filename.replace(str(index), newname)

            new_image_path = path + move_path + newname

            shutil.move(image_path, new_image_path)
        
        count += 1