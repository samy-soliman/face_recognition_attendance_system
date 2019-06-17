# USAGE
# python encode_faces.py --dataset dataset --encodings encodings.pickle

# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os


def encodeFaces(datasetPath,encodingsPath):

	# construct the argument parser and parse the arguments

	detectionMethod = 'hog'

	# grab the paths to the input images in our dataset
	print("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images(datasetPath))

	# initialize the list of known encodings and known names
	oldknownEncodings = []
	oldknownNames = []

	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1,
			len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		# load the input image and convert it from RGB (OpenCV ordering)
		# to dlib ordering (RGB)
		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb,
			model=detectionMethod)

		# compute the facial embedding for the face
		#num_jitters=100
		encodings = face_recognition.face_encodings(rgb, boxes)

		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			oldknownEncodings.append(encoding)
			oldknownNames.append(name)

	print('loading  old encodings to add new ones')
	oldEncode = pickle.loads(open(encodingsPath, "rb").read())
	newKnownEncodings = oldEncode['encodings']+ oldknownEncodings
	newknownNames = oldEncode['names'] + oldknownNames
	data= {"encodings": newKnownEncodings, "names": newknownNames}

	# dump the facial encodings + names to disk
	print("[INFO] serializing encodings...")
	f = open(encodingsPath, "wb")
	f.write(pickle.dumps(data))
	f.close()
