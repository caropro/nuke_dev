#coding=utf-8
import sys
import nuke
import time
import nukescripts
import threading
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

class adult(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.__data()

	def __data(self):
		# nuke.message("File better be jpg file")
		path = nuke.getFilename("File better be jpg file")
		limit = nuke.getInput("set the width to scale")
		if not int(limit):
			nuke.message("Wrong Type")
		self.adult_dict = {}
		img = QImage(path)
		img = img.scaledToWidth(int(limit))
		width, height = img.width(), img.height()
		scale = 255
		id = 0
		for y in range(0, height):
			for x in range(0, width):
				id += 1
				c = img.pixel(x, y)
				r, g, b, a = QColor(c).getRgbF()
				r, g, b, a = r * scale, g * scale, b * scale, a * scale
				color = int('%02x%02x%02x%02x' % (r, g, b, a), 16)
				xa = x * 10
				ya = y * 10
				self.adult_dict[id] = {"pos": (xa, ya), "color": color}
			id = id + 1
			self.adult_dict[id] = None
		print(self.adult_dict)

	def run(self):
		node = None
		incs = 1
		for i in range(incs):
			for n, m in self.adult_dict.items():
				if not m:
					nukescripts.clear_selection_recursive()
					continue
				node = nuke.createNode("Dot")
				x = m["pos"][0]
				y = m["pos"][1]
				color = m["color"]
				nuke.executeInMainThreadWithResult(node.setXpos, int(x))
				nuke.executeInMainThreadWithResult(node.setYpos, int(y))
				nuke.executeInMainThreadWithResult(node["tile_color"].setValue, (int(color)))

def run():
	adult().start()

