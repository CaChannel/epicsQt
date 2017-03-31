epicsQt
=======

`epicsQt` is a QObject representing an EPICS PV connection.

Based on it there is a set of PyQt widgets which has epics awareness.
They are here to integrate epics into existing PyQt applications.

+--------------+----------------+
| Widget type  |  Description   |
+==============+================+
| eButton      | Message button |
+--------------+----------------+
| eButtonGroup | Choice button  |
+--------------+----------------+
| eCheckbox    | Boolean button |
+--------------+----------------+
| eCombo       | Choice menu    |
+--------------+----------------+
| eDoubleSpin  | Numeric input  |
+--------------+----------------+
| eIntSpin     | Integer input  |
+--------------+----------------+
| eLCD         | Integer dislay |
+--------------+----------------+
| eLabel       | Text display   |
+--------------+----------------+
| eTextEdit    | Text input     |
+--------------+----------------+

Their designer plugins can be used, if PyQt installed,
    $ export PYQTDESIGNERPATH=<epicsQt>/plugin/

