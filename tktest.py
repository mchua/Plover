from tkinter import *
from stenowinder import Translator

class KeyEater( Frame ):
	'''For antighosting qwerty keyboard such as Sidewinder X4'''
	def __init__( self, exportDic, dictType ):
		Frame.__init__( self )
		self.pack( expand = YES, fill = BOTH )
		self.master.title( "Plover, The Open Source Steno Program" )
		self.master.geometry( "950x50" )

		self.message1 = StringVar()
		self.line1 = Label( self, textvariable = self.message1 )
		self.message1.set( "Plover for SideWinder X4 -- http://plover.stenoknight.com" )
		self.line1.pack()

		self.message2 = StringVar()
		self.line2 = Label( self, textvariable = self.message2 )
		self.message2.set( "Dictionary Format: %s" % dictType )
		self.line2.pack()

		self.master.bind( "<KeyPress>", self.keyPressed )
		self.master.bind( "<KeyRelease>", self.keyReleased )
	
		# Initialization for steno-specific actions 
		self.translator = Translator(30, exportDic, dictType)
		self.downKeys = [] 
		self.releasedKeys = []
		
		self.translationFile = open("log.txt", "w")

		self.dictType = dictType
			
	def keyPressed( self, event ):
		self.downKeys.append(event.char)
		self.downKeys.sort()

	def keyReleased( self, event ):
		self.releasedKeys.append(event.char)
		self.releasedKeys.sort()
		if self.downKeys == self.releasedKeys:
			try: 
				self.translator.translate(self.releasedKeys)
			except KeyError:
				self.releasedKeys = []
				self.downKeys = []
			self.message2.set(self.translator.fullTranslation())	 
			if self.translator.hasTranslations():
				newTranslation = self.translator.mostRecentTranslation()
				if newTranslation.english: 
					self.translationFile.write(' ' + self.translator.mostRecentTranslation().english)
			self.translationFile.flush()
			self.downKeys = [] 
			self.releasedKeys = []
