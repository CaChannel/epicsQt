import PyQt4.Qt as Qt
import epicsQt
import css

class eButton(Qt.QPushButton):
    def __init__(self, parent=None, pvName=None):
        Qt.QPushButton.__init__(self, parent)
        self.setEnabled(False)
        self.setStyleSheet(css.disabled)
        if pvName!=None:
            self.setPV(pvName)
        self.connect(self, Qt.SIGNAL('clicked()'), self.buttonClicked)

    def setPV(self, pv):
        if type(pv)==str:
            self.pv=epicsQt.epicsQt(pv)
        else:
            self.pv=pv
        if self.pv.inited:
            self.setEnabled(True)
            self.setStyleSheet("")
        self.connect(self.pv, Qt.SIGNAL('stateChanged(int)'), self.stateChanged)

    def getPvName(self):
        return self.pv.name()
    def setPvName(self, name):
        self.setPV(str(name))

    pvName = Qt.pyqtProperty("QString", getPvName, setPvName)

    def buttonClicked(self):
        self.pv.array_put(1)

    def stateChanged(self, state):
        if state!=2:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
        else:
            self.setEnabled(True)
            self.setStyleSheet("")
