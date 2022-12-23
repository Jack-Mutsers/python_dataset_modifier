import helpers.csv_manipulator as manipulator
from glob import glob
import random
import os

new_filename = "emnist-letters-train-trimmed-letters-only.csv"
shuffle = True
remove_records = True
start_character = "A"
end_character = "Z"
starting_index = 1

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

def retreve_records():
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

        collection[character] = manipulator.read_csv(filename="upper_lower.csv", filepath="temp/"+character+"/")

    return collection

def update_labels(collection):
    for character in labelNames:
        character_index = labelNames.index(character)

        # skip characters until desired character is reached
        if character_index < labelNames.index(start_character):
            continue

        # stop looping when numbers and all letters have been ran
        if character_index > labelNames.index(end_character):
            break

        print(character)

        path = "temp/"+character+"/"

        if os.path.exists(path) is False:
            continue
        
        lowercase_files = glob(path+'lowercase/*.png')
        uppercase_files = glob(path+'uppercase/*.png')
        image_files = lowercase_files + uppercase_files
        for file_directory in image_files:
            filepath = file_directory.replace("/", "\\") # make path seperator universal
            upper_lower = filepath.split("\\")[-2] # contains uppercase or lowercase

            filename = filepath.split("\\")[-1] # contains the filename like 00001.png

            record_index = int(filename.split(".")[0]) - starting_index # retreves the array index number from the file name

            record = collection[character][record_index]

            # get index of target letter
            new_label = character_index

            # if image is lowecase raise lable value by 26
            if upper_lower == "lowercase" and new_label < labelNames.index("a"):
                new_label += 26
            elif upper_lower == "uppercase" and new_label > labelNames.index("Z"):
                new_label -= 26

            # update label value of record
            record[0] = str(new_label)

            # overwrite existing record in list with updated record
            collection[character][record_index] = record
    
    return collection

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
            target_letter = filepath.split("\\")[-3] # new Letter to be assigned
            upper_lower = filepath.split("\\")[-2] # contains uppercase or lowercase

            filename = filepath.split("\\")[-1] # contains the filename like 00001.png

            record_index = int(filename.split(".")[0]) - starting_index # get row index number

            record = collection[currentLetter][record_index]

            # get index of target letter
            new_label = labelNames.index(target_letter)

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

def retreve_remaining_indexes(files):
    index_numbers = []
    for filepath in files:
        filename = filepath.split("\\")[-1] # get file name like 00001.png
        fileindex = filename.split(".")[0] # get file index like 00001
        index_numbers.append(int(fileindex) - starting_index)

    return index_numbers

def find_missing_indexes(remaining_index_numbers, total_rows):
    missing_indexes = []

    for i in range(0, total_rows):
        if i not in remaining_index_numbers:
            missing_indexes.append(i)
    
    return missing_indexes

def remove_bad_records(collection):
    total = 0
    for character in labelNames:
        character_index = labelNames.index(character)

        # skip characters until desired character is reached
        if character_index < labelNames.index(start_character):
            continue

        # stop looping when numbers and all letters have been ran
        if character_index > labelNames.index(end_character):
            break

        print(character)

        deletedRecords = []
        deletedRecordIndexes = []

        path = "temp/"+character+"/"
        uppercase_files = glob(path+'uppercase/*.png')
        lowercase_files = glob(path+'lowercase/*.png')
        transfer_files = glob(path+'transfer/*/*/*.png')
        files = uppercase_files + lowercase_files + transfer_files

        remaining_index_numbers = retreve_remaining_indexes(files)
        missing_indexes = find_missing_indexes(remaining_index_numbers, len(collection[character]))

        # remove highest index first to prevent row shifting when removing rows
        missing_indexes.sort(reverse=True)

        before = len(collection[character])

        for remove_index in missing_indexes:
            # del collection[currentLetter][remove_index]
            deletedRecords.append(collection[character][remove_index])
            deletedRecordIndexes.append([str(remove_index)])
            collection[character][remove_index] = []

        tmpList = [x for x in collection[character] if x != []]
        collection[character] = tmpList

        # manipulator.write_csv("deleted.csv", deletedRecords, path)
        # manipulator.write_csv("deletedIndexes.csv", deletedRecordIndexes, path)
        # manipulator.write_csv("upper_lower2.csv", collection[character], path)

        after = len(collection[character])
        removed = before - after
        total += removed

        print("before: " + str(before))
        print("after: " + str(after))
        print("removed: " + str(removed))
        print()
    
    print("total removed: " + str(total))
    return collection

def merge_letter_lists(collection):
    merged_list = []
    for character in collection:
        merged_list += collection[character]

    for i in range(10):
        random.shuffle(merged_list)

    return merged_list

collection = retreve_records()
relabled_collection = update_labels(collection)

if remove_records:
    restructured_collection = move_transfer_items(relabled_collection)
    filtered_collection = remove_bad_records(restructured_collection)
    updated_row_list = merge_letter_lists(filtered_collection)
else:
    updated_row_list = merge_letter_lists(relabled_collection)

print("writing new CSV file")
manipulator.write_csv(new_filename, updated_row_list)
print("CSV file was created")