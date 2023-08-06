import base64
import os
from PIL import Image
import cv2
import imutils
import numpy as np
import tensorflow
from imageai.Detection import ObjectDetection
import os
import cv2
from keras import backend as K

class ComputerVision:
    def face_detection_image(image_path):
        try:
            face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
            print(os.getcwd())
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 3)
            for (x, y, w,h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
        except Exception as e:
            print(e.args)
        return img


    def face_detection_json(image_path):
        try:
            face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 3)
            response = []
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
                face = {"x": int(x), "y": int(y), "width": int(w), "height": int(h)}
                response.append(face)
            return response
        except Exception as e:
            print(e.args)


    def licence_plate_image(image_path):
        lp_cascade =cv2.CascadeClassifier("resources/haarcascades/indian_license_plate.xml")
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        licence_plates = lp_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        print(lp_cascade)
        for (x, y, w, h) in licence_plates:
            cv2.rectangle(img, (x, y), (x + w, y + h), (51, 255, 51), 5)
    
        return img
    
    
    def licence_plate_json(image_path):
        try:
            lp_cascade = cv2.CascadeClassifier('resources/haarcascades/indian_license_plate.xml')
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            licence_plates = lp_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            response = []
            for (x, y, w, h) in licence_plates:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                lp = {"x": int(x), "y": int(y), "width": int(w), "height": int(h) }
                response.append(lp)
            return response
        except Exception as e:
            print(e.args)
    IMAGE_SIZE = 299
    IMAGE_CHANNELS = 3
    
    
    def image_classification(image_path):
        try:
            model = tensorflow.keras.applications.inception_v3.InceptionV3(weights='imagenet')
            model.run_eagerly = True
            tf_default_graph = tensorflow.compat.v1.get_default_graph()
            pil_img = Image.open(image_path)
            pil_img = pil_img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.BILINEAR)
            pil_img = np.array(pil_img)
    
            if len(pil_img.shape) == 2:
                pil_img = pil_img.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 1))
                pil_img = np.repeat(pil_img, 3, axis=3)
    
            pil_img = pil_img.reshape((1, IMAGE_SIZE, IMAGE_SIZE, IMAGE_CHANNELS))
    
            with tf_default_graph.as_default():
                x = tensorflow.keras.applications.inception_v3.preprocess_input(pil_img)
                y_hat = model.predict(x)
                top3 = tensorflow.keras.applications.inception_v3.decode_predictions(y_hat, top=3)[0]
                names = list(map(lambda e: e[1], top3))
                probs = list(map(lambda e: str(round(e[2] * 100, 1)) + "%", top3))
                output = {}
                for i in range(0, len(names)):
                    output[names[i]] = probs[i]
            return output
        except Exception as e:
            print(e.args)
    
    
    def object_detection_json(image_path):
        execution_path = os.getcwd()
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath( os.path.join(execution_path, "resources/resnet50_coco_best_v2.0.1.h5"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , image_path))
        print(type(detections))
        print(detections[0])
        dt={}
        for i in detections:
            if i["percentage_probability"] > 0:
                dt[i["percentage_probability"]]=[i["name"],i["box_points"]]
        K.clear_session()
        return dt
    
    
    
    
    def object_detection_image(image_path):
        execution_path = os.getcwd()
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath( os.path.join(execution_path, "resources/resnet50_coco_best_v2.0.1.h5"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , image_path))
        print(type(detections))
        print(detections[0])
        dt={}
        for i in detections:
            if i["percentage_probability"] > 0:
                dt[i["percentage_probability"]]=[i["name"],i["box_points"]]
        ds =sorted (dt.keys())
        print(type(ds))
        ds=ds[(len(ds)-20):len(ds)]
        for i in ds:
            print(dt[i])
    
    # path
        path = image_path
    
    # Reading an image in default mode
        image = cv2.imread(path)
    
    # Window name in which image is displayed
        window_name = 'Image'
    
    # Start coordinate, here (5, 5)
    # represents the top left corner of rectangle
        start_point = (5, 5)
    
    # Ending coordinate, here (220, 220)
    # represents the bottom right corner of rectangle
        end_point = (220, 220)
    
    # Blue color in BGR
        color = (255, 0, 0)
    
    # Line thickness of 2 px
        thickness = 2
    
    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    # Displaying the image
        for i in ds:
            b=(dt[i][1][0],dt[i][1][1])
            e=(dt[i][1][2],dt[i][1][3])
            cv2.rectangle(image, b, e, color, thickness)
        K.clear_session()
        return image
