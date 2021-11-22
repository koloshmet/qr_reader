from PIL import Image
import cv2


class Camera(object):
    def __init__(self, cam):
        self._cap = cv2.VideoCapture(cam)

    def get_image(self) -> Image.Image:
        ret, cap_frame = self._cap.read()
        rgb_im = cv2.cvtColor(cap_frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_im)

    def close(self):
        self._cap.release()

