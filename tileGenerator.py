from PIL import Image
from collections import deque
import random
import numpy as np

#Layers
LAYER_UP = 18
LAYER_CURRENT = 9
LAYER_DOWN = 0

#Directions
ROW_UP = 0
ROW_CURRENT = 3
ROW_DOWN = 6

#Position
LEFT = 1
CURRENT = 2
RIGHT = 3

#Self
SELF = 14

class Color:
	#possibly add checks to see if createTransitionTable is the last method called
	#before start
	def __init__(self, name, color):
		self.name = name
		self.RGBA = color
		self.transitions = dict()	
		self.transitionTable = dict()	

	def debug(self):
		print("Name: " + self.name)
		print("RGBA: " + str(self.RGBA))
		print("Table: " + str(self.transitions))

	def addTransition(self, chance, color, direction):
		self.transitions[(color, direction)] = chance

	def removeTransition(self, color, direction):
		self.transitions[(color, direction)] = None

	def normalize(self):
		total = 0;
		keys = self.transitions.keys()
		for trans in keys:
			total += self.transitions[trans]
		if len(keys) == 0:
			self.addTransition(1, None, 14)
		else:
			for trans in keys:
				self.transitions[trans] = self.transitions[trans]/total

	def createTransitionTable(self):
		sumation = 0
		for transition in self.transitions.keys():
			#value will be the key to this since we will iterate over it and it doesnt need to be easy for the user to manipulate it since the user won't touch it
			if transition[0]:
				print(str(transition[0].name) + " " + str(transition[1]) + " " + str(self.transitions[transition]))
			else:
				print(str(transition[0]) + " " + str(transition[1]) + " " + str(self.transitions[transition]))
			self.transitionTable[sumation] = transition
			sumation += self.transitions[transition]

	def generate(self, value):
		table = self.transitionTable
		keys = sorted(table.keys())
		notFound = True
		i = 0
		tbr = None

		while(notFound and i < len(keys)):
			if value >= keys[i]:
				tbr = table[keys[i]]
			else:
				notFound = False
			i += 1
		print("TBR: " + str(tbr))
		return tbr

		

class ColorTracker:
	def __init__(self):
		self.Colors = dict()

	#color should be a tuple in the form RGBA
	def addColor(self, color):
		self.Colors[color.name] = color

	def debug(self):
		for color in self.Colors.keys():
			print(self.Colors[color].debug())

	def normalizeAll(self):
		for color in self.Colors.keys():
			self.Colors[color].normalize()

	def createTransitionTable(self):
		for color in self.Colors.keys():
			self.Colors[color].createTransitionTable()

class Tile:
	def __init__(self, sizeX, sizeY, sizeZ):
		self.tile = [[[None for x in range(sizeX)] for y in range(sizeY)] for z in range(sizeZ)]
		self.queue = deque()

	def saveTile(self, name):
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

	def start(self, optionalColor, tracker):

		if not self.queue:
			self.presetPixel(optionalColor, 0, 0, 0)
			#random color? 
		while(self.queue):
			CurrentPosition = self.queue.popleft()
			x,y,z = CurrentPosition
			self.tile[z][y][x].generate(random.random())
			#self.generateColors()

	'''
	Used to generate the entire image. Will also normalize all fields.
	'''
	def generateImage(self, tracker):
		tracker.normalizeAll()
		tracker.createTransitionTable()
		self.start('RED', tracker)



def test():
	red = Color("RED ", (255,0,0,255))
	blue = Color("BLUE", (0,255,0,255))
	green = Color("GREEN", (0,0,255,255))
	red.addTransition(.2, green, (LEFT+ROW_CURRENT)+LAYER_CURRENT)
	red.addTransition(.2, blue, (RIGHT+ROW_CURRENT)+LAYER_CURRENT)
	red.addTransition(.2, red, (CURRENT+ROW_UP)+LAYER_CURRENT)
	red.addTransition(.2, green, (CURRENT+ROW_DOWN)+LAYER_CURRENT)
	blue.addTransition(.25, green, (LEFT+ROW_CURRENT)+LAYER_CURRENT)
	blue.addTransition(.25, blue, (RIGHT+ROW_CURRENT)+LAYER_CURRENT)
	blue.addTransition(.25, red, (CURRENT+ROW_UP)+LAYER_CURRENT)
	blue.addTransition(.25, green, (CURRENT+ROW_DOWN)+LAYER_CURRENT)
	green.addTransition(1, green, (LEFT+ROW_CURRENT)+LAYER_CURRENT)
	green.addTransition(1, blue, (RIGHT+ROW_CURRENT)+LAYER_CURRENT)
	green.addTransition(1, red, (CURRENT+ROW_UP)+LAYER_CURRENT)
	green.addTransition(1, green, (CURRENT+ROW_DOWN)+LAYER_CURRENT)
	tracker = ColorTracker()
	tracker.addColor(red)
	tracker.addColor(blue)
	tracker.addColor(green)
	#tracker.debug()
	tile = Tile(100, 100, 1)
	tile.presetPixel(red, 0, 0, 0)
	tile.presetPixel(green, 0, 99, 0)
	tile.presetPixel(blue, 0, 99, 99)
	tile.generateImage(tracker)
	#print(red.transitionTable)
test()
