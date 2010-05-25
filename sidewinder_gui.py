import tktest
import re
import time
import os
from eclipseDict import exportDic

tktest.KeyEater(exportDic, 'Eclipse').mainloop() 
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
