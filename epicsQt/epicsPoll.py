import ca
import time, threading

#threading version doesnt work
#class epicsPoll(threading.Thread):
#    def __init__(self):
#        threading.Thread.__init__(self)
#        self._stop=False
#        
#    def run(self):
#        while not self._stop:
#            time.sleep(1)
#            print 'hehe'
#            ca.poll()
#    
#    def stop(self):
#        self._stop=True

#Qt version

import PyQt4.Qt as Qt
class epicsPoll(Qt.QObject):
    def __init__(self):
        Qt.QObject.__init__(self)
        self.startTimer(100)
    def timerEvent(self, event):
        ca.poll()
