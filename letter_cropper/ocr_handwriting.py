# import the necessary packages
from keras.models import load_model
from imutils.contours import sort_contours
from glob import glob
import numpy as np
import imutils
import cv2

image_paths = [
	r"letter_cropper/images/img-06.jpeg", # uper with lowercase letters (more space + no background)
	# r"letter_cropper/images/letter_e1_trimmed.jpg",
	# r"letter_cropper/images/letter_e2_trimmed.jpg",
	# r"letter_cropper/images/letter_e3_trimmed.jpg",
]

# model_path = r"models/back-up/2022-11-10_11-11-16/handwriting-lowercase-4x100.model"
# model_path = r"models/new/handwriting_new.model"
model_path = r"models/working/handwriting_lowercase_uppercase_clasification.model"

# define the list of label names
labelNames = ""
# labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames += "abcdefghijklmnopqrstuvwxyz"
labelNames = [l for l in labelNames]

# load the handwriting OCR model
print("[INFO] loading handwriting OCR model...")
model = load_model(model_path)

for image_path in image_paths:
	# load the input image from disk, convert it to grayscale, and blur
	# it to reduce noise
	image = cv2.imread(image_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)

	# perform edge detection, find contours in the edge map, and sort the
	# resulting contours from left-to-right
	edged = cv2.Canny(blurred, 30, 150)
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sort_contours(cnts, method="left-to-right")[0]

	# initialize the list of contour bounding boxes and associated
	# characters that we'll be OCR'ing
	chars = []

	# loop over the contours
	for c in cnts:
		# compute the bounding box of the contour
		(x, y, w, h) = cv2.boundingRect(c)
		
		# filter out bounding boxes, ensuring they are neither too small
		# nor too large
		if (w >= 5 ) and (h >= 15 and h <= 120):
			# extract the character and threshold it to make the character
			# appear as *white* (foreground) on a *black* background, then
			# grab the width and height of the thresholded image
			roi = gray[y:y + h, x:x + w]

			thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
			(tH, tW) = thresh.shape

			# if the width is greater than the height, resize along the
			# width dimension
			if tW > tH:
				thresh = imutils.resize(thresh, width=32)

			# otherwise, resize along the height
			else:
				thresh = imutils.resize(thresh, height=32)

			# re-grab the image dimensions (now that its been resized)
			# and then determine how much we need to pad the width and
			# height such that our image will be 32x32
			(tH, tW) = thresh.shape
			dX = int(max(0, 32 - tW) / 2.0)
			dY = int(max(0, 32 - tH) / 2.0)

			# pad the image and force 32x32 dimensions
			padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY, left=dX, right=dX, borderType=cv2.BORDER_CONSTANT, value=(0, 0, 0))
			padded = cv2.resize(padded, (32, 32))

			# prepare the padded image for classification via our
			# handwriting OCR model
			padded = padded.astype("float32") / 255.0
			padded = np.expand_dims(padded, axis=-1)

			# update our list of characters that will be OCR'd
			chars.append((padded, (x, y, w, h)))

	# extract the bounding box locations and padded characters
	boxes = [b[1] for b in chars]
	chars = np.array([c[0] for c in chars], dtype="float32")

	image_storage = r"letter_cropper/dataset/"
	for char in chars:
		name = len(glob(image_storage + "*.png"))
		cv2.imwrite(image_storage + str(name) + ".png", 255*char)
		# cv2.imshow("Image", char)
		# cv2.waitKey(0)

	# OCR the characters using our handwriting recognition model
	preds = model.predict(chars)

	# loop over the predictions and bounding box locations together
	for (pred, (x, y, w, h)) in zip(preds, boxes):
		# find the index of the label with the largest corresponding
		# probability, then extract the probability and label
		i = np.argmax(pred)
		prob = pred[i]
		label = labelNames[i]
		
		# draw the prediction on the image
		print("[INFO] {} - {:.2f}%".format(label, prob * 100))
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.putText(image, label, (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

	# show the image
	# cv2.imshow("Image", image)
	# cv2.waitKey(0)

