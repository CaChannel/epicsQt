import PyQt4.Qt as Qt
import epicsQt
import css

class eCheckBox(Qt.QCheckBox):
    def __init__(self, parent=None, pvName=None):
        Qt.QPushButton.__init__(self, parent)
        self.setEnabled(False)
        self.setStyleSheet(css.disabled)
        if pvName!=None:
            self.setPV(pvName)
        self.connect(self, Qt.SIGNAL('stateChanged(int)'), self.boxChecked)

    def setPV(self,pv):
        if type(pv)==str:
            self.pv=epicsQt.epicsQt(pv)
        else:
            self.pv=pv
        if self.pv.inited:
            self.setEnabled(True)
            self.valueChanged()
        self.connect(self.pv, Qt.SIGNAL('stateChanged(int)'), self.stateChanged)
        self.connect(self.pv, Qt.SIGNAL('valueChanged()'), self.valueChanged)

    def getPvName(self):
        return self.pv.name()
    def setPvName(self, name):
        self.setPV(str(name))

    pvName = Qt.pyqtProperty("QString", getPvName, setPvName)

    # Qt signals
    def boxChecked(self, state):
        if state == Qt.Qt.Checked:
            self.pv.array_put(1)
        if state == Qt.Qt.Unchecked:
            self.pv.array_put(0)

    # EPICS signals
    def valueChanged(self):
        if   self.pv.pv_severity==0: self.setStyleSheet(css.normal)
        elif self.pv.pv_severity==1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity==2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity==3: self.setStyleSheet(css.invalid)
        
        if self.pv.pv_value==1:
            self.setCheckState(Qt.Qt.Checked)
        if self.pv.pv_value==0:
            self.setCheckState(Qt.Qt.Unchecked)
        try:
            status=self.pv.pv_statestrings[self.pv.pv_value]
            self.setText(status)
        except KeyError:
            pass
        
    def stateChanged(self, state):
        if state!=2:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
        else:
            self.setEnabled(True)
