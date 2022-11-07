# import the necessary packages
from keras.models import load_model
import argparse

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

def read(image):
	# classify the character
	probs = model.predict(image)
	prediction = probs.argmax(axis=1)
	label = labelNames[prediction[0]]
	
	return label
