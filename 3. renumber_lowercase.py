import helpers.csv_manipulator as manipulator
from glob import glob
import random

new_filename = "emnist-letters-train-lowercase.csv"
shuffle = True
remove_records = True
letters = {
    1:"A",
    2:"B",
    3:"C",
    4:"D",
    5:"E",
    6:"F",
    7:"G",
    8:"H",
    9:"I",
    10:"J",
    11:"K",
    12:"L",
    13:"M",
    14:"N",
    15:"O",
    16:"P",
    17:"Q",
    18:"R",
    19:"S",
    20:"T",
    21:"U",
    22:"V",
    23:"W",
    24:"X",
    25:"Y",
    26:"Z",
}


def update_lowercase_labels():
    collection = {}
    for index in letters:
        letter = letters[index]
        path = "temp/"+letter+"/lowercase/"
        files = glob(path+'*.png')
        
        index_numbers = retreve_indexes(files)
        
        records = manipulator.read_csv(filename="upper_lower.csv", filepath="temp/"+letter+"/")

        for row_index in index_numbers:
            row = records[row_index-1]
            new_col_val = int(row[0]) + 26
            row[0] = str(new_col_val)
            records[row_index-1] = row

        collection[letter] = records.copy()
    
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
    for i in range(1, total_rows + 1):
        if i not in remaining_index_numbers:
            missing_indexes.append(i)
    
    return missing_indexes

def remove_bad_records(collection):
    total = 0
    for index in letters:
        letter = letters[index]
        print(letter)

        path = "temp/"+letter+"/*/"
        files = glob(path+'*.png')
        
        remaining_index_numbers = retreve_indexes(files)
        missing_indexes = find_missing_indexes(remaining_index_numbers, len(collection[letter]))

        # remove highest index first to prevent row shifting when removing rows
        missing_indexes.sort(reverse=True)

        before = len(collection[letter])

        for remove_index in missing_indexes:
            del collection[letter][remove_index-1]

        after = len(collection[letter])
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
    for letter in collection:
        merged_list += collection[letter]

    for i in range(10):
        random.shuffle(merged_list)

    return merged_list

collection = update_lowercase_labels()

if remove_records:
    updated_collection = remove_bad_records(collection)
    updated_row_list = merge_letter_lists(updated_collection)
else:
    updated_row_list = merge_letter_lists(collection)

manipulator.write_csv(new_filename, updated_row_list)