from logitech.g19 import G19
import os
import random
import time
import thread

class WALLPAPER:
	def __init__(self, lg19):
		self.imgPath = 'wallpaper'
		self.timeout = 60
		self.lg19 = lg19

	def reloadImages(self):
		self.files = os.listdir(self.imgPath)
		random.shuffle(self.files,random.random)

	def changeImages(self):
		for image in self.files:
			self.lg19.load_image(os.path.join(self.imgPath, image))
			time.sleep(self.timeout)

	def play(self):
		while True:
			self.reloadImages()
			self.changeImages()

class COLOR:
	def __init__(self, lg19):
		self.lg19 = lg19

	def userInput(self):
		inp = raw_input()
		val = inp.split(' ')
		if len(val) != 3:
			print 'Syntax Error. Combination is "255 255 255"'
			return False
		for i in val:
			try:
				j = int(i)
			except:
				print 'Needs integer %s' % (i)
				return False
			if j<0  or j>255:
				print 'Wrong value for color %d' % (j)
				return False
		self.value = val
		return True

	def setColor(self):
		self.lg19.set_bg_color(int(self.value[0]), int(self.value[1]), int(self.value[2]))

	def play(self):
		print 'Enter color in "255 0 0" format'
		while True:
			if self.userInput():
				self.setColor()
				print '[+] Settings applied'
			else:
				print '[-] Changes not applied'

if __name__=="__main__":
	lg19 = G19()
	wp = WALLPAPER(lg19)
	thread.start_new_thread(wp.play, ())
	cl = COLOR(lg19)
	cl.play()
