____To launch Plover____

First, install Python 3.1: http://python.org/download/releases/3.1.2/

**With SideWinder X4**

Required files (must all be in the same directory): translation.py,
tktest.py, sidewinder_gui.py (or dcsidewinder_gui.py), eclipseDict.py
(or your dCAT formatted dictionary).

- If you have a steno dictionary exported from Eclipse (like the default
Plover dictionary on the GitHub), make sure it's named eclipseDict.py,
then launch sidewinder_gui.py.

- If you have a steno dictionary exported from DigitalCAT into Python
format, rename it dCATDict.py and launch dcsidewinder_gui.py.

**With Gemini PR protocol steno machine**

Required files (must all be in the same directory): translation.py,
serial_gui.py, eclipseDict.py. 

- Open serial_gui.py and search for "self.ser". It should take you to a
line that reads "self.ser = serial.Serial(7)". Change the number in the
parentheses to the one that matches your serial port. Make sure you
have PySerial installed. (http://pyserial.sourceforge.net/) Then
launch serial_gui.py.

- If you're using Linux rather than Windows, you may need to toggle the
capitalization of "tkinter" and "queue" in certain files.

____Plover text output____

Currently Plover exports all the text of a session into a single-line
file, and cleans up the formatting to a certain degree. The text file
will be named "Plover" plus 12 digits representing the date and time.
DigitalCAT dictionary owners will need to have their dictionaries
re-converted by Plover developers to take advantage of the formatting
clean-up. There aren't any sophisticated or grammatical suffix or
spelling rules in place yet, but simple punctuation and capitalization
should work most of the time if your dictionary has been formatted
correctly.  

____To do_____

* Fix the Sidewinder bug that causes freezing when too many keys are
pressed at one time.

* Add more formatting rules, including rules for paragraphing, so that
the text file isn't just in one long line.

* Add more sophisticated grammar rules, to eliminate doubled vowels in
suffixes and to add doubled consonants where appropriate.

* Add support for Gemini TX and Stentura serial protocols.

* Consolidate program files.

* Display properly formatted text in GUI.

* Add support for cross-platform editing directly into open OS windows.

--
Please email bugs to plover@stenoknight.com or post them at
http://plover.stenoknight.com or http://github.com/stenoknight/Plover.

