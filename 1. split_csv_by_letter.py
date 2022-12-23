import helpers.csv_manipulator as manipulator

# filename = "emnist-letters-train-lowercase.csv"
# filename = "emnist-byclass-train-trimmed-letters-only.csv"
filename = "typed_letters_sm.csv"
label_offset = 0 # this is the amount that the label value has to be raised to match the correct value for my model

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

def split_by_letter(row_list):
    print("split different characters")
    collection = {}
    
    for character in labelNames:
        character_index = labelNames.index(character)
        if character_index > labelNames.index("Z"):
            break
        
        print("current character: " + character)

        collection[character] = []

    for row in row_list:
        index = int(row[0]) + label_offset
        row[0] = str(index)
        if index > 35:
            index = index - 26
        character = labelNames[index]
        collection[character] += [row]
    
    return collection

row_list = manipulator.read_csv(filename)
collection = split_by_letter(row_list)

for character in collection:
    filepath = "temp\\"+character
    manipulator.write_csv("upper_lower.csv", collection[character], filepath)
