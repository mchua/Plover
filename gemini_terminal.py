import serial
from translation import Translator
import geminipr
import eclipseDict 

def main(stenoDict, stenoDictType):
    # open first serial port
    ser = serial.Serial(7)  
    #ser = serial.Serial(7)  
    print("Using %s." % ser.portstr)
    # Create translation engine.
    translator = Translator(30, stenoDict, stenoDictType, geminipr.Stroke)
    while True:
        # read six bytes
        x = ser.read(6)
        translator.translate(x)
        print(translator.fullTranslation())

if __name__ == "__main__":
    main(eclipseDict.exportDic, 'Eclipse')
