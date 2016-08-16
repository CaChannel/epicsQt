import PyQt4.Qt as Qt
import epicsQt
import css

class eCombo(Qt.QComboBox):
    def __init__(self, parent=None, pvName=None):
        Qt.QComboBox.__init__(self, parent)
        self.setEnabled(False)
        self.setEditable(False)
        self.setStyleSheet(css.disabled)
        if pvName!=None:
            self.setPV(pvName)
        self.connect(self, Qt.SIGNAL('activated(int)'), self.choiceActivated)

    def setPV(self,pv):
        if type(pv)==str:
            self.pv=epicsQt.epicsQt(pv)
        else:
            self.pv=pv
        if self.pv.inited:
            self.setEnabled(True)
            self.controlInfo()
            self.valueChanged()
        self.connect(self.pv, Qt.SIGNAL('stateChanged(int)'), self.stateChanged)
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
        if   self.pv.pv_severity==0: self.setStyleSheet(css.normal)
        elif self.pv.pv_severity==1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity==2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity==3: self.setStyleSheet(css.invalid)

        self.setCurrentIndex(self.pv.pv_value)
    
    def stateChanged(self, state):
        if state!=2:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
        else:
            self.setEnabled(True)
