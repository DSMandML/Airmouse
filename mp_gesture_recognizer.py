import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2


class GestureRecognizer:
    def __init__(self):
        self.base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
        self.gesture_recognition_options = vision.GestureRecognizerOptions(base_options=self.base_options,
                                           running_mode=mp.tasks.vision.RunningMode.VIDEO, num_hands=2)
        self.model = vision.GestureRecognizer.create_from_options(self.gesture_recognition_options)
        self.frame_idx = 0

    def __call__(self, input):
        result = self.model.recognize_for_video(input, self.frame_idx)
        self.frame_idx +=1
        return result

    def draw_landmarks_on_image(self, rgb_image, detection_result):
        hand_landmarks_list = detection_result.hand_landmarks
        hand_gesture_list = detection_result.gestures
        handedness_list = detection_result.handedness
        annotated_image = np.copy(rgb_image)

        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            cur_gesture = hand_gesture_list[idx][0].category_name
            handedness = handedness_list[idx]

            # Draw the hand landmarks.
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style())

            # Get the top left corner of the detected hand's bounding box.
            height, width, _ = annotated_image.shape
            x_coordinates = [landmark.x for landmark in hand_landmarks]
            y_coordinates = [landmark.y for landmark in hand_landmarks]
            text_x = int(min(x_coordinates) * width)
            text_y = int(min(y_coordinates) * height) - 10

            # Draw handedness (left or right hand) on the image.
            cv2.putText(annotated_image, f"{handedness[0].category_name}", (text_x, text_y),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(annotated_image, f"{cur_gesture}", (text_x, text_y - 20),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)

        return annotated_image


if __name__ == '__main__':
    vid_cap = cv2.VideoCapture(0)
    gesture_recognizer = GestureRecognizer()

    while True:
        success, image_np = vid_cap.read()
        image_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_np)
        if not success:
            break
        gesture_recognizer(image_mp)
        result = gesture_recognizer.get_result()
        annotated_image = gesture_recognizer.draw_landmarks_on_image(image_mp.numpy_view(), result)
        cv2.imshow('output', annotated_image)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            print('Exiting..!!')
            break
