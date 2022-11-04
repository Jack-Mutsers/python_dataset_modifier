import random
import helpers.csv_manipulator as manipulator

# filename = "emnist-byclass-train.csv"
filename = "emnist-byclass-train.csv"
new_filename = "emnist-byclass-train-modded.csv"
shuffle = True

def lower_to_upper_clasification(row_list):
    row_count = 0

    if shuffle:
        random.shuffle(row_list)

    for row in row_list:
        if int(row[0]) > 35:
            row_count += 1
            new_col_val = int(row[0]) - 26
            print("old val: "+ str(row[0]) +", new val: "+ str(new_col_val))
            row[0] = str(new_col_val)

    return row_list

row_list = manipulator.read_csv(filename)

updated_row_list = lower_to_upper_clasification(row_list)
manipulator.write_csv(new_filename, updated_row_list)