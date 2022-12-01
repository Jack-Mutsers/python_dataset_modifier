import helpers.csv_manipulator as manipulator
from glob import glob
import shutil
import os

new_filename = "emnist-byclass-train-test.csv"
shuffle = True
remove_records = True
start_character = "V"
end_character = "Z"
deleted_records = {
    "0": [],
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
    "8": [],
    "9": [],
    "A": [],
    "B": [],
    "C": [],
    "D": [],
    "E": [],
    "F": [],
    "G": [],
    "H": [],
    "I": [],
    "J": [],
    "K": [],
    "L": [],
    "M": [],
    "N": [],
    "O": [],
    "P": [],
    "Q": [],
    "R": [],
    "S": [],
    "T": [],
    "U": [],
    "V": [],
    "W": [],
    "X": [],
    "Y": [],
    "Z": [],
}

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

def retreve_records(csv_filename):
    collection = {}
    for character in labelNames:
        character_index = labelNames.index(character)

        # skip characters until desired character is reached
        if character_index < labelNames.index(start_character):
            continue

        # stop looping when numbers and all letters have been ran
        if character_index > labelNames.index(end_character):
            break

        print(character)

        collection[character] = manipulator.read_csv(filename=csv_filename, filepath="temp/"+character+"/")
        deleted_records[character] = manipulator.read_csv(filename="deleted.csv", filepath="temp/"+character+"/")

    return collection

def retreve_indexes(files):
    index_numbers = []
    for filepath in files:
        filename = filepath.split("\\")[-1]
        filename = filename.split(".")[0]
        index_numbers.append(int(filename))

    return index_numbers

def find_missing_indexes(remaining_index_numbers, total_rows):
    missing_indexes = []
    for i in range(1, total_rows):
        if i not in remaining_index_numbers:
            missing_indexes.append(i)
    
    return missing_indexes

def move_transfer_items(collection):
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

        path = "temp/"+currentLetter+"/transfer/"

        if os.path.exists(path) is False:
            continue
        
        lowercase_files = glob(path+'*/*/*.png')
        for filepath in lowercase_files:
            target_letter = filepath.split("\\")[-3]
            upper_lower = filepath.split("\\")[-2]

            record_index = filepath.split("\\")[-1]
            record_index = int(record_index.split(".")[0]) - 1

            record = collection[currentLetter][record_index]

            # get index of target letter
            new_label = list(labelNames.values()).index(target_letter)

            # if image is lowecase raise lable value by 26
            if upper_lower == "lowercase" and new_label <= labelNames.index("Z"):
                new_label += 26
            elif upper_lower == "uppercase" and new_label > labelNames.index("Z"):
                new_label -= 26

            # update label value of record
            record[0] = str(new_label)

            # overwrite existing record in list with updated record
            collection[currentLetter][record_index] = record
    
    return collection

def update_labels(collection):
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

        if os.path.exists(path) is False:
            continue
        
        image_files = glob(path+'*/*.png')
        for filepath in image_files:
            upper_lower = filepath.split("\\")[-2]

            record_index = filepath.split("\\")[-1]
            record_index = int(record_index.split(".")[0]) - 1

            record = collection[currentLetter][record_index]

            # get index of target letter
            new_label = character_index

            # if image is lowecase raise lable value by 26
            if upper_lower == "lowercase" and new_label <= labelNames.index("Z"):
                new_label += 26
            elif upper_lower == "uppercase" and new_label > labelNames.index("Z"):
                new_label -= 26

            # update label value of record
            record[0] = str(new_label)

            # overwrite existing record in list with updated record
            collection[currentLetter][record_index] = record
    
    return collection

def remove_bad_records(collection):
    total = 0
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

        remaining_index_numbers = retreve_indexes(files)
        missing_indexes = find_missing_indexes(remaining_index_numbers, len(collection[currentLetter]))

        # remove highest index first to prevent row shifting when removing rows
        missing_indexes.sort(reverse=True)

        before = len(collection[currentLetter])

        for remove_index in missing_indexes:
            deleted_records[currentLetter].append(collection[currentLetter][remove_index])
            del collection[currentLetter][remove_index]

        after = len(collection[currentLetter])
        removed = before - after
        total += removed

        print("before: " + str(before))
        print("after: " + str(after))
        print("removed: " + str(removed))
        print()
    
    print("total removed: " + str(total))
    return collection

def remove_folders(character):
    search_dir = "temp/"+character+"/"
    folder_names = [name for name in os.listdir(search_dir) if os.path.isdir(os.path.join(search_dir, name))]

    for folder_name in folder_names:
        shutil.rmtree(search_dir + folder_name)

def run(csv_filename = "upper_lower.csv", new_csv_filename = "upper_lower.csv"):
    collection = retreve_records(csv_filename)
    relabled_collection = update_labels(collection)

    restructured_collection = move_transfer_items(relabled_collection)
    filtered_collection = remove_bad_records(restructured_collection)

    for character in labelNames:
        character_index = labelNames.index(character)

        # skip characters until desired character is reached
        if character_index < labelNames.index(start_character):
            continue

        # stop looping when numbers and all letters have been ran
        if character_index > labelNames.index(end_character):
            break

        manipulator.write_csv(filename=new_csv_filename, row_list=filtered_collection[character], filepath="temp/"+character+"/")
        manipulator.write_csv(filename="deleted.csv", row_list=deleted_records[character], filepath="temp/"+character+"/")
        remove_folders(character)

# run()