class Translation :

	def __init__(self, strokes, rtfcreDict):
		'''strokes is a list of Stroke objects.'''
		self.strokes = strokes
		self.rtfcre = "/".join([s.rtfcre for s in self.strokes])
		self.english = rtfcreDict.get(self.rtfcre, None)
		self.isCorrection = False

	def __eq__(self, other):
		return(self.rtfcre == other.rtfcre)

	def __str__(self):
		if self.english:
			return(self.english)
		else:
			return(self.rtfcre)

	def __repr__(self):
		return(str(self))

class TranslationBuffer :

	def __init__(self, maxLength, rtfcreDict):
		self.maxLength = maxLength
		self.strokes = []
		self.translations = []
		self.rtfcreDict = rtfcreDict
		self.callbacks = []
		
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
		
		# Compare old translations to the new translations and
		# reconcile them by emitting one or more tokens,
		# where a token is either a correction or a
		# translation.
		for i in range(min(len(self.translations), len(newTranslations))):
			if self.translations[i] != newTranslations[i]:
				# Emit corrections for each remaining
				# element in self.translations after
				# the two lists differ.
				for t in self.translations[i:] :
					t.isCorrection = True
					self.emit(t)
				for t in newTranslations[i:] :
					self.emit(t)
				self.translations = newTranslations
				return

		# The translation and new translations don't differ
		# except for one is the same as the other with
		# additional translations appended.  As such,
		# translations must be removed or added, depending on
		# which list is longer.
		if len(self.translations) > len(newTranslations) :
			for t in self.translations[len(newTranslations):] :
				t.isCorrection = True
				self.emit(t)
		else :
			for t in newTranslations[len(self.translations):] :
				self.emit(t)

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
			translation = Translation(strokeList[:i], self.rtfcreDict)
			if translation.english != None:
				return(translation)
		return Translation(strokeList[0:1], self.rtfcreDict) 
			
	def emit(self, translation):
		for callback in self.callbacks :
			callback(translation)

	def correct(self):
		pass

	def subscribe(self, callback) :
		self.callbacks.append(callback)


class Translator:
	def __init__(self, maxLength, rtfcreDict, dictType, strokeClass):
		self.buffer = TranslationBuffer(maxLength, rtfcreDict)
		self.dictType = dictType
		self.strokeClass = strokeClass
	
	def translate(self, machineOutput):
		if not machineOutput is str :
			if len(machineOutput) and isinstance(machineOutput[0], str):
				machineOutput = ''.join(machineOutput)
			else: 
				machineOutput = ''.join([chr(x) for x in machineOutput])
		self.buffer.consume(self.strokeClass(machineOutput, self.dictType))
	
	def fullTranslation(self):
		return ' '.join([str(t) for t in self.buffer.translations])

	def hasTranslations(self):
		return len(self.buffer.translations) > 0

	def mostRecentTranslation(self):
		return self.buffer.translations[-1]

	def subscribe(self, callback) :
		self.buffer.subscribe(callback)
