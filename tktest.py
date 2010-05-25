from tkinter import *
import sidewinder
from translation import Translator
import re

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
		self.translator = Translator(30, exportDic, dictType, sidewinder.Stroke)
		self.translator.subscribe(self.emitted)
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
			self.downKeys = [] 
			self.releasedKeys = []

	def emitted(self, translation) :
			if translation.isCorrection :
                                tell = self.translationFile.tell()
                                if translation.english :
                                        i = tell - (len(translation.english) + 1)
                                else :
                                        i = tell - (len(translation.rtfcre) + 1)
				# XXX Possibly the seek problem is here? Raise exception?
                                self.translationFile.seek(i, 0)
                                self.translationFile.truncate()
			else :
				if translation.english :
					out = translation.english
				else :
					out = translation.rtfcre
				self.translationFile.write(out + ' ')
			self.translationFile.flush()
