stenChart = ("Fn","#","#","#","#","#","#",
	     "S-","S-","T-","K-","P-","W-","H-",
             "R-","A-","O-","*","*","res","res",
             "pwr","*","*","-E","-U","-F","-R",
             "-P","-B","-L","-G","-T","-S","-D",
             "#","#","#","#","#","#","-Z")

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

class Stroke :

	def __init__(self, binary, stenoDictType) :

		# XXX : ignore stenoDictType for now.

		# XXX : work around for python 3.1 and python 2.6 differences
		if isinstance(binary, str) :
			binary = [ord(x) for x in binary]

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
		
		# Converts strokes involving number bar to numbers.  
		if '#' in self.stenoKeys:
			for i, e in enumerate(self.stenoKeys):
				self.stenoKeys[i] = stenNumbers.get(e,e)
			while '#' in self.stenoKeys:
				self.stenoKeys.remove('#')


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
		if '-' in out:
			noHyphen = out.replace('-','')
			if noHyphen.isdigit(): 
				out = noHyphen

		self.rtfcre = out
	
	def isCorrection(self):
		return(self.rtfcre == '*')

	def __str__(self):
		return(' '.join(['%02X' % b for b in self.binary]))		

	def __eq__(self, other):
		return(isinstance(other, Stroke) and self.binary==other.binary) 
	
	def __repr__(self):
		return("Stroke(%s)" % str(self))
	
