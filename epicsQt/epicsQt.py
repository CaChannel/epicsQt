import PyQt4.Qt as Qt
from CaChannel import ca, CaChannel


class epicsQt(CaChannel, Qt.QObject):
    def __init__(self, pvName=None):
        Qt.QObject.__init__(self)
        CaChannel.__init__(self)
        self.never_conn = True
        self.inited = False
        if pvName is not None:
            self.search_and_connect(pvName, self.connectCB)

    # Callback functions
    def controlCB(self, epicsArgs, _):
        for key in epicsArgs.keys():
            setattr(self, key, epicsArgs[key])
        self.inited = True
        self.emit(Qt.SIGNAL('controlInfo()'))

    def valueCB(self, epicsArgs, _):
        for key in epicsArgs.keys():
            setattr(self, key, epicsArgs[key])
        self.emit(Qt.SIGNAL('valueChanged()'))

    def connectCB(self, epicsArgs, _):
        conn = epicsArgs[1] == ca.CA_OP_CONN_UP
        # setup valueCB only in the first time
        if conn and self.never_conn:
            # register monitor for value and alarm change
            self.add_masked_array_event(ca.dbf_type_to_DBR_STS(self.field_type()), None,
                                        ca.DBE_VALUE | ca.DBE_ALARM, self.valueCB)
            # retrieve the control information
            self.array_get_callback(ca.dbf_type_to_DBR_CTRL(self.field_type()), None, self.controlCB)
            self.never_conn = False
        self.emit(Qt.SIGNAL('connectionChanged(bool)'), conn)
