import PyQt4.Qt as Qt
from .epicsQt import epicsQt
from . import css


class eButton(Qt.QPushButton):
    def __init__(self, parent=None, pvName=None, message=(None, None)):
        Qt.QPushButton.__init__(self, parent)
        self.setEnabled(False)
        self.setStyleSheet(css.disabled)
        self._offMessage, self._onMessage = message
        if pvName is not None:
            self.setPV(pvName)
        self.connect(self, Qt.SIGNAL('pressed()'), self.buttonPressed)
        self.connect(self, Qt.SIGNAL('released()'), self.buttonReleased)

    def setPV(self, pv):
        if isinstance(pv, str):
            self.pv = epicsQt(pv)
        else:
            self.pv = pv
        if self.pv.inited:
            self.setEnabled(True)
            self.setStyleSheet("")
        self.connect(self.pv, Qt.SIGNAL('connectionChanged(bool)'), self.connectionChanged)

    def getPvName(self):
        return self.pv.name()

    def setPvName(self, name):
        self.setPV(str(name))

    def getOnMessage(self):
        return self._onMessage

    def setOnMessage(self, on):
        self._onMessage = on

    def getOffMessage(self):
        return self._offMessage

    def setOffMessage(self, off):
        self._offMessage = off

    pvName = Qt.pyqtProperty("QString", getPvName, setPvName)
    onMessage = Qt.pyqtProperty("QString", getOnMessage, setOnMessage)
    offMessage = Qt.pyqtProperty("QString", getOffMessage, setOffMessage)

    def buttonPressed(self):
        if self._onMessage is not None:
            self.pv.array_put(self._onMessage)

    def buttonReleased(self):
        if self._offMessage is not None:
            self.pv.array_put(self._offMessage)

    def connectionChanged(self, connected):
        if connected:
            self.setEnabled(True)
            self.setStyleSheet("")
        else:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
