#!/usr/bin/env python

from PyQt4 import QtGui, QtCore, QtDesigner
from epicsQt import eButton

def Q_TYPEID(class_name):
    return QtCore.QString("com.trolltech.Qt.Designer.TaskMenu")


class eButtonPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent = None):
        QtDesigner.QPyDesignerCustomWidgetPlugin.__init__(self)
        self.initialized = False

    def initialize(self, formEditor):
        if self.initialized:
            return

        manager = formEditor.extensionManager()
        if manager:
            self.factory = eButtonTaskMenuFactory(manager)
            manager.registerExtensions(
                self.factory, Q_TYPEID("QPyDesignerTaskMenuExtension")
                )

        self.initialized = True

    def isInitialized(self):
        return self.initialized

    # This factory method creates new instances of our custom widget with the
    # appropriate parent.
    def createWidget(self, parent):
        widget = eButton(parent)
        return widget

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "eButton"

    # Returns the name of the group in Qt Designer's widget box that this
    # widget belongs to.
    def group(self):
        return "EPICS Widget"

    # Returns the icon used to represent the custom widget in Qt Designer's
    # widget box.
    def icon(self):
        return QtGui.QIcon()

    # Returns a short description of the custom widget for use in a tool tip.
    def toolTip(self):
        return ""

    # Returns a short description of the custom widget for use in a "What's
    # This?" help message for the widget.
    def whatsThis(self):
        return ""

    # Returns True if the custom widget acts as a container for other widgets;
    # otherwise returns False. Note that plugins for custom containers also
    # need to provide an implementation of the QDesignerContainerExtension
    # interface if they need to add custom editing support to Qt Designer.
    def isContainer(self):
        return False

    # Returns an XML description of a custom widget instance that describes
    # default values for its properties. Each custom widget created by this
    # plugin will be configured using this description.
    def domXml(self):
        return '<widget class="eButton" name=\"eButton\" />\n'

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "epicsQt/eButton"


class eButtonTaskMenuFactory(QtDesigner.QExtensionFactory):
    def __init__(self, parent = None):
        QtDesigner.QExtensionFactory.__init__(self, parent)

    # This standard factory function returns an object to represent a task
    # menu entry.
    def createExtension(self, obj, iid, parent):

        if iid != Q_TYPEID("QPyDesignerTaskMenuExtension"):
            return None

        # We pass the instance of the custom widget to the object representing
        # the task menu entry so that the contents of the custom widget can be
        # modified.
        if isinstance(obj, eButton):
            return eButtonTaskMenu(obj, parent)

        return None


class eButtonTaskMenu(QtDesigner.QPyDesignerTaskMenuExtension):

    def __init__(self, obj, parent):
        QtDesigner.QPyDesignerTaskMenuExtension.__init__(self, parent)
        self.eWidget=obj
        self.setPVAction = QtGui.QAction("Set PV...", self)
        self.connect(self.setPVAction, QtCore.SIGNAL("triggered()"),
                     self.setPV)

    def preferredEditAction(self):
        return self.setPVAction

    def taskActions(self):
        return [self.setPVAction]

    @QtCore.pyqtSignature("setPV()")
    def setPV(self):
        pv,ok=QtGui.QInputDialog.getText(None,'Assign PV name','PV Name:',QtGui.QLineEdit.Normal,self.eWidget.getPvName())
        if ok:
            formWindow = QtDesigner.QDesignerFormWindowInterface.findFormWindow(self.eWidget)
            if formWindow:
                formWindow.cursor().setProperty("pvName",
                            QtCore.QVariant(pv))
