from PIL import Image
from collections import deque
import random
import numpy as np

class Color:
	# used for layers and rows.
	ABOVE = 2
	CURRENT = MIDDLE = 1
	BELOW = 0


	def __init__(self, name, color):
		self.name = name
		self.RGBA = color
		#index 0 = table for layer below
		#index 1 = table for current layer
		#index 2 = table above
		self.transitionTable = [[[0 for x in range(3)] for y in range(3)] for z in range(3)]
		

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
				total += sum(row)
		if total != 1:
			if total != 0:
				for layer in self.transitionTable:
					for row in layer:
						for ele in row:
							ele = ele/total
			else:
				self.transitionTable[1][1][1] = 1

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
		self.transitionTable = [[[0 for x in range(3)] for y in range(3)] for z in range(3)]


class ColorTracker:
	def __init__(self):
		self.Colors = dict()

	#color should be a tuple in the form RGBA
	def addColor(self, color):
		self.Colors[color.name] = color.RGBA

	def debug(self):
		for key in self.Colors.keys():
			print("Color: " + key)
			print("RGBA: " + str(self.Colors[key]))

class Tile:
	def __init__(self, sizeX, sizeY):
		self.tile = [[None for x in range(sizeX)] for y in range(sizeY)]
		self.queue = []

	def saveTile(self):
		im = Image.fromarray(self.tile)
		im.mode = 'RGBA'
		im.show()
		im.save(name + '.png')

	def presetPixel(self, color, layer, xPos, yPos):
		tile[layer][yPos][xPos] = color
		queue.append((xPos,yPos))

	#might need to fix order of xPos and yPos
	def validPoint(self, layer, xPos, yPos):
		if len(self.tile) > layer:
			if len(self.tile[0]) > yPos:
				if len(self.tile[0][0]) > xPos:
					if xPos > 0 or yPos > 0:
						if self.tile[yPos][xPos] == None:
							return True
		return False

	def start(self, optionalColor):
		if not self.queue:
			self.presetPixel(optionalColor, 0, 0, 0)
			#random color? 
		while(self.queue):
			CurrentPosition = self.Queue.popleft()
			generateColors()

def test():
	red = Color("RED", (255,0,0,255))
	blue = Color("BLUE", (0,255,0,255))
	green = Color("GREEN", (0,0,255,255))
	red.normalizeTable()
	tracker = ColorTracker()
	tracker.addColor(red)
	tracker.addColor(blue)
	tracker.addColor(green)
	tracker.debug()

test()
