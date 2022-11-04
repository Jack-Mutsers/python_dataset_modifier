import csv
import os
import numpy as np

def read_csv(filename, filepath = "input/"):
	filepath = filepath + filename
	row_list = []
	with open(filepath, mode='r') as csv_file:
		csv_reader = csv.reader(csv_file)
		row_count = 0
		for row in csv_reader:
			row_list.append(row)
			row_count += 1
			print("row number: " + str(row_count))
	
	return row_list

def write_csv(filename, row_list, filepath = "output"):
	if os.path.exists(filepath) is False:
		os.makedirs(filepath)

	filepath += "/" + filename

	with open(filepath, 'w', newline='') as outfile:
		file_writer = csv.writer(outfile)
		file_writer.writerows(row_list)

def reshape_and_rotate(image):
	image = np.fliplr(image)
	image = np.rot90(image)
	return image

def load_az_dataset(datasetPath, flipped = False):
	# initialize the list of data and labels
	data = []
	labels = []

	# loop over the rows of the A-Z handwritten digit dataset
	for row in open(datasetPath):
		# parse the label and image from the row
		row = row.split(",")
		label = int(row[0])
		image = np.array([int(x) for x in row[1:]], dtype="uint8")

		# images are represented as single channel (grayscale) images
		# that are 28x28=784 pixels -- we need to take this flattened
		# 784-d list of numbers and repshape them into a 28x28 matrix
		image = image.reshape((28, 28))

		if flipped:
			image = reshape_and_rotate(image)

		# update the list of data and labels
		data.append(image)
		labels.append(label)

	# convert the data and labels to NumPy arrays
	data = np.array(data, dtype="float32")
	labels = np.array(labels, dtype="int")

	# return a 2-tuple of the A-Z data and labels
	return (data, labels)

