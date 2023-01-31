import tkinter as tk
import pyautogui
import cv2
import mediapipe as mp
import time

def start_moving():
  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles
  mp_hands = mp.solutions.hands

  IMAGE_FILES = []
  with mp_hands.Hands(
      static_image_mode=True,
      max_num_hands=2,
      min_detection_confidence=0.5) as hands:
    for idx, file in enumerate(IMAGE_FILES):
      image = cv2.flip(cv2.imread(file), 1)
      results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
      print('Handedness:', results.multi_handedness)
      if not results.multi_hand_landmarks:
        continue
      image_height, image_width, _ = image.shape
      annotated_image = image.copy()
      for hand_landmarks in results.multi_hand_landmarks:
        print('hand_landmarks:', hand_landmarks)
        print(
            f'Index finger tip coordinates: (',
            f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
            f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
        )
        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
      cv2.imwrite(
          '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
      if not results.multi_hand_world_landmarks:
        continue
      for hand_world_landmarks in results.multi_hand_world_landmarks:
        mp_drawing.plot_landmarks(
          hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)


  cap = cv2.VideoCapture(0)
  with mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        continue

      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          image_height, image_width, _ = image.shape
          x_one=2000-(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 2000)
          y_two=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 1100
          pyautogui.moveTo(x_one, y_two)
          mp_drawing.draw_landmarks(
              image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
      cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
      if cv2.waitKey(5) & 0xFF == 27:
        
        break
  cap.release()
  cv2.destroyAllWindows()

def stop_moving():
    root.destroy()


def update_coordinates():
    while True:
        entry_x.delete(0, tk.END)
        entry_x.insert(0, pyautogui.position()[0])
        entry_y.delete(0, tk.END)
        entry_y.insert(0, pyautogui.position()[1])
        root.update()
        time.sleep(0.1)

root = tk.Tk()
root.title("Mouse Mover")
root.geometry("400x200")

frame_input = tk.Frame(root)
frame_input.pack(pady=30)

label_x = tk.Label(frame_input, text="X Coordinate:", font=("Helvetica", 12))
label_x.pack(side="left")

entry_x = tk.Entry(frame_input, font=("Helvetica", 12), width=10)
entry_x.pack(side="left")

label_y = tk.Label(frame_input, text="Y Coordinate:", font=("Helvetica", 12))
label_y.pack(side="left", padx=30)

entry_y = tk.Entry(frame_input, font=("Helvetica", 12), width=10)
entry_y.pack(side="left")

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=30)

button_start = tk.Button(frame_buttons, text="Start", font=("Helvetica", 12), command=start_moving)
button_start.pack(side="left", padx=30)

button_stop = tk.Button(frame_buttons, text="Stop", font=("Helvetica", 12), command=stop_moving)
button_stop.pack(side="left")

root.after(0, update_coordinates)
root.mainloop()

