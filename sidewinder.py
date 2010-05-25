from dictionaries import *

qwertyToSteno = {"a": "S-",
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
 
class Stroke :
	def __init__(self, keyList, dictType) : 
		if dictType == 'dCAT':
			dictionaryFormat = DCATDictionaryFormat()
		elif dictType == 'Eclipse':
			dictionaryFormat = EclipseDictionaryFormat()

		# Retain the original keyList version of the stroke.
		self.keyList = keyList 

		# Convert the keyList to a list of steno keys.
		self.stenoKeys = []
		for s in keyList: 
			self.stenoKeys.append(qwertyToSteno[s])
		if '#' in self.stenoKeys:
                    # XXX : not yet implemented
                    pass
                
		# Following brilliant line of code thanks to Stavros from #python.
                # XXX : Use in-place sort instead.
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

	def isCorrection(self):
		return(self.rtfcre == '*')

	def __str__(self):
		return(' '.join(['%02X' % b for b in self.keyList]))		

	def __eq__(self, other):
		return(isinstance(other, Stroke) and self.keyList==other.keyList) 
	
	def __repr__(self):
		return("Stroke(%s)" % str(self))
