import PyQt4.Qt as Qt
import epicsQt
import css

class eTime(Qt.QTimeEdit):
    def __init__(self, parent, pvHour,pvMinute,pvSecond):
        Qt.QTimeEdit.__init__(self,parent)
        self.setEnabled(False)
        
        self.pvH=epicsQt.epicsQt(pvHour)
        self.connect(self.pvH, Qt.SIGNAL('stateChanged(int)'), self.stateChanged)
        self.connect(self.pvH, Qt.SIGNAL('valueChanged()'), self.valueChanged)
        self.pvM=epicsQt.epicsQt(pvMinute)
        self.connect(self.pvM, Qt.SIGNAL('stateChanged(int)'), self.stateChanged)
        self.connect(self.pvM, Qt.SIGNAL('valueChanged()'), self.valueChanged)
        self.pvS=epicsQt.epicsQt(pvSecond)
        self.connect(self.pvS, Qt.SIGNAL('stateChanged(int)'), self.stateChanged)
        self.connect(self.pvS, Qt.SIGNAL('valueChanged()'), self.valueChanged)

        self.connect(self, Qt.SIGNAL('timeChanged(QTime)'),self.slotTimeChanged)

    def valueChanged(self):
        # avoid infinite loop
        self.disconnect(self, Qt.SIGNAL('timeChanged(QTime)'), self.slotTimeChanged)
        h = self.pvH.pv_value
        m = self.pvM.pv_value
        s = self.pvS.pv_value
        # count for cases where minutes and seconds are above 60 
        m += s / 60
        s %= 60        
        h += m / 60
        m %= 60

        self.setTime(Qt.QTime(h,m,s))
        self.connect(self, Qt.SIGNAL('timeChanged(QTime)'), self.slotTimeChanged)

    def slotTimeChanged(self,time):
        h = time.hour()
        m = time.minute()
        s = time.second()
        seconds = 3600 * h + 60 * m + s
        self.pvH.array_put(0)
        self.pvM.array_put(0)
        self.pvS.array_put(seconds)

    def stateChanged(self, state):
        if state!=2:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
        else:
            self.setEnabled(True)
            self.setStyleSheet(css.normal)
