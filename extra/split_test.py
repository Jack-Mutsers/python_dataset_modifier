
import helpers.csv_manipulator as manipulator
import helpers.ocr_handwriting as reader
import numpy as np
import cv2
import os

temp_path = "temp"
flip_invert_images = True
force_guess = True

labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

def run(model_path, csv_filename = "upper_lower3.csv"):
    if os.path.exists(temp_path) is False:
        os.makedirs(temp_path)

    reader.set_model(model_path)

    for character in labelNames:
        character_index = labelNames.index(character)

        # skip characters until desired character is reached
        if character_index < labelNames.index("V"):
            continue

        # stop looping when numbers and all letters have been ran
        if character_index > labelNames.index("Z"):
            break

        print("current character: " + character)

        character_index = labelNames.index(character)

        filepath = temp_path+"/"+character+"/" + csv_filename
        (data, labels) = manipulator.load_az_dataset(datasetPath=filepath, flipped=False)
        (flippedData, _) = manipulator.load_az_dataset(datasetPath=filepath, flipped=flip_invert_images)

        character_size = len(str(labels.size))

        # each image in the A-Z and MNIST digts datasets are 28x28 pixels;
        # however, the architecture we're using is designed for 32x32 images,
        # so we need to resize them to 32x32
        data = [cv2.resize(image, (32, 32)) for image in data]
        data = np.array(data, dtype="float32")

        # add a channel dimension to every image in the dataset and scale the
        # pixel intensities of the images from [0, 255] down to [0, 1]
        data = np.expand_dims(data, axis=-1)
        data /= 255.0

        # each image in the A-Z and MNIST digts datasets are 28x28 pixels;
        # however, the architecture we're using is designed for 32x32 images,
        # so we need to resize them to 32x32
        flippedData = [cv2.resize(image, (32, 32)) for image in flippedData]
        flippedData = np.array(flippedData, dtype="float32")

        # add a channel dimension to every image in the dataset and scale the
        # pixel intensities of the images from [0, 255] down to [0, 1]
        flippedData = np.expand_dims(flippedData, axis=-1)
        flippedData /= 255.0

        num_unique_values = len(set(labels))


        guesses = reader.read_batch(data)

        index = 0
        for rawImage in data:
            flippedRawImage = flippedData[index]

            image = (rawImage * 255).astype("uint8")
            image = cv2.merge([image] * 3)
            image = cv2.resize(image, (32, 32), interpolation=cv2.INTER_LINEAR)

            flippedImage = (flippedRawImage * 255).astype("uint8")
            flippedImage = cv2.merge([flippedImage] * 3)
            flippedImage = cv2.resize(flippedImage, (32, 32), interpolation=cv2.INTER_LINEAR)

            filepath = temp_path+"/"+ character + "/"

            guess_letter_index = expected_letter_index = int(labels[index])
            guess = labelNames[guess_letter_index]
            if (num_unique_values == 1 and guess_letter_index > 9) or force_guess == True:
                guess = guesses[index]
                guess_letter_index = labelNames.index(guess)
                print("current index: "+ str(index) + " of character: " + character)

            # check if value is a number and if its the current number
            if guess_letter_index < labelNames.index("A") and guess == character:
                filepath += "number/"
            # check if guess matches the desired character (uppercase only)
            elif guess == character and guess_letter_index < labelNames.index("a"):
                filepath += "uppercase/"
            # check if the guess is in the lowercase range and if it matches the desired letter
            elif guess_letter_index > labelNames.index("Z") and (labelNames[guess_letter_index - 26]) == character:
                filepath += "lowercase/"
            else:
                print("guess: " + guess)
                filepath += "unknown/"

            # seperate guessed letter with lable description in case of misguessed/mislabeled characters
            if (num_unique_values == 1 and guess_letter_index > 9) or force_guess == True:
                if expected_letter_index > labelNames.index("Z"):
                    filepath += "labeled_lowercase/"
                else:
                    filepath += "labeled_uppercase/"

            if os.path.exists(filepath) is False:
                os.makedirs(filepath)

            newname = str(index).zfill(character_size)
            filename = filepath + newname + ".png"
            cv2.imwrite(filename, flippedImage)
            index += 1

model_path = r"models/test/2022-11-25_16-39-35/test-1x50.model"
# run(model_path)