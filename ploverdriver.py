import serial
from ploverbd import exportDic 

stenChart = ("Fn","#1","#2","#3","#4","#5","#6",
	     "S-","S-","T-","K-","P-","W-","H-",
	     "R-","A-","O-","*","*","res","res",
	     "pwr","*","*","-E","-U","-F","-R",
	     "-P","-B","-L","-G","-T","-S","-D",
	     "#7","#8","#9","#10","#11","#12","-Z")

tinyDic = {'H- R- O- -G': 'log', 
	   'K- A- -T': 'cat' ,
	   'K- A- -T / H- R- O- -G': 'catalog',
	   'H- R- O- -G / K- A- -T': 'Log Cat'}

MAX_WORD_STROKES = 10

strokeBuffer = []

def stenStrokeToRTFCRE(stroke):
	"""
	Takes a list of stenKeys and outputs a string in rtf/cre
	compatible format.
	"""
	out = []
	hyphenFound = False
	for i in range(len(stroke)):
		k = stroke[i]
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
	return(''.join(out))


def isStenKey(x):
	"""
	Returns True if this is a valid Gemini steno stroke; False
	otherwise.
	"""
 	#Checks length of stroke and checks if MSB of first byte is set.
	#Later - make it check the rest of the bytes.
	return((len(x) == 6) and (x[0] & 0x80))

def stenKeyToString(x):
	"""
	Converts input from steno machine into human-readable format.
	"""
	#strokeList = []
	#for b in x:
	#	strokeList.append('%02X' % b) 
	#return(' '.join(strokeList))
	return(' '.join(['%02X' % b for b in x]))	
 
def stenKeyToRawSteno(x):
	"""
	Converts binary from steno machine into standard stenographic
	code, and returns a list of elements in stenChart.
	"""
	out = []
	for i in range(len(x)):
		b = x[i]
		#print("b equals " + str(b)k)
		for j in range(8):
			#print("j equals " + str(j))
			if b & (b & (0x80 >> j)):
				out.append(stenChart[i*7 + j-1])
	return(out[1:])

def rawStenoCleanup(x):
	#print("Raw steno: " + str(stenKeyToRawSteno(x)))
	prettySteno = stenKeyToRawSteno(x) 
	prettySteno = ' '.join(prettySteno)
	return(prettySteno)

def emit(x):
	print(x)

def translateIndex(b):
	# Returns index of longest possible 
	# sequence of consecutive strokes, starting 
	#from the first stroke. If no translation
	#is found, return 0.
	for i in range(len(b),0,-1):
		strokeSequence = '/'.join(b[0:i])
		if strokeSequence in exportDic:
			return(i,strokeSequence)
	return(-1,None)

def translateCheck(x): 
	"""
	Tries to define the longest series of strokes up to
	maximum set by MAX_WORD_STROKES; if unsuccessful,
	chops up series of strokes into largest definable pieces.
	"""
	global strokeBuffer
	# The buffer is full, so make room for the new stroke by
	# emitting either translation or the raw steno, if there
	# is no translation.
	if len(strokeBuffer) >= MAX_WORD_STROKES:
		i,strokeSequence = translateIndex(strokeBuffer)
		if strokeSequence is None:
			emit(strokeBuffer[0])
			strokeBuffer = strokeBuffer[1:]
		else:
			strokeBuffer = strokeBuffer[i:]
			emit(exportDic[strokeSequence])
	
	# Add the new stroke to the buffer in rtfcre format
 	stroke = stenKeyToRawSteno(x)
	rtfcre = stenStrokeToRTFCRE(stroke) 
	strokeBuffer.append(rtfcre)
	for i in range(len(strokeBuffer),0,-1):
			if strokeSequence in exportDic:
				emit(exportDic[strokeSequence])
				strokeBuffer = strokeBuffer[i:]
				break

	# Keep track of length of translated strokes	


def main():
	ser = serial.Serial(7)  # open first serial port
	print(ser.portstr)       # check which port was really used
	while True:
		x = ser.read(6)          # read six bytes
		if isStenKey(x): 
			print(type(x))
			translateCheck(x)
		else:
			print("Not a complete stroke.")

if __name__ == "__main__" :
	main()
