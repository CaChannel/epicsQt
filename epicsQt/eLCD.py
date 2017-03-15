import PyQt4.Qt as Qt
from CaChannel import ca
from .epicsQt import epicsQt
from . import css


class eLCD(Qt.QLCDNumber):
    def __init__(self, parent=None, pvName=None):
        Qt.QLCDNumber.__init__(self, parent)
        self.setFrameStyle(Qt.QFrame.StyledPanel | Qt.QFrame.Raised)
        self.setSegmentStyle(Qt.QLCDNumber.Flat)
        self.setMode(Qt.QLCDNumber.Dec)
        self.setEnabled(False)
        self.setStyleSheet(css.disabled)
        if pvName is not None:
            self.setPV(pvName)

    def setPV(self, pv):
        if isinstance(pv, str):
            self.pv = epicsQt(pv)
        else:
            self.pv = pv
        if self.pv.inited:
            self.setEnabled(True)
            self.valueChanged()
        self.connect(self.pv, Qt.SIGNAL('connectionChanged(bool)'), self.connectionChanged)
        self.connect(self.pv, Qt.SIGNAL('valueChanged()'), self.valueChanged)

    def getPvName(self):
        return self.pv.name()

    def setPvName(self, name):
        self.setPV(str(name))

    pvName = Qt.pyqtProperty("QString", getPvName, setPvName)

    # EPICS signals
    def valueChanged(self):
        # FIXME: How to do with INVALID (pv_severity=3)
        if self.pv.pv_severity == 0: self.setStyleSheet(css.normal)
        elif self.pv.pv_severity == 1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity == 2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity == 3: self.setStyleSheet(css.invalid)

        if self.pv.field_type() == ca.DBF_DOUBLE or self.pv.field_type() == ca.DBF_FLOAT:
            if hasattr(self.pv, 'pv_precision'): format = '%%.%df' % self.pv.pv_precision
            else: format = '%f'
            sval = format % self.pv.pv_value
        else:
            sval = str(self.pv.pv_value)
        self.setDigitCount(len(sval))
        self.display(sval)
        # re-emit it for upper level applications
        self.emit(Qt.SIGNAL('valueChanged()'))

    def connectionChanged(self, connected):
        if connected:
            self.setEnabled(True)
        else:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
