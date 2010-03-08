from ploverbd import exportDic 
import unittest

stenChart = ("Fn","#","#","#","#","#","#",
	     "S-","S-","T-","K-","P-","W-","H-",
             "R-","A-","O-","*","*","res","res",
             "pwr","*","*","-E","-U","-F","-R",
             "-P","-B","-L","-G","-T","-S","-D",
             "#","#","#","#","#","#","-Z")

class Stroke :

	def __init__(self, binary) :

		#print("binary:",binary)

		# Make sure this is a valid steno stroke.
		if not ((len(binary) == 6) and 
			(binary[0] & 0x80) and
			(not (binary[1] & 0x80)) and
			(not (binary[2] & 0x80)) and
			(not (binary[3] & 0x80)) and
			(not (binary[4] & 0x80)) and
			(not (binary[5] & 0x80))): 
			raise(ValueError("Not a valid Gemini PR steno stroke."))

		# Retain the original binary version of the stroke.
		self.binary = binary 

		# Convert the binary to a list of steno keys.
		self.stenoKeys = []
		for i in range(len(self.binary)):
			b = self.binary[i]
			for j in range(8):
				if i == 0 and j == 0:
					continue # Ignore the first bit 
				if (b & (0x80 >> j)):
					self.stenoKeys.append(stenChart[i*7 + j-1]) 

		# Takes a list of stenKeys and outputs a string in rtf/cre compatible format.  
		out = []
		hyphenFound = False
		for i in range(len(self.stenoKeys)):
			k = self.stenoKeys[i]
			#print("key",k)
			if k == "A-" or k == "O-":
				k = k[:-1]
				hyphenFound = True

			elif k == "-E" or k == "-U":
				k = k[1:]
				hyphenFound = True

			elif k[0] == "*":
				hyphenFound = True
					
			elif k.endswith("-"):
				k = k[:-1]

			elif k.startswith("-"):
				if hyphenFound == True:
					k = k[1:] 
				elif hyphenFound == False:
					k = k[1:] 
					out.append("-")
					hyphenFound = True 
					
			out.append(k)
		out = ''.join(out) 
		out = out.replace('****','*').replace('***','*').replace('**','*')
		out = out.replace('SS','S')
		self.rtfcre = out
	
	def isCorrection(self):
		return(self.rtfcre == '*')

	def __str__(self):
		return(' '.join(['%02X' % b for b in self.binary]))		

	def __eq__(self, other):
		return(isinstance(other, Stroke) and self.binary==other.binary) 
	
	def __repr__(self):
		return("Stroke(%s)" % str(self))
	

class Translation :

	def __init__(self, strokes):
		'''strokes is a list of Stroke objects.'''
		self.strokes = strokes
		self.rtfcre = "/".join([s.rtfcre for s in self.strokes])
		self.english = exportDic.get(self.rtfcre, None) 

	def __str__(self):
		if self.english:
			return(self.english)
		else:
			return(self.rtfcre)

	def __repr__(self):
		return(str(self))

