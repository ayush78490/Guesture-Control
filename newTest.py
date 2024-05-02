import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detactor = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y=0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame_height, frame_wdth, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detactor.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        # Create a transparent image to draw landmarks
        transparent_img = frame.copy()
        transparent_img = cv2.cvtColor(transparent_img, cv2.COLOR_BGR2BGRA)
        transparent_img[:, :, 3] = 0  # Set alpha channel to 0

        for hand in hands:
            # Draw landmarks on the transparent image
            drawing_utils.draw_landmarks(transparent_img, hand, connection_drawing_spec=None, landmark_drawing_spec=drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1))

            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x=int(landmark.x*frame_wdth)
                y=int(landmark.y*frame_height)
                if id==8:
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(0,255,255))
                    index_x=screen_width/frame_wdth*x
                    index_y=screen_height/frame_height*y
                    pyautogui.moveTo(index_x,index_y)
                if id==4:
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(0,255,255))
                    thumb_x=screen_width/frame_wdth*x
                    thumb_y=screen_height/frame_height*y
                    print(abs(thumb_x-index_x))
                    if abs(thumb_x-index_x)<20:
                        pyautogui.click()
                        pyautogui.sleep(1)

        # Merge the transparent image with the original frame
        frame = cv2.addWeighted(frame, 1, transparent_img, 0.5, 0)

    cv2.imshow('virtualMouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
