from CaChannel import ca
import PyQt4.Qt as Qt


class epicsPoll(Qt.QObject):
    def __init__(self):
        Qt.QObject.__init__(self)
        self.startTimer(100)

    def timerEvent(self, event):
        ca.poll()
