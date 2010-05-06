from stenowinder import *
import eclipseDict
import dCATDict

class TestTranslatingWithDifferentFormats(unittest.TestCase):
	def testShouldTranslateDCATCorrectly(self):
		sampleDCATDict = {
			'SA-S': 'sass',
			'KA-T': 'cat',
			'KA*-T': 'cath',
			}
		self.whenUsingDictionary(sampleDCATDict, 'dCAT')
		self.shouldTranslateEverythingProperly()
	
	def testShouldTranslateEclipseCorrectly(self):
		sampleEclipseDict = {
			'SAS': 'sass',
			'KAT': 'cat',
			'KA*T': 'cath',
			}
		self.whenUsingDictionary(sampleEclipseDict, 'Eclipse')
		self.shouldTranslateEverythingProperly()

	def whenUsingDictionary(self, dict, dictType):
		self.translator = Translator(10, dict, dictType)
	
	def shouldTranslateEverythingProperly(self):
		self.assertTranslates(['q', 'c', ';'], "sass")
		self.assertTranslates(['s', 'c', 'p'], "cat")
		self.assertTranslates(['s', 'c', 'y', 'p'], "cath")
	
	def assertTranslates(self, keys, expectedTranslation):
		self.translator.translate(keys)
		self.assertEquals(expectedTranslation, self.translator.mostRecentTranslation().english)

if __name__ == "__main__":
	unittest.main()
