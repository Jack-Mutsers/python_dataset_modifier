import helpers.csv_manipulator as manipulator

filename = "emnist-letters-train-lowercase.csv"

def split_by_letter(row_list):
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

    collection = {}
    
    for letter in letters:
        collection[letters[letter]] = []

    for row in row_list:
        index = int(row[0])
        if index > 26:
            index = index - 26
        letter = letters[index]
        collection[letter] += [row]
    
    return collection

row_list = manipulator.read_csv(filename)
collection = split_by_letter(row_list)

for letter in collection:
    filepath = "temp\\"+letter
    manipulator.write_csv("upper_lower.csv", collection[letter], filepath)
