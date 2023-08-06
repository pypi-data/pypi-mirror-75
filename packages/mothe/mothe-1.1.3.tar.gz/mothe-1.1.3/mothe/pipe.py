from __future__ import print_function
from sklearn.model_selection import train_test_split
import yaml
import os
import sys
import csv
import io
import cv2
import numpy as np
import tensorflow
import keras
import h5py
import math as m
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
import scipy
from scipy.optimize import linear_sum_assignment
import glob
import time
import argparse
from filterpy.kalman import KalmanFilter
from filterpy.stats import mahalanobis
import filterpy
import pyautogui

class mothe:

    def __init__(self, root_path, thresh_min, thresh_max, step_for_dt):
        self.root_path = root_path
        self.thresh_min = thresh_min
        self.thresh_max = thresh_max
        self.step_for_dt = step_for_dt
    @staticmethod
    def scr_resize(image_name):
        width, height = pyautogui.size()
        scale_width = width/image_name.shape[1]
        scale_height = height/image_name.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(image_name.shape[1] * scale)
        window_height = int(image_name.shape[0] * scale)
        print(image_name.shape[0], image_name.shape[1])
        return window_width, window_height, scale


    def set_config(self, movie_name):
        self.movie_name = movie_name
        # initialize the list of reference points and boolean indicating
        # whether cropping is being performed or not
        def click_and_crop(event, x, y, flags, param):
            # grab references to the global variables
            global refPt, cropping

            # if the left mouse button was clicked, record the starting
            # (x, y) coordinates and indicate that cropping is being
            # performed
            if event == cv2.EVENT_LBUTTONDOWN:
                refPt = [(x, y)]
                cropping = True

            # check to see if the left mouse button was released
            elif event == cv2.EVENT_LBUTTONUP:
                # record the ending (x, y) coordinates and indicate that
                # the cropping operation is finished
                refPt.append((x, y))
                cropping = False

                # draw a rectangle around the region of interest
                cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
                cv2.imshow("image", image)
        specifications= {}
        root_dir= self.root_path
        specifications.__setitem__('root_dir', root_dir)
        step_for_dt= self.step_for_dt
        specifications.__setitem__('step_for_dt', step_for_dt)

        # Add the dimensions of the bounding box based on user requirement
        movieName =  self.movie_name
        cap = cv2.VideoCapture(root_dir + "/" + movieName)
        i=0
        steps=50
        nframe =cap.get(cv2.CAP_PROP_FRAME_COUNT)
        while(cap.isOpened() & (i<(nframe-steps))):
            i = i + steps
            print("[REQUIRED.....] Click and drag the mouse across the area of interest. In case you want to navigate to a different frame, press 'k'")
            cap.set(cv2.CAP_PROP_POS_FRAMES,i)

            ret, image = cap.read()
            clone = image.copy()
            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            ww, wh, scale = mothe.scr_resize(image)
            cv2.resizeWindow('image', ww, wh)
            cv2.setMouseCallback("image", click_and_crop)
            while True:
                # display the image and wait for a keypress
                cv2.imshow("image", image)
                key = cv2.waitKey(1) & 0xFF

                # if the 'r' key is pressed, reset the cropping region
                if key == ord("r"):
                    frame = clone.copy()

                # if the 'c' key is pressed, break from the loop
                elif key == ord("c"):
                    break

            # if there are two reference points, then crop the region of interest
            # from teh image and display it
            if len(refPt) == 2:
                roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                if (refPt[1][0]-refPt[0][0]) > (refPt[1][1]-refPt[0][1]):
                    specifications.__setitem__('annotation_size', ((refPt[1][0]-refPt[0][0])*scale))
                else:
                    specifications.__setitem__('annotation_size', ((refPt[1][1]-refPt[0][1])*scale))
                cv2.imshow("ROI", roi)
                cv2.waitKey(0)

            # close all open windows
            cv2.destroyAllWindows()
            break
        threshold_value1 = self.thresh_min
        specifications.__setitem__('threshold_value1', threshold_value1)
        threshold_value2 = self.thresh_max
        specifications.__setitem__('threshold_value2', threshold_value2)

        with io.open("config.yml", "w", encoding= "utf8") as outfile:
            yaml.dump(specifications, outfile, default_flow_style= False, allow_unicode= True)


    def train_model(self):
        np.random.seed(7)
        with open("config.yml", "r") as stream:
            config_data= yaml.safe_load(stream)
        path = config_data["root_dir"]
        cls0 = path + '/no/'
        cls1 = path + '/yes/'

        lst0 = [name for name in os.listdir(cls0) if not name.startswith('.')]
        lst1 = [name for name in os.listdir(cls1) if not name.startswith('.')]
        lst=[]
        lst.extend(lst0)
        lst.extend(lst1)
        #Create image dataset
        trainData = np.ndarray(shape=(len(lst),40,40,3), dtype='uint8', order='C')
        targetData = np.hstack((np.zeros(len(lst0)),np.ones(len(lst1))))
        #extract image data and append to matrix
        i=0
        for i in range(trainData.shape[0]):
            if(i<len(lst0)):
              im = cv2.imread(cls0+lst[i])
            else:
              im = cv2.imread(cls1+lst[i])
            if(im is not None):
               trainData[i-1,:,:] = cv2.resize(im,(40,40))

        # Change the labels from categorical to one-hot encoding
        targetH = to_categorical(targetData)

        #data preprocessing

        train_X = trainData.reshape(-1, 40,40, 3)
        train_X = train_X.astype('float32')
        train_X = train_X / 255.

        train_X,valid_X,train_label,valid_label = train_test_split(train_X, targetH, test_size=0.4, random_state=13)

        batch_size = 64
        epochs = 25
        num_classes = 2

        bb_model = Sequential()
        bb_model.add(Conv2D(64, kernel_size=(3, 3),activation='linear',input_shape=(40,40,3),padding='same'))
        bb_model.add(LeakyReLU(alpha=0.1))
        bb_model.add(MaxPooling2D((2, 2),padding='same'))
        #Second layer
        bb_model.add(Conv2D(96, (3, 3), activation='linear',padding='same'))
        bb_model.add(LeakyReLU(alpha=0.1))
        bb_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
        bb_model.add(Dropout(0.25))
        #Third layer
        bb_model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
        bb_model.add(LeakyReLU(alpha=0.3))
        bb_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
        #Dense layer
        bb_model.add(Flatten())
        bb_model.add(Dense(96, activation='linear'))
        bb_model.add(LeakyReLU(alpha=0.1))
        bb_model.add(Dropout(0.3))

        bb_model.add(Dense(128, activation='linear'))
        bb_model.add(LeakyReLU(alpha=0.1))
        bb_model.add(Dropout(0.3))


        #Output
        bb_model.add(Dense(num_classes, activation='softmax'))

        #Compile the model

        bb_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(),metrics=['accuracy'])
        bb_model.summary()

        #Training

        bb_train = bb_model.fit(train_X, train_label, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(valid_X, valid_label))

        accuracy =bb_train.history['accuracy']
        val_accuracy = bb_train.history['val_accuracy']
        loss = bb_train.history['loss']
        val_loss = bb_train.history['val_loss']
        epochs = range(len(accuracy))
        plt.plot(epochs, accuracy, 'bo', label='Training accuracy')
        plt.plot(epochs, val_accuracy, 'b', label='Validation accuracy')
        plt.title('Training and validation accuracy')
        plt.legend()
        plt.figure()
        plt.plot(epochs, loss, 'bo', label='Training loss')
        plt.plot(epochs, val_loss, 'b', label='Validation loss')
        plt.title('Training and validation loss')
        plt.legend()
        plt.show()

        #Save the model for future
        bb_model.save(path + "/mothe_model.h5py")

    def detection(self, movie_name, model_name):
        self.movie_name = movie_name
        self.model_name = model_name
        with open("config.yml", "r") as stream:
            config_data= yaml.safe_load(stream)
        path = config_data["root_dir"]
        grabsize = (int(config_data["annotation_size"]))
        threshold_value1 = (int(config_data["threshold_value1"]))
        threshold_value2 = (int(config_data["threshold_value2"]))
        steps = (int(config_data["step_for_dt"]))
        #get screen resolution
        # screen_width = int(root.winfo_screenwidth())
        # screen_height = int(root.winfo_screenheight())

        movieName =  self.movie_name
        cap = cv2.VideoCapture(movieName)

        nframe =cap.get(cv2.CAP_PROP_FRAME_COUNT)
        nx = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        ny = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


        #Create data frames to store x and y coords of the identified blobs, rows for each individual column for each frame
        df = pd.DataFrame(columns=['c_id','x_px','y_px','frame'])
        data = pd.DataFrame([])
        i=0
        row = 0
        alt = 100#int(input("Enter height of video(integer):  "))
        # work out size of box if box if 32x32 at 100m
        #grabSize = int(m.ceil((100/alt)*12))
        #Load model
        from keras.models import load_model
        bb_model = load_model(self.model_name)
        #Video writer object
        out = cv2.VideoWriter(path + '/mothe_detect.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (nx,ny))

        while(cap.isOpened() & (i<(nframe-steps))):

          i = i + steps
          print("[UPDATING.....]{}th frame detected and stored".format(i))
          cap.set(cv2.CAP_PROP_POS_FRAMES,i)
          ret, frame = cap.read()
          if ret == False:
              continue
          grayF = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          #Equalize image
          #gray = cv2.equalizeHist(gray)
          #remove noise
          gray = cv2.medianBlur(grayF,5)
          #Invert image
          gray = cv2.bitwise_not(gray)

          # Blob detection
          # Setup SimpleBlobDetector parameters.
          params = cv2.SimpleBlobDetector_Params()

          # Change thresholds
          params.minThreshold = threshold_value1;
          params.maxThreshold = threshold_value2;

          # Filter by Area.
          #params.filterByArea = False
        #  params.minArea = 100
         # params.maxArea = 150

          # Filter by Circularity
          params.filterByCircularity = False
          #params.minCircularity = 0.1

          # Filter by Convexity
          params.filterByConvexity = False
          #params.minConvexity = 0.87

          # Filter by Inertia
          params.filterByInertia = False

          # Create a detector with the parameters
          ver = (cv2.__version__).split('.')
          if int(ver[0]) < 3 :
            detector = cv2.SimpleBlobDetector(params)
          else :
            detector = cv2.SimpleBlobDetector_create(params)

          # Detect blobs.
          keypoints = detector.detect(gray)

          testX = np.ndarray(shape=(len(keypoints),40,40,3), dtype='uint8', order='C')
          j = 0
          for keyPoint in keypoints:

            ix = keyPoint.pt[0]
            iy = keyPoint.pt[1]
            tmpImg=frame[max(0,int(iy-grabsize)):min(ny,int(iy+grabsize)), max(0,int(ix-grabsize)):min(nx,int(ix+grabsize))].copy()

            tmpImg1=cv2.resize(tmpImg,(40,40))
            testX[j,:,:,:]=tmpImg1
            j = j + 1
          testX = testX.reshape(-1, 40,40, 3)
          testX = testX.astype('float32')
          testX = testX / 255.
          pred = bb_model.predict(testX)
          Pclass = np.argmax(np.round(pred),axis=1)
          j=0
          indx=[]
          FKP = []
          for pr in Pclass:
              if pr == 1:
                  row = row + 1
                  df.loc[row] = [j, keypoints[j].pt[0],keypoints[j].pt[1], i]
                  FKP.append(keypoints[j])
                  indx.append(j)

              j=j+1
          pts=[(m.floor(i.pt[0]), m.floor(i.pt[1])) for i in FKP]

          for item in pts:
            data = data.append(pd.DataFrame({'frame': i, 'x': item[0], 'y': item[1],}, index=[0]), ignore_index=True)
            data.to_csv(path + "/detect.csv")
            cv2.rectangle(frame,(item[0]-grabsize, item[1]-grabsize), (item[0]+grabsize, item[1]+grabsize),(0,255,0),thickness = 2)
          out.write(frame)
        print("...SUCCESSFULLY DETECTED {} AND STORED mothe_detect.avi AND CSV...".format(self.movie_name))
        cap.release()
        out.release()


    class yolo:
        def _interval_overlap(interval_a, interval_b):
            x1, x2 = interval_a
            x3, x4 = interval_b

            if x3 < x1:
                if x4 < x1:
                    return 0
                else:
                    return min(x2,x4) - x1
            else:
                if x2 < x3:
                     return 0
                else:
                    return min(x2,x4) - x3

        def bbox_iou(box1, box2):

            intersect_w = mothe.yolo._interval_overlap([box1[0], box1[2]], [box2[0], box2[2]])
            intersect_h = mothe.yolo._interval_overlap([box1[1], box1[3]], [box2[1], box2[3]])

            intersect = intersect_w * intersect_h

            w1, h1 = box1[2]-box1[0], box1[3]-box1[1]
            w2, h2 = box2[2]-box2[0], box2[3]-box2[1]

            union = w1*h1 + w2*h2 - intersect

            return float(intersect) / union

        def do_nms(new_boxes, nms_thresh):
            # do nms
            sorted_indices = np.argsort(-new_boxes[:,4])
            boxes=new_boxes.tolist()

            for i in range(len(sorted_indices)):

                index_i = sorted_indices[i]

                if new_boxes[index_i,4] == 0: continue

                for j in range(i+1, len(sorted_indices)):
                    index_j = sorted_indices[j]
                    # anything with certainty above 1 is untouchable
                    if boxes[index_j][4]>1:
                        continue
                    if mothe.yolo.bbox_iou(boxes[index_i][0:4], boxes[index_j][0:4]) > nms_thresh:
                        new_boxes[index_j,4] = 0

            return

        def convert_bbox_to_kfx(bbox):
            """
            Takes a bounding box in the form [x1,y1,x2,y2] and returns z in the form
            [x,y,s,r] where x,y is the centre of the box and s is the scale/area and r is
            the aspect ratio
            """
            w = bbox[2]-bbox[0]
            h = bbox[3]-bbox[1]
            x = bbox[0]+w/2.
            y = bbox[1]+h/2.
            return np.array([x,y,w,h]).reshape((4,1))

        def convert_kfx_to_bbox(x):
            """
            Takes a bounding box in the centre form [x,y,s,r] and returns it in the form
            [x1,y1,x2,y2] where x1,y1 is the top left and x2,y2 is the bottom right
            """
            w=max(0.0,x[2])
            h=max(0.0,x[3])
            return np.array([x[0]-w/2.,x[1]-h/2.,x[0]+w/2.,x[1]+h/2.]).reshape((1,4))


        class KalmanBoxTracker(object):
            """
            This class represents the internel state of individual tracked objects observed as bbox.
            """
            count = 0
            def __init__(self,bbox):
                """
                Initialises a tracker using initial bounding box.
                """
                #define constant velocity model
                self.kf = KalmanFilter(dim_x=8, dim_z=4)
                self.kf.F = np.array([[1,0,0,0,1,0,0.5,0],[0,1,0,0,0,1,0,0.5],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,1,0],[0,0,0,0,0,1,0,1],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]])
                self.kf.H = np.array([[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0]])

                self.kf.R[:,:] *= 25.0 # set measurement uncertainty for positions
                self.kf.Q[:2,:2] = 0.0 # process uncertainty for positions is zero - only moves due to velocity, leave process for width height as 1 to account for turning
                self.kf.Q[2:4,2:4] *= 0.1 # process uncertainty for width/height for turning
                self.kf.Q[4:6,4:6] = 0.0 # process uncertainty for velocities is zeros - only accelerates due to accelerations
                self.kf.Q[6:,6:] *= 0.01 # process uncertainty for acceleration
                self.kf.P[4:,4:] *= 5.0 # maximum speed

                z=mothe.yolo.convert_bbox_to_kfx(bbox)
                self.kf.x[:4] = z
                self.time_since_update = 0
                self.id = mothe.yolo.KalmanBoxTracker.count
                mothe.yolo.KalmanBoxTracker.count += 1
                self.hits = 1
                self.hit_streak = 1
                self.age = 1
                self.score = bbox[4]

            def update(self,bbox):
                """
                Updates the state vector with observed bbox.
                """
                self.time_since_update = 0
                self.hits += 1
                self.hit_streak += 1
                self.score = (self.score*(self.hits-1.0)/float(self.hits)) + (bbox[4]/float(self.hits))
                z = mothe.yolo.convert_bbox_to_kfx(bbox)
                self.kf.update(z)

            def predict(self):
                """
                Advances the state vector and returns the predicted bounding box estimate.
                """
                self.kf.predict()
                self.age += 1
                if(self.time_since_update>0):
                    self.hit_streak = 0
                self.time_since_update += 1

            def get_state(self):
                """
                Returns the current bounding box estimate.
                """
                return convert_kfx_to_bbox(self.kf.x)

            def get_distance(self, y):
                """
                Returns the mahalanobis distance to the given point.
                """
                b1 = convert_kfx_to_bbox(self.kf.x[:4])[0]
                return (bbox_iou(b1,y))

        def associate_detections_to_trackers(detections,trackers,iou_threshold = 0.3):
            """
            Assigns detections to tracked object (both represented as bounding boxes)
            Returns 3 lists of matches, unmatched_detections and unmatched_trackers
            """
            if(len(trackers)==0):
                return np.empty((0,2),dtype=int), np.arange(len(detections)), np.empty((0,5),dtype=int)

            iou_matrix = np.zeros((len(detections),len(trackers)),dtype=np.float32)
            id_matrix = np.zeros((len(detections),len(trackers)),dtype=np.float32)
            scale_id = 0.5

            for d,det in enumerate(detections):
                for t,trk in enumerate(trackers):
                    trackBox = mothe.yolo.convert_kfx_to_bbox(trk.kf.x[:4])[0]
                    iou_matrix[d,t] = mothe.yolo.bbox_iou(trackBox, det)
                    id_matrix[d,t] = scale_id*det[4]

            matched_indices = linear_sum_assignment(-iou_matrix-id_matrix)
            matched_indices = np.asarray(matched_indices)
            matched_indices = np.transpose(matched_indices)

            unmatched_detections = []
            for d,det in enumerate(detections):
                if(d not in matched_indices[:,0]):
                    unmatched_detections.append(d)

            unmatched_trackers = []
            for t,trk in enumerate(trackers):
                if(t not in matched_indices[:,1]):
                    unmatched_trackers.append(t)

            #filter out matched with low probability
            matches = []
            for m in matched_indices:
                if(iou_matrix[m[0],m[1]]<iou_threshold):
                    unmatched_detections.append(m[0])
                    unmatched_trackers.append(m[1])
                else:
                    matches.append(m.reshape(1,2))

            if(len(matches)==0):
                matches = np.empty((0,2),dtype=int)
            else:
                matches = np.concatenate(matches,axis=0)

            return matches, np.array(unmatched_detections), np.array(unmatched_trackers)



        class yoloTracker(object):
            def __init__(self,max_age=1,track_threshold=0.5, init_threshold=0.9, init_nms=0.0,link_iou=0.3 ):
                """
                Sets key parameters for YOLOtrack
                """
                self.max_age = max_age # time since last detection to delete track
                self.trackers = []
                self.frame_count = 0
                self.track_threshold = track_threshold # only return tracks with average confidence above this value
                self.init_threshold = init_threshold # threshold confidence to initialise a track, note this is much higher than the detection threshold
                self.init_nms = init_nms # threshold overlap to initialise a track - set to 0 to only initialise if not overlapping another tracked detection
                self.link_iou = link_iou # only link tracks if the predicted box overlaps detection by this amount
                mothe.yolo.KalmanBoxTracker.count = 0

            def update(self,dets):
                """
                Params:
                  dets - a numpy array of detections in the format [[x1,y1,x2,y2,score],[x1,y1,x2,y2,score],...]
                Requires: this method must be called once for each frame even with empty detections.
                Returns a similar array, where the last column is the object ID.

                NOTE: The number of objects returned may differ from the number of detections provided.
                """
                self.frame_count += 1
                #get predicted locations from existing trackers.
                trks = np.zeros((len(self.trackers),5))

                ret = []
                for t,trk in enumerate(self.trackers):
                    self.trackers[t].predict()


                matched, unmatched_dets, unmatched_trks = mothe.yolo.associate_detections_to_trackers(dets,self.trackers, self.link_iou)

                #update matched trackers with assigned detections
                for t,trk in enumerate(self.trackers):
                    if(t not in unmatched_trks):
                        d = matched[np.where(matched[:,1]==t)[0],0]
                        trk.update(dets[d,:][0])
                        dets[d,4]=2.0 # once assigned we set it to full certainty

                #add tracks to detection list
                for t,trk in enumerate(self.trackers):
                    if(t in unmatched_trks):

                        d = mothe.yolo.convert_kfx_to_bbox(trk.kf.x)[0]
                        d = np.append(d,np.array([2]), axis=0)
                        d = np.expand_dims(d,0)
                        dets = np.append(dets,d, axis=0)

                if len(dets)>0:
                    dets = dets[dets[:,4]>self.init_threshold]
                    mothe.yolo.do_nms(dets,self.init_nms)
                    dets= dets[dets[:,4]<1.1]
                    dets= dets[dets[:,4]>0]

                for det in dets:
                    trk = mothe.yolo.KalmanBoxTracker(det[:])
                    self.trackers.append(trk)

                i = len(self.trackers)
                for trk in reversed(self.trackers):
                    i -= 1
                    #remove dead tracklet
                    if(trk.time_since_update > self.max_age):
                        self.trackers.pop(i)

                for trk in (self.trackers):
                    d = mothe.yolo.convert_kfx_to_bbox(trk.kf.x)[0]
                    if ((trk.time_since_update < 1) and (trk.score>self.track_threshold)):
                        ret.append(np.concatenate((d,[trk.id])).reshape(1,-1))

                if(len(ret)>0):
                    return np.concatenate(ret)
                return np.empty((0,5))


    def tracking(self, movie_name, model_name):
        self.movie_name = movie_name
        self.model_name = model_name
        with open("config.yml", "r") as stream:
            config_data= yaml.safe_load(stream)
        root_dir = config_data["root_dir"]
        grabsize = int(config_data["annotation_size"])
        threshold_value1 = (int(config_data["threshold_value1"]))
        threshold_value2 = (int(config_data["threshold_value2"]))
        steps = int(config_data["step_for_dt"])

        #get screen resolution
        # screen_width = int(root.winfo_screenwidth())
        # screen_height = int(root.winfo_screenheight())

        movieName =  self.movie_name
        cap = cv2.VideoCapture(movieName)

        nframe =cap.get(cv2.CAP_PROP_FRAME_COUNT)
        nx = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        ny = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Craete data frames to store x and y coords of the identified blobs, rows for each individual column for each frame
        df = pd.DataFrame(columns=['c_id','x_px','y_px','frame'])
        data = pd.DataFrame(columns= ['frame', 'lx', 'ty', 'rx', 'by', 'id'])
        i=0
        row = 0
        alt = 100#int(input("Enter height of video(integer):  "))
        # work out size of box if box if 32x32 at 100m
        grabSize = int(m.ceil((100/alt)*12))
        #Load model
        from keras.models import load_model
        bb_model = load_model(root_dir+ "/" + self.model_name)
        #Video writer object
        out = cv2.VideoWriter(root_dir+'/mothe_track.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 24, (nx,ny))
        tracker = mothe.yolo.yoloTracker(max_age=20, track_threshold=0.6, init_threshold=0.8, init_nms=0.0, link_iou=0.1)

        #Define a distance function
        def distance(point1, point2):
          dist=m.sqrt(((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2))
          return dist
        lx=[]
        ty=[]
        rx=[]
        by=[]
        uid=[]
        frameid=[]

        while(cap.isOpened() & (i<(nframe-steps))):

          i = i + steps
          print("[UPDATING.....]{}th/{} frame detected and stored".format(i, nframe))
          cap.set(cv2.CAP_PROP_POS_FRAMES,i)
          ret, frame = cap.read()
          if ret == False:
              continue
          grayF = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          #Equalize image
          #gray = cv2.equalizeHist(gray)
          #remove noise
          gray = cv2.medianBlur(grayF,5)
          #Invert image
          gray = cv2.bitwise_not(gray)

          # Blob detection
          # Setup SimpleBlobDetector parameters.
          params = cv2.SimpleBlobDetector_Params()

          # Change thresholds
          params.minThreshold = threshold_value1;
          params.maxThreshold = threshold_value2;

          # Filter by Circularity
          params.filterByCircularity = False
          #params.minCircularity = 0.1

          # Filter by Convexity
          params.filterByConvexity = False
          #params.minConvexity = 0.87

          # Filter by Inertia
          params.filterByInertia = False

          # Create a detector with the parameters
          ver = (cv2.__version__).split('.')
          if int(ver[0]) < 3 :
            detector = cv2.SimpleBlobDetector(params)
          else :
            detector = cv2.SimpleBlobDetector_create(params)

          # Detect blobs.
          keypoints = detector.detect(gray)

          testX = np.ndarray(shape=(len(keypoints),40,40,3), dtype='uint8', order='C')
          j = 0
          for keyPoint in keypoints:

            ix = keyPoint.pt[0]
            iy = keyPoint.pt[1]
            #Classification: here draw boxes around keypints and classify them using svmClassifier
            tmpImg=frame[max(0,int(iy-grabsize)):min(ny,int(iy+grabsize)), max(0,int(ix-grabsize)):min(nx,int(ix+grabsize))].copy()

            tmpImg1=cv2.resize(tmpImg,(40,40))
            testX[j,:,:,:]=tmpImg1
            j = j + 1
          testX = testX.reshape(-1, 40,40, 3)
          testX = testX.astype('float32')
          testX = testX / 255.
          pred = bb_model.predict(testX)
          Pclass = np.argmax(np.round(pred),axis=1)
          track_class=[]
          for certainty in pred:
            track_class.append(certainty[1])
          tictac=[]
          for tic, tac in zip(Pclass, track_class):
            tictac.append([tic, tac])
          #print(tictac)
          #print((Pclass),(track_class))
          j=0
          indx=[]
          FKP = []
          detection= []
          confidence= []
          for pr in tictac:
              if pr[0] == 1:
                  row = row + 1
                  df.loc[row] = [j, keypoints[j].pt[0],keypoints[j].pt[1], i]
                  FKP.append(keypoints[j])
                  detection.append((keypoints[j], pr[1]))

                  indx.append(j)

              j=j+1

          pts=[(m.floor(i.pt[0]), m.floor(i.pt[1])) for i in FKP]
          detections= [(m.floor(i.pt[0])-grabsize, m.floor(i.pt[1])-grabsize, m.floor(i.pt[0])+grabsize,m.floor(i.pt[1])+grabsize, j) for i, j in detection]
        #  print(detections)
          tracks = tracker.update(np.asarray(detections))
          save_output= True
          full_warp = np.eye(3, 3, dtype=np.float32)

          for item in tracks:
              data = data.append(pd.DataFrame({'uid': item[4], 'lx': item[0], 'by': item[1], 'rx' : item[2], 'ty' : item[3]}, index=[0]), ignore_index=True)
              data.to_csv("track.csv")

          for ids in tracks:
            np.random.seed(int(ids[4])) # show each track as its own colour - note can't use np random number generator in this code
            r = np.random.randint(256)
            g = np.random.randint(256)
            b = np.random.randint(256)
            lx.append(ids[0])
            ty.append(ids[1])
            rx.append(ids[2])
            by.append(ids[3])
            uid.append(ids[4])
            frameid.append(i)
            cv2.rectangle(frame,(int(ids[0]), int(ids[1])), (int(ids[2]), int(ids[3])),(b,g,r), 2)
            cv2.putText(frame, str(int(ids[4])),(int(ids[2])+5, int(ids[3])-5),0, 5e-3 * 200, (b, g, r),2)

          out.write(frame)
        data['frame']=frameid
        data['lx']=lx
        data['ty']=ty
        data['rx']=rx
        data['by']=by
        data['id']=uid
        data.to_csv("video_track.csv")
        print("...SUCCESSFULLY TRACKED {} AND STORED mothe_track.avi AND CSV...".format(self.movie_name))

        cap.release()
        out.release()

    def generate_dataset(self, movie_name, class_name, step_for_dg):
        self.movie_name = movie_name
        self.class_name = class_name
        self.step_for_dg = step_for_dg
        with open("config.yml", "r") as stream:
            config_data= yaml.safe_load(stream)
        path = config_data["root_dir"]
        grab_size = int(config_data["annotation_size"])
        ix, iy = -1, -1
        def click_crop(event, x, y, flags, param):
            global ix, iy
            if event == cv2.EVENT_LBUTTONDOWN:
                ix, iy = x, y
                keypoints.append((ix, iy)) 
        if self.class_name not in os.listdir():
            os.mkdir(self.class_name)     
        cap = cv2.VideoCapture(path+ "/" + self.movie_name)
        nframes =cap.get(cv2.CAP_PROP_FRAME_COUNT)          
        i = 0
        steps = int(self.step_for_dg)
        while cap.isOpened() and i<(nframes-steps):
            i=i+steps
            print("...PROCESSING {}/{} FRAME...".format(i, nframes))
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret == False:
                continue
            clone = frame.copy()
            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("image", 1920, 1080)
            cv2.setMouseCallback("image", click_crop)
            keypoints = []
            while True:
                cv2.imshow("image", clone)
                key = cv2.waitKey(20) & 0xFF
                if key == ord("n"):
                    break 
                elif key == ord("u"):
                    if len(keypoints)==0:
                        print("...NO POINTS HAVE BEEN SELECTED...")
                        break
                    else:
                        print("...DELETED POINT {}".format(keypoints[-1]))
                        keypoints.pop(-1)
                        print(keypoints)
                        clone = frame.copy()
                        for point in keypoints:
                            cv2.rectangle(clone, (point[0]-(round(grab_size/2)+1), point[1]-(round(grab_size/2)+1)), (point[0]+(round(grab_size/2)+1), point[1]+(round(grab_size/2)+1)), (0, 255, 0), 2)

                elif key == 27:
                    i = (nframes)
                    print("...GENERATION TERMINATED...")
                    break
                elif key == ord("s"):
                    print("...SAVING {} DATA POINTS FROM {} FRAME...".format(len(keypoints), i))
                    for (enum,keys) in enumerate(keypoints):
                        crop_img = frame[keys[1]-grab_size:keys[1]+(grab_size),keys[0]-grab_size:keys[0]+(grab_size)]
                        cv2.imwrite(path + "/" + self.class_name + "/" + "{}-{}-f{}-k{}.jpg".format(self.movie_name, self.class_name, i, enum), crop_img)
                    break
                for point in keypoints:
                    cv2.rectangle(clone, (point[0]-(round(grab_size/2)+1), point[1]-(round(grab_size/2)+1)), (point[0]+(round(grab_size/2)+1), point[1]+(round(grab_size)/2)+1), (0, 255, 0), 2)
            cv2.destroyAllWindows()

    












if __name__=="__main__":
    mothe = mothe("/home/elcucuy/mothe/mothe", 50, 150, 15)
    configuration = mothe.set_config("wasp_original.MTS")
    mothe.generate_dataset("wasp_original.MTS", "yes", 15)
    # mothe.train_model()
    # mothe.detection("wasp_original.MTS", "wasp_model.h5py")
    # mothe.tracking("wasp_original.MTS", "wasp_model.h5py")
