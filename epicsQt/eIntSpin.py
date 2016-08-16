import PyQt4.Qt as Qt
import epicsQt
import css

class eIntSpin(Qt.QSpinBox):
    def __init__(self, parent=None, pvName=None):
        Qt.QSpinBox.__init__(self,parent)
        self.setFixedWidth(60)
        self.setEnabled(False)
        if pvName!=None:
            self.setPV(pvName)

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
        self.connect(self.pv, Qt.SIGNAL('valueChanged()'),self.valueChanged)
        self.connect(self.pv, Qt.SIGNAL('controlInfo()'), self.controlInfo)

    def getPvName(self):
        return self.pv.name()
    def setPvName(self, name):
        self.setPV(str(name))

    pvName = Qt.pyqtProperty("QString", getPvName, setPvName)

    # Qt signals

    # Triggered whenever there is a change.
    # Normally this is not what you want for some critical records
    # Its useful to see realtime change though
    def editingFinished(self, value):
        self.pv.array_put(self.value())

    def controlInfo(self):
        lolim=None; uplim=None
        if hasattr(self.pv, 'pv_loctrllim'):
            lolim=self.pv.pv_loctrllim
            self.setMinimum(lolim)
        if hasattr(self.pv, 'pv_upctrllim'):
            uplim=self.pv.pv_upctrllim
            self.setMaximum(uplim)

        # to avoid stupid lazy developers who put lowlim=uplim=0.0
        if lolim==uplim:
            self.setRange(-pow(2,31),pow(2,30))

        if hasattr(self.pv, 'pv_units'):
            self.setSuffix(' '+self.pv.pv_units)

    def valueChanged(self):
        if   self.pv.pv_severity==0: self.setStyleSheet(css.normal)
        elif self.pv.pv_severity==1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity==2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity==3: self.setStyleSheet(css.invalid)
        # avoid infinite loop
        self.disconnect(self, Qt.SIGNAL('valueChanged(int)'), self.editingFinished)
        self.setValue(self.pv.pv_value)
        self.connect(self, Qt.SIGNAL('valueChanged(int)'), self.editingFinished)

    def stateChanged(self, state):
        if state!=2:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
        else:
            self.setEnabled(True)
