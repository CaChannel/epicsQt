import PyQt4.Qt as Qt
from .epicsQt import epicsQt
from . import css


class eCombo(Qt.QComboBox):
    def __init__(self, parent=None, pvName=None):
        Qt.QComboBox.__init__(self, parent)
        self.setEnabled(False)
        self.setEditable(False)
        self.setStyleSheet(css.disabled)
        if pvName is not None:
            self.setPV(pvName)
        self.connect(self, Qt.SIGNAL('activated(int)'), self.choiceActivated)

    def setPV(self, pv):
        if isinstance(pv, str):
            self.pv = epicsQt(pv)
        else:
            self.pv = pv
        if self.pv.inited:
            self.setEnabled(True)
            self.controlInfo()
            self.valueChanged()
        self.connect(self.pv, Qt.SIGNAL('connectionChanged(bool)'), self.connectionChanged)
        self.connect(self.pv, Qt.SIGNAL('valueChanged()'), self.valueChanged)
        self.connect(self.pv, Qt.SIGNAL('controlInfo()'), self.controlInfo)

    def getPvName(self):
        return self.pv.name()

    def setPvName(self, name):
        self.setPV(str(name))

    pvName = Qt.pyqtProperty("QString", getPvName, setPvName)

    # Qt signals
    
    def choiceActivated(self, value):
        self.pv.array_put(value)

    # EPICS signals
    
    def controlInfo(self):
        for state in self.pv.pv_statestrings:
            self.addItem(state)

    def valueChanged(self):
        if self.pv.pv_severity == 0:   self.setStyleSheet(css.normal)
        elif self.pv.pv_severity == 1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity == 2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity == 3: self.setStyleSheet(css.invalid)

        self.setCurrentIndex(self.pv.pv_value)
    
    def connectionChanged(self, connected):
        if connected:
            self.setEnabled(True)
        else:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
