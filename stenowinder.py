import unittest
import sys

sidewinderStenChart = {"a": "S-",
	     "q": "S-",
	     "w": "T-",
	     "s": "K-",
	     "e": "P-",
	     "d": "W-",
	     "r": "H-",
	     "f": "R-",
	     "c": "A-",
	     "v": "O-",
	     "t": "*",
	     "g": "*",
	     "y": "*",
	     "h": "*",
	     "n": "-E",
	     "m": "-U",
	     "u": "-F",
	     "j": "-R",
	     "i": "-P",
	     "k": "-B",
	     "o": "-L",
	     "l": "-G",
	     "p": "-T",
	     ";": "-S",
	     "[": "-D",
	     "'": "-Z",
	     "1": "#",
	     "2": "#",
	     "3": "#",
	     "4": "#",
	     "5": "#",
	     "6": "#",
	     "7": "#",
	     "8": "#",
	     "9": "#",
	     "0": "#",
	     "-": "#",
	     "=": "#",}


stenOrder = {"S-": 0,
	     "T-": 1,
	     "K-": 2,
	     "P-": 3,
	     "W-": 4,
	     "H-": 5,
	     "R-": 6,
	     "A-": 7,
	     "O-": 8,
	     "*": 9,
	     "*": 10,
	     "*": 11,
	     "*": 12,
	     "-E": 13,
	     "-U": 14,
	     "-F": 15,
	     "-R": 16,
	     "-P": 17,
	     "-B": 18,
	     "-L": 19,
	     "-G": 20,
	     "-T": 21,
	     "-S": 22,
	     "-D": 23,
	     "-Z": 24}
 

stenNumbers = { 'S-':'1-', 
		'T-': '2-',
		'P-': '3-',
		'H-': '4-',
		'A-': '5-',
		'O-': '0-',
		'-F': '-6',
		'-P': '-7',
		'-L': '-8',
		'-T': '-9'}


class EclipseDictionaryFormat:
	def formatAsRTFCRE(self, stenoKeys):
		self.stenoKeys = stenoKeys
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
		return ''.join(out) 

class DCATDictionaryFormat:
	def formatAsRTFCRE(self, stenoKeys):
		self.stenoKeys = stenoKeys
		out = []
		hyphenFound = False
		for i in range(len(self.stenoKeys)):
			k = self.stenoKeys[i]
			#print("key",k)

			if len(out) == 0 and k == '*':
				out.append(k)
			
			elif k =="*" and out[-1] == "-": 
				out.pop()
				out.append(k)
				out.append("-")
			
			if k == "A-":
				k = k[:-1]
				out.append(k)
				out.append("-")
				hyphenFound = True

			elif len(out) >0 and k =="O-" and out[-1] == "-": 
				out.pop()
				k = k[:-1]
				out.append(k)
				out.append("-")
				hyphenFound = True
			
			elif k == "O-":
				if hyphenFound == True:
					k = k[:-1]
					out.append(k)
				elif hyphenFound == False:
					k = k[:-1]
					out.append(k)
					out.append("-")
					hyphenFound = True

			elif k == "-E":
				if hyphenFound == True:
					k = k[1:] 
					out.append(k)
				elif hyphenFound == False: 
					k = k[1:]
					out.append("-")
					hyphenFound = True
					out.append(k)

			elif k == "-U":
				if hyphenFound == True:
					k = k[1:] 
					out.append(k)
				elif hyphenFound == False: 
					k = k[1:]
					out.append("-")
					hyphenFound = True
					out.append(k) 

			elif k.startswith("-"):
				if hyphenFound == True:
					k = k[1:] 
					out.append(k)
				elif hyphenFound == False:
					k = k[1:] 
					out.append("-")
					hyphenFound = True 
					out.append(k)
			
			elif k.endswith("-"):
				k = k[:-1]
				out.append(k)

			elif k == "*" and len(out) > 0 and out[-1] != '-':
				out.append(k)

		if len(out) > 0 and out[-1] == "-":
			out.pop()
				
		return ''.join(out) 


class Stroke :
	def __init__(self, sidewinder, dictType) : 
		if dictType == 'dCAT':
			dictionaryFormat = DCATDictionaryFormat()
		elif dictType == 'Eclipse':
			dictionaryFormat = EclipseDictionaryFormat()

		# Retain the original sidewinder version of the stroke.
		self.sidewinder = sidewinder 

		# Convert the sidewinder to a list of steno keys.
		self.stenoKeys = []
		for s in sidewinder: 
			self.stenoKeys.append(sidewinderStenChart[s])
		if '#' in self.stenoKeys:
			for i, e in enumerate(self.stenoKeys):
				self.stenoKeys[i] = stenNumbers.get(e,e)
			while '#' in self.stenoKeys:
				self.stenoKeys.remove('#')

		# Following brilliant line of code thanks to Stavros from #python.
		self.stenoKeys = sorted(self.stenoKeys, key=lambda x: stenOrder[x])	

		out = dictionaryFormat.formatAsRTFCRE(self.stenoKeys)
		out = out.replace('****','*').replace('***','*').replace('**','*')
		out = out.replace('SS','S')
		if '-' in out:
			noHyphen = out.replace('-','')
			if noHyphen.isdigit(): 
				out = noHyphen

		self.rtfcre = out
		self.rtfcre = ''.join(out) 
		#print("self.rtfcre:",self.rtfcre)

	def isCorrection(self):
		return(self.rtfcre == '*')

	def __str__(self):
		return(' '.join(['%02X' % b for b in self.sidewinder]))		

	def __eq__(self, other):
		return(isinstance(other, Stroke) and self.sidewinder==other.sidewinder) 
	
	def __repr__(self):
		return("Stroke(%s)" % str(self))
	

class Translation :

	def __init__(self, strokes, exportDic):
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

	def __init__(self, maxLength, exportDic):
		self.maxLength = maxLength
		self.strokes = []
		self.translations = []
		self.exportDic = exportDic
		
	def consume(self, stroke):
		if stroke.isCorrection() and len(self.strokes) > 0:
			self.strokes.pop()
		# If buffer is full, discard all strokes of oldest
		# translation to make room and save the translation to
		# file.
		if len(self.strokes) >= self.maxLength:
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
					self.emit(self)
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
			translation = Translation(strokeList[:i], self.exportDic)
			if translation.english != None:
				return(translation)
		return Translation(strokeList[0:1], self.exportDic) 
			
	def emit(self, translation):
		pass

	def correct(self):
		pass

class Translator:
	def __init__(self, maxLength, exportDic, dictType):
		self.buffer = TranslationBuffer(maxLength, exportDic)
		self.dictType = dictType
	
	def translate(self, releasedKeys):
		self.buffer.consume(Stroke(''.join(releasedKeys), self.dictType))
	
	def fullTranslation(self):
		return ' '.join([str(t) for t in self.buffer.translations])

	def hasTranslations(self):
		return len(self.buffer.translations) > 0

	def mostRecentTranslation(self):
		return self.buffer.translations[-1]

