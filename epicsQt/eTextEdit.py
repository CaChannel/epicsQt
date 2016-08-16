import PyQt4.Qt as Qt
import epicsQt
import css

class eTextEdit(Qt.QTextEdit):
    def __init__(self, parent=None, pvName=None):
        Qt.QTextEdit.__init__(self, parent)
        self.setEnabled(False)
        self.setStyleSheet(css.disabled)
        if pvName!=None:
            self.setPV(pvName)
        self.connect(self, Qt.SIGNAL('textChanged()'), self.editChanged)

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

    # Qt signals
    def editChanged(self):
        txt = [ord(c) for c in str(self.toPlainText())]
        if txt:
            self.pv.array_put(txt)
        else:
            self.pv.array_put([0])

#    def keyPressEvent(self,event):
#        if event.key()==Qt.Qt.Key_Return or event.key()==Qt.Qt.Key_Enter:
#            if self.validator()!=None and self.validator().validate(self.text(),0)[0]!=Qt.QValidator.Acceptable:
#                self.setText(str(self.pv.pv_value))
#        Qt.QLineEdit.keyPressEvent(self, event)

    # EPICS signals
    def valueChanged(self):
        if   self.pv.pv_severity==0: self.setStyleSheet(css.normal)
        elif self.pv.pv_severity==1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity==2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity==3: self.setStyleSheet(css.invalid)

        if self.pv.field_type()==epicsQt.CaChannel.ca.DBF_CHAR:
            txt = ''.join(chr(c) for c in self.pv.pv_value if c != 0)
            if txt!= str(self.toPlainText()):
                self.setPlainText(txt)

        self.emit(Qt.SIGNAL('valueChanged()'))

    def stateChanged(self, state):
        if state!=2:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)
        else:
            self.setEnabled(True)
            self.setReadOnly(not self.pv.write_access())
