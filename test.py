import PyQt4.Qt as Qt
from epicsQt import epicsQt,epicsPoll,eLabel,eEdit,eIntSpin, eButtonGroup,\
    eDoubleSpin,eButton, eCombo, eCheckBox, eLCD, eTextEdit

import sys, time


def choosePV(index):
    mylabel.setPV(pvs[index])

if __name__=='__main__':
    app = Qt.QApplication(sys.argv)

    win = Qt.QWidget()

    poll = epicsPoll()

    pvs=[]
    pvs.append(epicsQt('catest'))
    pvs.append(epicsQt('cabo'))
    
    layout = Qt.QVBoxLayout()
    win.setLayout(layout)

    label = Qt.QLabel('cawavec (waveform of char)', win)
    layout.addWidget(label)

    edit = eTextEdit(win, 'cawavec')
    layout.addWidget(edit)

    edit = eEdit(win, 'cawavec')
    layout.addWidget(edit)

    label = Qt.QLabel('dynamic PV assignment', win)
    layout.addWidget(label)

    combo = Qt.QComboBox()
    combo.addItems(['catest','cabo'])
    Qt.QObject.connect(combo, Qt.SIGNAL('activated(int)'),choosePV)
    layout.addWidget(combo)

    mylabel = eLabel(win)
    layout.addWidget(mylabel)

    label = Qt.QLabel('catest (ai)', win)
    layout.addWidget(label)

    edit = eEdit(win,'catest')
    layout.addWidget(edit)

    fspin2 = eDoubleSpin(win, 'catest')
    layout.addWidget(fspin2)

    fspin = eEdit(win, 'catest')
    layout.addWidget(fspin)

    lcd  = eLCD(win, 'catest')
    layout.addWidget(lcd)

    label = Qt.QLabel('cabo (bo)', win)
    layout.addWidget(label)

    button = eCombo(win, 'cabo')
    layout.addWidget(button)

    check = eCheckBox(win, 'cabo')
    check.setText('Auto Start')
    layout.addWidget(check)

    btngrp = eButtonGroup(win, 'cabo', h=False)
    layout.addWidget(btngrp)


    win.show()

    sys.exit(app.exec_())
