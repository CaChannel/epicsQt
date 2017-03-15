import PyQt4.Qt as Qt
from .epicsQt import epicsQt
from . import css


class eButton(Qt.QPushButton):
    def __init__(self, parent=None, pvName=None):
        Qt.QPushButton.__init__(self, parent)
        self.setEnabled(False)
        self.setStyleSheet(css.disabled)
        if pvName is not None:
            self.setPV(pvName)
        self.connect(self, Qt.SIGNAL('clicked()'), self.buttonClicked)

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

    pvName = Qt.pyqtProperty("QString", getPvName, setPvName)

    def buttonClicked(self):
        self.pv.array_put(1)

    def connectionChanged(self, connected):
        if connected:
            self.setEnabled(True)
            self.setStyleSheet("")
        else:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
