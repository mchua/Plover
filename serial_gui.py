# Modified version of http://code.activestate.com/recipes/82965-threads-tkinter-and-asynchronous-io/

import tkinter
import time
import threading
import random
import queue
import serial
from translation import Translator
import eclipseDict
import geminipr
import re
import os

class GuiPart:
    def __init__(self, master, queue, endCommand, exportDict, dictType, strokeClass):
        # Initialization for steno-specific actions 
        self.translator = Translator(30, exportDict, dictType, strokeClass)
        self.translator.subscribe(self.emitted)
        self.translationFile = open("log.txt", "w")
        self.dictType = dictType

        # Keep track of events from the serial port.
        self.queue = queue
        
        # Set up the GUI
        frame = tkinter.Frame()
        frame.pack( expand = tkinter.YES, fill = tkinter.BOTH )
        frame.master.title( "Plover, The Open Source Steno Program" )
        frame.master.geometry( "950x50" )

        frame.message1 = tkinter.StringVar()
        frame.line1 = tkinter.Label( frame, textvariable = frame.message1 )
        frame.message1.set( "Plover for Gemini PR -- http://plover.stenoknight.com" )
        frame.line1.pack()
        
        self.message2 = tkinter.StringVar()
        frame.line2 = tkinter.Label( frame, textvariable = self.message2 )
        self.message2.set( "Dictionary Format: %s" % dictType )
        frame.line2.pack()
        
        frame.pack()

    def processIncoming(self):
        """
        Handle all the messages currently in the Queue (if any).
        """
        while self.queue.qsize():
            try:
                # Process the raw steno from the serial port.
                x = self.queue.get(0)
                self.translator.translate(x)
                self.message2.set(self.translator.fullTranslation())
            except queue.Empty:
                pass

    def emitted(self, translation) :
        if translation.isCorrection :
            tell = self.translationFile.tell()
            if translation.english : 
                i = tell - (len(translation.english) + 1)
            else :
                i = tell - (len(translation.rtfcre) + 1)
            self.translationFile.seek(i, 0)
            self.translationFile.truncate()
        else :
            if translation.english :
                out = translation.english
            else :
                out = translation.rtfcre
            self.translationFile.write(out + ' ')
        self.translationFile.flush()


class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master, exportDict, dictType, strokeClass):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication, exportDict, dictType, strokeClass)

        # open first serial port
        self.ser = serial.Serial(7)  
        # ser = serial.Serial(7)  
        print("Using %s." % self.ser.portstr)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            x = self.ser.read(6)
            self.queue.put(x)

    def endApplication(self):
        self.running = 0

rand = random.Random()
root = tkinter.Tk()

client = ThreadedClient(root, eclipseDict.exportDic, 'Eclipse', geminipr.Stroke)
root.mainloop()
translationFileRead = open("log.txt", "r")
translationFileWrite = open("write.txt", "w")
text = translationFileRead.read()
text = re.sub(r' {\^([a-zA-Z ]*)} ', lambda m: '%s ' % (m.group(1),), text)
text = re.sub(r' {([a-zA-Z ]*)\^} ', lambda m: ' %s' % (m.group(1),), text)
text = re.sub(r'{([a-zA-Z])([a-zA-Z]*)\^} ', lambda m: '%s' % (m.group(1).upper() + m.group(2),), text)
text = re.sub(r' {\.} ([a-z])', lambda m: '. %s' % (m.group(1).upper(),), text)
text = re.sub(r' {\?} ([a-z])', lambda m: '? %s' % (m.group(1).upper(),), text)
text = re.sub(r' {\!} ([a-z])', lambda m: '! %s' % (m.group(1).upper(),), text)
text = re.sub(r' {\,}', ',', text)
text = re.sub(r' {\.}', '.', text)
text = re.sub(r' {\?}', '?', text)
text = re.sub(r' {\!}', '!', text)
text = re.sub(r'^([a-z])', lambda m: '%s' % (m.group(1).upper()), text, 1)
translationFileWrite.write(text)
translationFileWrite.close()
os.rename('write.txt','plover' + time.strftime('%m%d%y%H%M%S') + '.txt')
