import CaChannel

import PyQt4.Qt as Qt

class epicsQt(CaChannel.CaChannel, Qt.QObject):
    def __init__(self, pvName=None):
        Qt.QObject.__init__(self)
        CaChannel.CaChannel.__init__(self)
        self.never_conn=True
        self.inited = False
        if pvName!=None:
            self.search_and_connect(pvName, self.connectCB, pvName)

    # Callback functions

    def controlCB(self,epicsArgs,userArgs):
        for key in epicsArgs.keys():
            setattr(self, key, epicsArgs[key])
        self.inited = True
        self.emit(Qt.SIGNAL('controlInfo()'))

    def valueCB(self, epicsArgs, userArgs):
        for key in epicsArgs.keys():
            setattr(self, key, epicsArgs[key])
        self.emit(Qt.SIGNAL('valueChanged()'))

    def connectCB(self, epicsArgs, userArgs):
        state=self.state()
        # setup valueCB only in the first time
        if state==2 and self.never_conn:
            self.add_masked_array_event(CaChannel.ca.dbf_type_to_DBR_STS(self.field_type()), None,
                CaChannel.ca.DBE_VALUE | CaChannel.ca.DBE_ALARM,
                self.valueCB)
            self.array_get_callback(CaChannel.ca.dbf_type_to_DBR_CTRL(self.field_type()),
                None, self.controlCB)
            self.never_conn=False
        self.emit(Qt.SIGNAL('stateChanged(int)'), state)
