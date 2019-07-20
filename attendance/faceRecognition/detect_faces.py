# import the necessary packages
import numpy as np
import cv2
import os
import face_recognition
import pickle

# path of the lecture photo
# path of the grade embeddings 

def detectFaces(imagePath, gradeEmbeddingsPath):

        image = imagePath

        model = os.getcwd() + r'/attendance/faceRecognition/res10_300x300.caffemodel'
        protxt = os.getcwd() + r'/attendance/faceRecognition/deploy.prototxt.txt'
        confidenceArg = 0.5
	
	# load the known faces and embeddings
        print("[INFO] loading encodings...")
        embeddingsPath = gradeEmbeddingsPath
        data = pickle.loads(open( embeddingsPath, "rb").read())
        
        # load our serialized model from disk
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(protxt, model)

        # load the input image and construct an input blob for the image
        # by resizing to a fixed 300x300 pixels and then normalizing it
        image = cv2.imread(image)

        # make an image for face recognition as dlib used RGB not BGR
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        
        (h, w) = image.shape[:2]	    
        blob = cv2.dnn.blobFromImage((image), 1.0,(300, 300), (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the detections and
        # predictions
        print("[INFO] computing object detections...")
        net.setInput(blob)
        detections = net.forward()
        boxes = []
        # counter for detections
        counter = 0

        # loop over the detections
        for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > confidenceArg:
                        
                        # increase counter
                        counter = counter + 1

                        # compute the (x, y)-coordinates of the bounding box for the
                        # object
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        transform = [startY, endX, endY,startX]
                        boxes.append(transform)
                        ## crop the detection area
                        #crop_img = image[startY:endY,startX:endX]

                        ## save the detection to a folder
                        #path = r'/home/ace/Desktop/projects/Django/try_webcam/detections'
                        #cv2.imwrite(os.path.join(path , str(counter)+'.png'), crop_img)

        # comput the facial embeddings for each face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # initialize the list of names for each face detected
        names = []
        # loop over the facial embeddings
        for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                        encoding,tolerance=0.4)
                name = "Unknown"
                # check to see if we have found a match
                if True in matches:
                        # find the indexes of all matched faces then initialize a
                        # dictionary to count the total number of times each face
                        # was matched
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        # loop over the matched indexes and maintain a count for
                        # each recognized face face
                        for i in matchedIdxs:
                                name = data["names"][i]
                                counts[name] = counts.get(name, 0) + 1

                        # determine the recognized face with the largest number of
                        # votes (note: in the event of an unlikely tie Python will
                        # select first entry in the dictionary)
                        name = max(counts, key=counts.get)
	
                # update the list of names
                names.append(name)

        return names