class TranslationBuffer :

	def __init__(self, maxLength):
		self.maxLength = maxLength
		self.strokes = []
		self.translations = []
	
	def consume(self, stroke):
		if stroke.isCorrection() and len(self.strokes) > 0:
			self.strokes.pop()
		# If buffer is full, discard all strokes of oldest
		# translation to make room.
		if len(self.strokes) >= self.maxLength:
			#print("Buffer is full. Discard oldest translation.")
			forsaken = self.translations.pop(0)	
			for s0 in forsaken.strokes:
				s1 = self.strokes.pop(0) 
				if s0 != s1:
					raise(RuntimeError("Buffers out of sync."))

		# Add new stroke and update buffers.	
		if not stroke.isCorrection():
			self.strokes.append(stroke)
		newTranslations = self.translateStrokes(self.strokes) 
		#print("self.strokes",self.strokes)
		
		# Compare old translations to the new translations and
		# reconcile them by emitting one or more tokens,
		# where a token is either a correction or a
		# translation.
		for i in range(min(len(self.translations), len(newTranslations))):
			if self.translations[i] != newTranslations[i]: 
				# Emit corrections for each remaining
				# element in self.translations after
				# the two lists differ.
				for j in range(i, len(self.translations)):
					self.correct()
				for j in range(i, len(newTranslations)):
					self.emit(newTranslations[j])
				break

		# Replace old translations with new translations.
		self.translations = newTranslations

	def translateStrokes(self, strokeList):
		'''Takes list of strokes and returns a list of
		translations that uses all the strokes.'''
		newTranslations = []
		# The loop ends as soon as we've used all the strokes.
		numStrokesUsed = 0 
		while numStrokesUsed != len(strokeList):
			newTranslations.append(self.longestTranslation(strokeList[numStrokesUsed:]))
			numStrokesUsed = sum([len(t.strokes) for t in newTranslations]) 
		return(newTranslations)

	def longestTranslation(self, strokeList):
		'''Returns longest English translation that starts from the
		beginning of the buffer, or a translation object
		containing only the first stroke if no English
		translation exists.'''
		for i in range(len(strokeList),0,-1):
			translation = Translation(strokeList[:i])
			if translation.english != None:
				return(translation)
		return(Translation(strokeList[0:1]))
			
	def emit(self, translation):
		pass

	def correct(self):
		pass

def test0():
	raw0 = [0x80,0x08,0x20,0x01,0x00,0x00]
	stroke0 = Stroke(raw0)
	stroke1 = Stroke(raw0)
	assert(stroke0 == stroke1)
	assert(stroke0.binary == stroke1.binary)
	assert(stroke0.stenoKeys == stroke1.stenoKeys)
	assert(stroke0.rtfcre == stroke1.rtfcre)
	assert(exportDic["-B"] == "be")

def test1():
	import serial
	# open first serial port
	ser = serial.Serial(7)  
	print(ser.portstr)       
	# Create translation engine.
	tBuffer = TranslationBuffer(10)
	while True:
		# read six bytes
		x = ser.read(6)          
		tBuffer.consume(Stroke(x))
		print(tBuffer.translations)
		print([t.rtfcre for t in tBuffer.translations])	

class TestTranslationFunctions(unittest.TestCase):
	def setUp(self):
		self.tBuffer = TranslationBuffer(10)
		raw = [0x80,0x08,0x20,0x01,0x00,0x00]
		self.s1 = Stroke(raw)
		self.s2 = Stroke(raw)

	def testSuffixes(self):
		self.s1.rtfcre = "PWAOEUBG"
		self.s2.rtfcre = "-G"
		self.tBuffer.consume(self.s1)
		self.tBuffer.consume(self.s2)
		self.assertEqual(["biking"], self.tBuffer.translations)

	def testAsteriskEquivalence(self):
		fourAsterisksRaw = [0x80, 0x00, 0x0C, 0x30, 0x00, 0x00]
		threeAsterisksRaw = [0x80, 0x00, 0x08, 0x30, 0x00, 0x00]
		twoAsterisksRaw = [0x80, 0x00, 0x00, 0x30, 0x00, 0x00]
		oneAsteriskRaw = [0x80, 0x00, 0x00, 0x10, 0x00, 0x00]
		fourAsterisksStroke = Stroke(fourAsterisksRaw)
		threeAsterisksStroke = Stroke(threeAsterisksRaw)
		twoAsterisksStroke = Stroke(twoAsterisksRaw)
		oneAsteriskStroke = Stroke(oneAsteriskRaw)
		self.assertEqual(oneAsteriskStroke.rtfcre,
				twoAsterisksStroke.rtfcre)
		self.assertEqual(oneAsteriskStroke.rtfcre,
				threeAsterisksStroke.rtfcre)
		self.assertEqual(oneAsteriskStroke.rtfcre,
				fourAsterisksStroke.rtfcre)

	def leftSEquivalence(self):
		# Raw steno for both S- keys pressed at once.
		# Turn pseudocode into real code.
		self.s1 = stenokeys(raw1)
		self.s2 = stenokeys(raw2)
		self.assertEqual(s1, s2)


if __name__ == "__main__":
	#test0()
	test1()
	unittest.main()
	# Add more tests



