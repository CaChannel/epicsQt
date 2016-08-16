import PyQt4.Qt as Qt
import epicsQt
import css

class eEdit(Qt.QLineEdit):
    def __init__(self, parent=None, pvName=None):
        Qt.QLineEdit.__init__(self, parent)
        self.setEnabled(False)
        self.setStyleSheet(css.disabled)
        if pvName!=None:
            self.setPV(pvName)
        self.connect(self, Qt.SIGNAL('returnPressed()'), self.returnPressed)

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
    def returnPressed(self):
        txt = str(self.text())
        if len(txt) == 0:
            txt = '\0'
        self.pv.array_put(txt)

    def keyPressEvent(self,event):
        if event.key()==Qt.Qt.Key_Return or event.key()==Qt.Qt.Key_Enter:
            if self.validator()!=None and self.validator().validate(self.text(),0)[0]!=Qt.QValidator.Acceptable:
                self.setText(str(self.pv.pv_value))
        Qt.QLineEdit.keyPressEvent(self, event)

    # EPICS signals
    def controlInfo(self):
        lolim=None; uplim=None
        if hasattr(self.pv, 'pv_loctrllim'): lolim=self.pv.pv_loctrllim
        if hasattr(self.pv, 'pv_upctrllim'): uplim=self.pv.pv_upctrllim
        # to avoid stupid lazy developers who put lowlim=uplim=0.0
        if lolim==uplim:
            lolim=-1e20;uplim=1e20

        if self.pv.field_type()==epicsQt.CaChannel.ca.DBF_SHORT or\
           self.pv.field_type()==epicsQt.CaChannel.ca.DBF_INT or \
           self.pv.field_type()==epicsQt.CaChannel.ca.DBF_LONG:
            self.setValidator(Qt.QIntValidator(lolim,uplim,self))

        if self.pv.field_type()==epicsQt.CaChannel.ca.DBF_ENUM:
            self.setValidator(Qt.QIntValidator(0,self.pv.pv_nostrings-1,self))

        if self.pv.field_type()==epicsQt.CaChannel.ca.DBF_FLOAT or\
           self.pv.field_type()==epicsQt.CaChannel.ca.DBF_DOUBLE:
               if not hasattr(self.pv,'pv_precision'): prec=12
               else: prec=self.pv.pv_precision
               self.setValidator(Qt.QDoubleValidator(lolim,uplim,prec,self))

    def valueChanged(self):
        if   self.pv.pv_severity==0: self.setStyleSheet(css.normal)
        elif self.pv.pv_severity==1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity==2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity==3: self.setStyleSheet(css.invalid)

        if self.pv.field_type()==epicsQt.CaChannel.ca.DBF_DOUBLE or \
           self.pv.field_type()==epicsQt.CaChannel.ca.DBF_FLOAT:
            if hasattr(self.pv, 'pv_precision'): format='%%.%df'%self.pv.pv_precision
            else: format='%f'
            self.setText(format%self.pv.pv_value)
        elif self.pv.field_type()==epicsQt.CaChannel.ca.DBF_CHAR:
            txt = ''.join(chr(c) for c in self.pv.pv_value if c != 0)
            if txt!= str(self.text()):
                self.setText(txt)
        else:
            self.setText(str(self.pv.pv_value))

        self.emit(Qt.SIGNAL('valueChanged()'))

    def stateChanged(self, state):
        if state!=2:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
        else:
            self.setEnabled(True)
            self.setReadOnly(not self.pv.write_access())
