from mp_gesture_recognizer import GestureRecognizer
from pointer_controller import PointerController
from Config import Config
import mediapipe as mp
from enum import Enum
import numpy as np
import math
import cv2


class State(Enum):
    idle = 0
    initializing = 1
    running = 2



class AirMouse:
    def __init__(self, finger_config, source_id=0):
        self.vid_cap = cv2.VideoCapture(source_id)
        success, image_np = self.vid_cap.read()
        assert success, f'Camera failed to open...'
        self.finger_config = finger_config
        self.gesture_recognizer = GestureRecognizer()
        self.pointer = PointerController(image_np.shape)
        self.state = State.idle
        self.cur_hand = None
        self.state_init_counter = 0
        self.no_hand_counter = 0
        self.no_hand_thresh = 2
        self.image_np = None
        self.max_frames_to_lock = 3
        self.thresh_finger_movement = 3.0
        self.finger_lock_counter = 0
        self.click_prev_valid = False
        self.click_counter = 0
        self.click_detection_thresh = 40.0
        self.short_click_thresh = 4.0
        self.long_click_thresh = 15.0
        self.thumb_index_tip_dist_thresh = 30.0
        self.start_drag = False
        self.start_drag_counter = 0
        self.start_drag_thresh = 5
        self.close_app_counter = 0
        self.close_app_thresh = 20
        self.start_scroll = False
        self.data = None
        self.prev_data = None

    def init_state(self, hand):
        self.cur_hand = hand
        self.state = State.running

    def reset_state(self):
        self.data = None
        self.prev_data = None
        self.cur_hand = None
        self.state = State.idle

    def read_frame(self):
        success, self.image_np = self.vid_cap.read()
        self.image_np = cv2.cvtColor(self.image_np, cv2.COLOR_BGR2RGB)
        assert success, f'Failed to read image. Check Camera!!'
        image_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.image_np)
        return image_mp

    def draw_landmarks_on_image(self, image_mp, recognition_result):
        output_img = self.gesture_recognizer.draw_landmarks_on_image(image_mp.numpy_view(), recognition_result)
        return output_img

    def perform_action(self, recognition_data):
        if not len(recognition_data.gestures):
            if self.state != State.idle:
                if self.no_hand_counter > self.no_hand_thresh:
                    self.reset_state()
                self.no_hand_counter += 1
            return
        self.no_hand_counter = 0

        if self.state == State.idle:
            self.state = State.initializing

        self.data = self.restructure_output(recognition_data)
        gesture, gesture_prob = self.data[0]['gesture']
        if gesture_prob < 0.5:
            return

        if self.state == State.initializing:
            self.lock_pointer_to_finger()
        elif self.state == State.running:
            self.finger_lock_counter = 0
            if self.prev_data is not None:
                if gesture == 'Thumb_Up':
                    if self.close_app_counter > self.close_app_thresh:
                        exit(0)
                    self.close_app_counter += 1
                else:
                    self.close_app_counter = 0

                if gesture != 'None':
                    self.start_scroll = False
                if gesture == 'None':
                    self.pointer.reset_move()
                    self.check_click_action()
                    self.check_and_perform_scroll()
                elif gesture == 'Victory':
                    if not self.start_drag and self.start_drag_counter > self.start_drag_thresh:
                        self.pointer.left_click_hold()
                        self.start_drag = True
                    else:
                        self.start_drag_counter += 1

                    if self.start_drag:
                        self.move_pointer_from_finger()
                elif gesture == 'Pointing_Up':
                    if self.start_drag_counter:
                        self.start_drag_counter = 0
                    if self.start_drag:
                        self.pointer.left_click_release()
                        self.start_drag = False
                    elif self.click_counter > self.long_click_thresh:
                        self.pointer.right_click()
                    elif self.click_counter > self.short_click_thresh:
                        self.pointer.left_doubleclick()
                    else:
                        self.move_pointer_from_finger()
                    self.click_prev_valid = False
                    self.click_counter = 0

            self.prev_data = self.data
        return

    def restructure_output(self, data):
        output_data = []
        for gesture, landmarks, metadata in zip(data.gestures, data.hand_landmarks, data.handedness):
            landmarks_np = np.array(list((data.x*self.image_np.shape[1], data.y*self.image_np.shape[0]) for data in landmarks))
            w, h = np.max(landmarks_np, axis=0) - np.min(landmarks_np, axis=0)
            output_data.append({'hand_side': metadata[0].category_name,
                                'score': metadata[0].score,
                                'gesture': (gesture[0].category_name, gesture[0].score),
                                'landmark': landmarks_np,
                                'area': w*h})
        output_data.sort(key=lambda x: x['area'], reverse=True)
        return output_data

    def check_click_action(self):
        if self.prev_data[0]['gesture'][0] == 'Pointing_Up':
            self.click_prev_valid = True
            self.click_counter = 0

        if self.click_prev_valid:
            landmark_data = self.data[0]['landmark']
            thumb_dist = abs(landmark_data[5][0]-landmark_data[4][0])
            if thumb_dist > self.click_detection_thresh:
                self.click_counter += 1
        return

    def check_and_perform_scroll(self):
        if self.prev_data[0]['gesture'][0] == 'Open_Palm':
            self.start_scroll = True
            self.pointer.reset_scroll()

        if self.start_scroll:
            landmark_data = self.data[0]['landmark']
            thumb_index_tip_dist = np.sqrt(sum((landmark_data[8]-landmark_data[4])**2))
            if thumb_index_tip_dist < self.thumb_index_tip_dist_thresh:
                prev_loc = self.prev_data[0]['landmark'][self.finger_config.finger_to_lock]
                cur_loc = self.data[0]['landmark'][self.finger_config.finger_to_lock]
                scrollx, scrolly = prev_loc - cur_loc
                self.pointer.vscroll(scrolly)
                self.pointer.hscroll(scrollx)
        return

    def lock_pointer_to_finger(self):
        if self.finger_lock_counter > self.max_frames_to_lock:
            self.init_state(self.data[0]['hand_side'])
            return

        if self.prev_data is None:
            self.prev_data = self.data
        else:
            prev_loc = self.prev_data[0]['landmark'][self.finger_config.finger_to_lock]
            cur_loc = self.data[0]['landmark'][self.finger_config.finger_to_lock]
            finger_movment = math.sqrt(sum((cur_loc - prev_loc)**2))

            if finger_movment > self.thresh_finger_movement:
                self.finger_lock_counter = 0
            else:
                self.finger_lock_counter += 1
            self.prev_data = self.data
        return

    def move_pointer_from_finger(self):
        prev_loc = self.prev_data[0]['landmark'][self.finger_config.finger_to_lock]
        cur_loc = self.data[0]['landmark'][self.finger_config.finger_to_lock]
        move_x, move_y = prev_loc - cur_loc
        self.pointer.move_rel_pos(move_x, -move_y)
        return


def run():
    finger_config = Config()
    air_mouse = AirMouse(finger_config, source_id=0)

    while True:
        input_img = air_mouse.read_frame()
        recognition_result = air_mouse.gesture_recognizer(input_img)
        air_mouse.perform_action(recognition_result)

        annotated_image = air_mouse.draw_landmarks_on_image(input_img, recognition_result)

        cv2.imshow('output', annotated_image[:, :, ::-1])
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            print('Exiting..!!')
            break


if __name__ == '__main__':
    run()