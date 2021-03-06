import PyQt4.Qt as Qt
from .epicsQt import epicsQt
from . import css


class eButtonGroup(Qt.QFrame):
    def __init__(self, parent=None, pvName=None, h=True):
        Qt.QFrame.__init__(self, parent)
        self.setStyleSheet(css.disabled)
        self.setEnabled(False)
        if pvName is not None:
            self.setPV(pvName)
        if h:
            self.layout = Qt.QHBoxLayout(self)
        else:
            self.layout = Qt.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.btngrp = Qt.QButtonGroup(self)
        self.btngrp.setExclusive(True)
        self.connect(self.btngrp, Qt.SIGNAL('buttonClicked(int)'), self.buttonClicked)

    def setPV(self, pv):
        if isinstance(pv, str):
            self.pv = epicsQt(pv)
        else:
            self.pv = pv
        self.connect(self.pv, Qt.SIGNAL('connectionChanged(bool)'), self.connectionChanged)
        self.connect(self.pv, Qt.SIGNAL('controlInfo()'), self.controlInfo)
        self.connect(self.pv, Qt.SIGNAL('valueChanged()'), self.valueChanged)

    def getPvName(self):
        return self.pv.name()

    def setPvName(self, name):
        self.setPV(str(name))

    pvName = Qt.pyqtProperty("QString", getPvName, setPvName)

    def controlInfo(self):
        if hasattr(self.pv, 'pv_statestrings'):
            for state_no, state_str in enumerate(self.pv.pv_statestrings):
                btn = Qt.QPushButton(state_str, self)
                btn.setCheckable(True)
                self.layout.addWidget(btn)
                self.btngrp.addButton(btn, state_no)
                if state_no == self.pv.pv_value:
                    btn.setChecked(True)

    def buttonClicked(self, index):
        self.emit(Qt.SIGNAL('buttonClicked(int)'), index)
        self.pv.array_put(index)

    def valueChanged(self):
        if self.pv.pv_severity == 0:   self.setStyleSheet(css.normal)
        elif self.pv.pv_severity == 1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity == 2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity == 3: self.setStyleSheet(css.invalid)

        btn = self.btngrp.button(self.pv.pv_value)
        if btn and not btn.isChecked():
            btn.setChecked(True)

    def connectionChanged(self, connected):
        if connected:
            self.setEnabled(True)
        else:
            self.setStyleSheet(css.disabled)
            self.setEnabled(False)
