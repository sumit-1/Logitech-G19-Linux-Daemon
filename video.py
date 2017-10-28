from logitech.g19 import G19
import time
import os
import random
import cv2
import ctypes
import subprocess
import signal
import sys

class AUDIOPLAYER:
    def __init__(self):
        pass

    def play(self, path):
        self.audio = subprocess.Popen(['mplayer', '-msglevel','all=-1', '-novideo', path], stderr=subprocess.PIPE)

    def stop(self):
        self.audio.send_signal(2)


class VIDEOPLAYER:
    def __init__(self):
        self.libc = ctypes.CDLL('libc.so.6')
        self.lg19 = G19()


    def play(self, path):
        videoFile = cv2.VideoCapture(path)
        nFrames = int(videoFile.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        fps = videoFile.get(cv2.cv.CV_CAP_PROP_FPS)
        frame_gap = 1/fps
        uexpected_time = int(frame_gap * 1000000)
        usleep = uexpected_time

        while (videoFile.isOpened()):
            t1 = time.time()
            self.libc.usleep(usleep)
            try:
                ret, frame = videoFile.read()
                frame = cv2.resize(frame, (320, 240))
                frame = cv2.transpose(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR565)
                data = frame.flatten('C').tolist()
            except:
                pass
            self.lg19.send_frame(data)
            t2 = time.time()
            time_taken = t2-t1
            utime_taken = int(time_taken*1000000)
            uextra_time = utime_taken - uexpected_time
            usleep = int(usleep - uextra_time)
            if usleep < 1:
                usleep = 1


class ROULETTE:
    def __init__(self, path=''):
        self.root = path

    def pick(self, include_hidden=False, extension=''):
        while True:
            dirs = os.listdir(self.root)
            pick = random.choice(dirs)
            path = os.path.join(root, pick)
            if os.path.isfile(path) and pick.endswith(extension):
                if include_hidden==True or not pick.startswith('.'):
                    break
        return path


if __name__=="__main__":
    def signal_handler(signal, frame):
        print('Quitting')
        audio.stop()
        sys.exit(0)

    root = '/home/sumit/data/My Passport/multimedia/video/'
    audio = AUDIOPLAYER()
    video = VIDEOPLAYER()
    lottery = ROULETTE(root)


    while True:
        path = lottery.pick()

        try:
            print '[>] {}'.format(path)
            audio.play(path)
            video.play(path)
        except:
            print '[*] {}'.format(path)
        audio.stop()
        time.sleep(10)
