import cv2
import numpy as np
from os.path import splitext

from jcopvision.exception import MediaToArrayError


class MediaReader:
    """
    An all around media reader built on top of opencv.


    === Example Usage ===
    media = MediaReader("video.mp4")
    for frame in media.read():
        # do something
    media.close()
    """
    def __init__(self, source="webcam"):
        self.input_type, self.cam = self._parse_source(source)
        self._parse_prop()

    def _parse_source(self, source):
        _ext = lambda source: splitext(source)[-1]
        source = 0 if source == "webcam" else source

        if source == 0:
            input_type = "camera"
            cam = cv2.VideoCapture(source)
        elif _ext(source) in [".mp4", ".avi"]:
            input_type = "video"
            cam = cv2.VideoCapture(source)
        elif _ext(source) in [".bmp", ".dib", ".jpg", ".jpeg", ".jp2", ".jpe", ".png", ".pbm", ".pgm",
                              ".ppm", ".sr", ".ras", ".tiff", ".tif"]:
            input_type = "image"
            cam = cv2.imread(source)
        else:
            raise Exception("File type not supported")
        return input_type, cam

    def _parse_prop(self):
        if self.input_type == "image":
            h, w, c = self.cam.shape
            self.aspect_ratio = w / h
            self.height = int(h)
            self.width = int(w)
        else:
            self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.aspect_ratio = self.width / self.height
            self.frame_count = self.cam.get(cv2.CAP_PROP_FRAME_COUNT)
            self.frame_rate = self.cam.get(cv2.CAP_PROP_FPS)

    def read(self):
        if self.input_type == "image":
            return self.cam
        else:
            return self._video_reader()

    def close(self):
        if self.input_type in ['video', "camera"]:
            self.cam.release()

    def _video_reader(self):
        while True:
            cam_on, frame = self.cam.read()
            if cam_on:
                yield frame
            else:
                break

    def to_array(self, color_model="rgb"):
        if self.input_type == "video":
            frames = [frame for frame in self.read()]
            frames = np.array(frames).transpose(0, 3, 1, 2)
            if color_model == "rgb":
                frames = frames[:, ::-1, :, :]
            return frames
        else:
            raise MediaToArrayError("Image / webcam stream could not be converted to array. Input should be a video.")

