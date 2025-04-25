import cv2
import mediapipe as mp
import time
import math




class pose_detector():
    def __init__(self, mode = False, detection_con = 0.5, track_con = 0.5):
        self.mode = mode
        # self.up_body = up_body           ## these two line are don't needed, it is only use for the old version of mp
        # self.smooth = smooth
        self.detection_con = detection_con
        self.track_con = track_con
    

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=self.mode, 
                                      min_detection_confidence=self.detection_con, 
                                      min_tracking_confidence=self.track_con)
        self.mp_draw = mp.solutions.drawing_utils
        
        
        
        
    def find_pose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # convert the img BGR to RGB
        self.results = self.pose.process(imgRGB)  
        # print(results.pose_landmarks)  
        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                
        return img
            
            
    def find_position(self, img, draw = True):  
        self.lm_list = [] 
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])     # appending the value into the empty list
                if draw:
                    cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
        return self.lm_list
    
    def find_angle(self, img, p1, p2, p3, draw = True):
        ## get the landmarks
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        x3, y3 = self.lm_list[p3][1:]
        
        ## calculate the angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360                           ## converting to absolute angle
        # print(angle)
        
        ## draw the points for better visualization
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 0, 0), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            # cv2.putText(img, str(int(angle)), (x2, y2 - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)  ## it will show the angle between the points
            
        return angle
        
        
        

def main():
    cap = cv2.VideoCapture('V:/part 10/1.mp4')  # Try different indices if needed (0, 1, 2, ......)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    p_time = 0
    c_time = 0

    detector = pose_detector()         ## creating an instance ofbthe pose_detector class

    while True:
        success, img = cap.read()
        
        
        img = detector.find_pose(img)
        lm_list = detector.find_position(img)
        if len(lm_list) != 0:
            print(lm_list)                       # by doing this we get a particular point's position from  the video clip
        
        
        # lm_list = detector.find_position(img, draw = False)      # we are tracking a particular point of the body
        # if len(lm_list) != 0:
            # print(lm_list[14]) 
            # cv2.circle(img, (lm_list[14][1], lm_list[14][2]), 15, (0, 255, 0), cv2.FILLED)
                             
        
        

        if not success or img is None:
            print("Error: Failed to capture image")  
            break  # Exit if no frame is captured
    
    
        c_time = time.time()
        fps = 1/(c_time - p_time)
        p_time = c_time
    
    
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    
    
    
        cv2.imshow("Image", img)  

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Press 'q' to exit
    




if __name__ == "__main__":
    main()
    
