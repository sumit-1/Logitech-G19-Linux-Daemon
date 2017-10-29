from logitech.g19 import G19
import time
import os
import random
import cv2
import ctypes
import subprocess
import signal
import sys
import thread

class AUDIOPLAYER:
    def __init__(self):
        pass

    def play(self, path):
        self.audio = subprocess.Popen(['mplayer', '-msglevel','all=-1', '-novideo', '-slave', path], stderr=subprocess.PIPE)

    def stop(self):
        self.audio.send_signal(2)


class COLOR:
    def __init__(self, lg19):
        self.lg19 = lg19

    def userInput(self):
        inp = raw_input()
        val = inp.split(' ')
        if len(val) != 3:
            print 'Syntax Error. Combination is "255 0 0"'
            return False
        for i in val:
            try:
                j = int(i)
            except:
                print 'Needs integer {}'.format(i)
                return False
            if j<0 or j>255:
                print 'Wrong color code {}'.format(j)
                return False
        self.value = val
        return True

    def setColor(self):
        self.lg19.set_bg_color(int(self.value[0]), int(self.value[1]), int(self.value[2]))

    def play(self):
        print 'Enter rgb color in "255 128 128" format'
        while True:
            if self.userInput():
                self.setColor()
                print '[+] Settings applied'
            else:
                print '[-] Changes not applied'

class VIDEOPLAYER:
    def __init__(self, lg19):
        self.libc = ctypes.CDLL('libc.so.6')
        self.lg19 = lg19


    def play(self, path):
        videoFile = cv2.VideoCapture(path)
        nFrames = int(videoFile.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        fps = videoFile.get(cv2.cv.CV_CAP_PROP_FPS)
        frame_gap = 1/fps
        uexpected_time = int(frame_gap * 1000000)
        usleep = uexpected_time

        for i in xrange(nFrames):
            t1 = time.time()
            self.libc.usleep(usleep)
            try:
                ret, frame = videoFile.read()
                frame = cv2.resize(frame, (320, 240))
                frame = cv2.transpose(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR565)
                data = frame.flatten('C').tolist()
            except:
                return
            self.lg19.send_frame(data)
            t2 = time.time()
            time_taken = t2-t1
            utime_taken = int(time_taken*1000000)
            uextra_time = utime_taken - uexpected_time
            usleep = int(usleep - uextra_time)
            if usleep < 1:
                usleep = 1


class WALLPAPER:
    def __init__(self, lg19):
        self.lg19 = lg19

    def load(self, path):
        self.lg19.load_image(path)

class ROULETTE:
    def __init__(self, path=''):
        self.root = path

    def pick(self, include_hidden=False, extension=''):
        while True:
            dirs = os.listdir(self.root)
            pick = random.choice(dirs)
            path = os.path.join(self.root, pick)
            if os.path.isfile(path) and pick.endswith(extension):
                if include_hidden==True or not pick.startswith('.'):
                    break
        return path


if __name__=="__main__":
    def signal_handler(signal, frame):
        print('Quitting')
        audio.stop()
        sys.exit(0)

    video_dir = '../multimedia/video/'
    image_dir = 'wallpaper'
    lg19 = G19()
    audio = AUDIOPLAYER()
    video = VIDEOPLAYER(lg19)
    color = COLOR(lg19)
    wallpaper = WALLPAPER(lg19)

    thread.start_new_thread(color.play, ())
    pick_video = ROULETTE(video_dir)
    pick_image = ROULETTE(image_dir)


    while True:
        for i in range(5):
            path = pick_image.pick()
            try: wallpaper.load(path)
            except: print path
            time.sleep(5)

        path = pick_video.pick()

        try:
            print '[>] {}'.format(path)
            audio.play(path)
            video.play(path)
        except:
            print '[*] {}'.format(path)
        audio.stop()
