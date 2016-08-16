import PyQt4.Qt as Qt
import epicsQt
import css

class eLCD(Qt.QLCDNumber):
    def __init__(self, parent=None, pvName=None):
        Qt.QLCDNumber.__init__(self, parent)
        self.setFrameStyle(Qt.QFrame.StyledPanel|Qt.QFrame.Raised)
        self.setSegmentStyle(Qt.QLCDNumber.Flat)
        self.setEnabled(False)
        self.setStyleSheet(css.disabled)
        if pvName!=None:
            self.setPV(pvName)

    def setPV(self,pv):
        if type(pv)==str:
            self.pv=epicsQt.epicsQt(pv)
        else:
            self.pv=pv
        if self.pv.inited:
            self.setEnabled(True)
            self.valueChanged()
        self.connect(self.pv, Qt.SIGNAL('stateChanged(int)'), self.stateChanged)
        self.connect(self.pv, Qt.SIGNAL('valueChanged()'),self.valueChanged)

    def getPvName(self):
        return self.pv.name()
    def setPvName(self, name):
        self.setPV(str(name))

    pvName = Qt.pyqtProperty("QString", getPvName, setPvName)

    # EPICS signals
    def valueChanged(self):
        # FIXME: How to do with INVALID (pv_severity=3)
        if   self.pv.pv_severity==0: self.setStyleSheet(css.normal)
        elif self.pv.pv_severity==1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity==2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity==3: self.setStyleSheet(css.invalid)

        if self.pv.field_type()==epicsQt.CaChannel.ca.DBF_DOUBLE or \
           self.pv.field_type()==epicsQt.CaChannel.ca.DBF_FLOAT:
            if hasattr(self.pv, 'pv_precision'): format='%%.%df'%self.pv.pv_precision
            else: format='%f'
            self.display(format%self.pv.pv_value)
        else:
            self.display(str(self.pv.pv_value))

        # re-emit it for upper level applications
        self.emit(Qt.SIGNAL('valueChanged()'))

    def stateChanged(self, state):
        if state!=2:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
        else:
            self.setEnabled(True)
