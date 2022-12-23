from glob import glob
import os

start_character = "A"
end_character = "Z"

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

def run():
    for character in labelNames:
        character_index = labelNames.index(character)
        currentLetter = character

        # skip characters until desired character is reached
        if character_index < labelNames.index(start_character):
            continue

        # stop looping when numbers and all letters have been ran
        if character_index > labelNames.index(end_character):
            break

        print(currentLetter)

        path = "temp/"+currentLetter+"/"
        upper_lower_files = glob(path+'lowercase/*.png')
        upper_lower_files += glob(path+'lowercase/*/*.png')
        upper_lower_files += glob(path+'uppercase/*.png')
        upper_lower_files += glob(path+'uppercase/*/*.png')
        transfer_files = glob(path+'transfer/*/*/*.png')
        files = upper_lower_files + transfer_files

        # remove highest index first to prevent row shifting when removing rows
        files.sort(reverse=True)

        for file in files:
            path = file.replace("/", "\\")
            filename = path.split("\\")[-1]
            index = filename.split(".")[0]

            character_size = len(str(len(files)))

            new_index = int(index)
            new_name = file.replace(index, str(new_index).zfill(character_size))
            os.rename(file, new_name)

run()