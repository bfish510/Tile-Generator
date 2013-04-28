from PIL import Image
from collections import deque
import random
import numpy as np

ABOVE = 2
CURRENT = MIDDLE = 1
BELOW = 0

class Color:
	# used for layers and rows.
	


	def __init__(self, name, color):
		self.name = name
		self.RGBA = color
		"""
			might make this four dimensional to reduce from 2 rand calls in my pervious version to 1.
			This should speed things up considerably with the new transition algorithm.
			Also, might make middle index 
		"""
		self.transitionTable = [[[[0, None] for x in range(3)] for y in range(3)] for z in range(3)]

		

	def debug(self):
		print("Name: " + self.name)
		print("RGBA: " + str(self.RGBA))
		print("Table: " + str(self.transitionTable))

	"""
		A zero magnitude table will result in the middle index being 1
	 	and will cause generation to end with this item. 
	 """ 
	def normalizeTable(self):
		total = 0
		for layer in self.transitionTable:
			for row in layer:
				for color in row:
					for ele in color:
						if ele:
							total += ele[0]
						else:
							total += 0
		if total != 1:
			if total != 0:
				for layer in self.transitionTable:
					for row in layer:
						for colors in row:
							for ele in colors:
								ele = ele/total
			else:
				self.transitionTable[1][1][1][0] = [1, None]

	def updateTransitionLayer(self, layer, newTable):
		self.transitionTable[layer] = newTable

	def updateTransitionRow(self, layer, row, newRow):
		self.transitionTable[layer][row] = newRow

	def updateTransitionIndex(self, layer, row, index, value):
		self.transitionTable[layer][row][index] = value

	def clearAndUpdateTransitionIndex(self, layer, row, index, value):
		clearTable()
		updateTransitionIndex(self, layer, row, index, value)

	def clearAndUpdateTransitionLayer(self, layer, newTable):
		clearTable()
		updateTransitionLayer(self, layer, newTable)

	def clearAndUpdateTransitionRow(self, layer, row, newRow):
		clearTable()
		updateTransitionRow(self, layer, row, newRow)

	def clearTable(self):
		self.transitionTable = [[[[0, None] for x in range(3)] for y in range(3)] for z in range(3)]


class ColorTracker:
	def __init__(self):
		self.Colors = dict()

	#color should be a tuple in the form RGBA
	def addColor(self, color):
		self.Colors[color.name] = color

	def debug(self):
		for key in self.Colors.keys():
			print("Color: " + key)
			print("RGBA: " + str(self.Colors[key].RGBA))
			print("Transition Table" + str(self.Colors[key].transitionTable))

class Tile:
	def __init__(self, sizeX, sizeY, sizeZ):
		self.tile = [[[None for x in range(sizeX)] for y in range(sizeY)] for z in range(sizeZ)]
		self.queue = deque()

	def saveTile(self):
		im = Image.fromarray(self.tile)
		im.mode = 'RGBA'
		im.show()
		im.save(name + '.png')

	def presetPixel(self, color, layer, xPos, yPos):
		self.tile[layer][yPos][xPos] = color
		self.queue.append((xPos,yPos,layer))

	
	def validPoint(self, layer, xPos, yPos):
		if len(self.tile) > layer:
			if len(self.tile[0]) > yPos:
				if len(self.tile[0][0]) > xPos:
					if xPos > 0 or yPos > 0:
						if self.tile[layer][yPos][xPos] == None:
							return True
		return False

	def start(self, optionalColor):
		if not self.queue:
			self.presetPixel(optionalColor, 0, 0, 0)
			#random color? 
		while(self.queue):
			CurrentPosition = self.queue.popleft()
			self.generateColors()

	'''
	Used to generate a single layer in an image. Shouldn't really be used directly but that's up to you!!!!!
	This might not need to exist because we will be transitioning between layers
	'''
	def generateLayer(self):
		return False

	'''
	Used to generate the entire image. Will also normalize all fields.
	'''
	def generateImage(self, tracker):
		for color in tracker.Colors.keys():
			print(color + '\t' + str(tracker.Colors[color].transitionTable))
			tracker.Colors[color].normalizeTable()
		self.start('RED')



def test():
	red = Color("RED ", (255,0,0,255))
	blue = Color("BLUE", (0,255,0,255))
	green = Color("GREEN", (0,0,255,255))
	red.normalizeTable()
	tracker = ColorTracker()
	tracker.addColor(red)
	tracker.addColor(blue)
	tracker.addColor(green)
	#tracker.debug()
	tile = Tile(10, 10, 1)
	tile.generateImage(tracker)
	#print(red.transitionTable)
test()
