# import the necessary packages
from keras.models import load_model
import argparse

with_offset = False
offset = 0

# model_path = r"models/test/test.model"
# model_path = r"models/test/2022-11-25_16-39-35/test-1x50.model"
model_path = r"models/handwriting-lowercase-5-11-2022.model"
# model_path = r"models/handwriting-lowercase.model"

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", type=str, required=False, help="path to trained handwriting recognition model", default=model_path)
args = vars(ap.parse_args())

# load the handwriting OCR model
print("[INFO] loading handwriting OCR model...")
model = load_model(args["model"])

# define the list of label names
labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

def set_model(model_path):
	global model
	# load the handwriting OCR model
	print("[INFO] loading handwriting OCR model...")
	model = None
	model = load_model(model_path)

def read(image):
	# classify the character
	probs = model.predict(image)
	prediction = probs.argmax(axis=1)

	plus = offset
	if prediction[0] > 4 and with_offset == True:
		plus *= 2
		plus += 10

	label = labelNames[prediction[0] + plus]
	
	return label

def read_batch(images):
	# classify the character
	probs = model.predict(images, batch_size=256)
	calc = probs.argmax(axis=1)

	labels = []
	for prediction in calc:
		plus = offset
		if prediction > 4 and with_offset == True:
			plus *= 2
			plus += 10

		label = labelNames[prediction + plus]
		labels.append(label)
	
	return labels
