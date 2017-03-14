import wx
from PIL import Image, ImageGrab
import os

# Globals
filename = "screenshot_"
fileNum = 1
fileExt = ".jpg"

def takeScreenShot(startX, startY, endX, endY):
	if (startX != endX and startY != endY):		
		image = ImageGrab.grab()

		savedImg = image.crop((startX, startY, endX, endY))

		for files in os.listdir(os.environ['USERPROFILE'] + "/Desktop"):
			if (os.path.isfile(os.path.join(os.environ['USERPROFILE'] + "/Desktop", files))):
				try:			
					if (files[:files.index('_')+1] == filename): # For every file it finds with the same format it adds one to fileNum
						global fileNum 
						fileNum += 1
				except:
					pass # No correct substring found; otherwise would crash	

		savedImg.save(os.environ['USERPROFILE'] + "/Desktop/" + filename+str(fileNum)+fileExt)

		print("Screenshot saved as screenshot_%d.jpg on Desktop" % fileNum)
	else:
		print("Screenshot Failed: Cannot have same x or y values for start and end.")

class Frame(wx.Frame):
	def __init__(self):
		super(Frame, self).__init__(None, style=wx.NO_BORDER)
		self.SetTitle("Screenshot Taker")	
		self.Show()			

		# Variables
		self.startX = 0
		self.startY = 0
		self.endX = 0
		self.endY = 0
		self.isClicked = False
		self.isDrawn = False

		screenSize = wx.DisplaySize()
		self.SetSizeWH(screenSize[0], screenSize[1])
		self.SetPosition((0, 0))
		self.SetTransparent(100)

		# Mouse Events
		self.Bind(wx.EVT_LEFT_DOWN, self.leftMousePressed)
		self.Bind(wx.EVT_MOTION, self.mouseMoved)
		self.Bind(wx.EVT_LEFT_UP, self.leftMouseReleased)
		# Exit Program
		self.Bind(wx.EVT_KEY_DOWN, self.escapePressed)

	def printCoords(self):
		mx, my = wx.GetMousePosition()
		print("Mouse X:\t%d\tMouse Y:\t%d" % (mx, my))

	def leftMousePressed(self, event):
		self.startX, self.startY = wx.GetMousePosition()
		self.isClicked = True

		try:
			self.dc.Clear()
		except:
			pass

	def leftMouseReleased(self, event):
		self.endX, self.endY = wx.GetMousePosition()
		self.isClicked = False

		self.dc.Clear()
		self.dc.DrawRectangle(self.startX, self.startY, self.endX-self.startX, self.endY-self.startY)	

	def mouseMoved(self, event):
		if (self.isClicked):
			self.dc = wx.WindowDC(self)
			self.dc.SetPen(wx.Pen('#D42626', 1)) # Lines
			self.dc.SetBrush(wx.Brush('#E64C4C')) # Fill
			self.dc.DrawRectangle(self.startX, self.startY, wx.GetMousePosition()[0]-self.startX, wx.GetMousePosition()[1]-self.startY)	
			self.isDrawn = True
			wx.CallLater(50, self.refreshRectangle)

	def refreshRectangle(self):
		self.dc.Clear()
		self.dc.DrawRectangle(self.startX, self.startY, wx.GetMousePosition()[0]-self.startX, wx.GetMousePosition()[1]-self.startY)	

	def escapePressed(self, event):
		if (event.GetKeyCode() == 27): # Escape
			self.Close()
		elif (event.GetKeyCode() == 13):
			self.dc.Clear()
			self.SetTransparent(0)
			takeScreenShot(self.startX, self.startY, self.endX, self.endY)
			self.SetTransparent(100)

if __name__ == "__main__":
	app = wx.App(None)
	frame = Frame()	
	app.MainLoop()