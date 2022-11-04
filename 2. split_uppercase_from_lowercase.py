
import helpers.csv_manipulator as manipulator
import helpers.ocr_handwriting as reader
import numpy as np
import cv2
import os

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

labelNames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

for letter_index in letters:
    letter = letters[letter_index]

    print("current letter: " + letter)

    filepath = "temp/"+letter+"/upper_lower.csv"
    (data, labels) = manipulator.load_az_dataset(datasetPath=filepath, flipped=True)

    # each image in the A-Z and MNIST digts datasets are 28x28 pixels;
    # however, the architecture we're using is designed for 32x32 images,
    # so we need to resize them to 32x32
    data = [cv2.resize(image, (32, 32)) for image in data]
    data = np.array(data, dtype="float32")

    # add a channel dimension to every image in the dataset and scale the
    # pixel intensities of the images from [0, 255] down to [0, 1]
    data = np.expand_dims(data, axis=-1)
    data /= 255.0

    num_unique_values = len(set(labels))

    index = 0
    for rawImage in data:
        image = (rawImage * 255).astype("uint8")
        image = cv2.merge([image] * 3)
        image = cv2.resize(image, (32, 32), interpolation=cv2.INTER_LINEAR)

        filepath = "temp/"+ letter + "/"

        guess_letter_index = labels[index]
        guess = labelNames[guess_letter_index - 1]
        if num_unique_values == 1:
            guess = reader.read(data[np.newaxis, index])

        if guess == letter:
            filepath += "uppercase/"
        elif guess == "empty":
            filepath += "unkown/"
        else:
            filepath += "lowercase/"

        if os.path.exists(filepath) is False:
            os.makedirs(filepath)

        index += 1
        filename = filepath + str(index) + ".png"
        cv2.imwrite(filename, image)