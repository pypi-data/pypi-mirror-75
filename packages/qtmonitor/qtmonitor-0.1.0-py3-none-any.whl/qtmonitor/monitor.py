"""
Module provides the main class for creating custom Monitors
"""
from .base import qw
from .group import Group


class Monitor(qw.QScrollArea):
    """ Subclass this, add groups and values to create a own custom monitor """

    _css = 'QScrollArea {border: 0px;}' \
           'QFrame#scrollAreaContainer {' \
           '    background: rgb(55, 55, 55);' \
           '}'

    def __init__(self, parent=None, compact=False):
        """
        Constructor

        Args:
            parent (PySide2.QtWidgets.QWidget): Parent widget
            compact (bool): Whether to make groups as compact as possible.
                            Default: ``False``

        """
        super(Monitor, self).__init__(parent)
        self._compact = compact

        # Layouts
        self.lay_main = qw.QHBoxLayout()

        # Widgets
        wgt_main = qw.QFrame(self)

        # Styling
        wgt_main.setObjectName('scrollAreaContainer')
        self.setStyleSheet(self._css)

        # self.lay_main.setSpacing(2)

        # Assembling
        if self._compact:
            self.lay_main.addStretch()

        wgt_main.setLayout(self.lay_main)

        self.setWidget(wgt_main)
        self.setWidgetResizable(True)

    def add_group(self, name):
        """
        Adds a group to the monitor

        Args:
            name (str): Group name

        Returns:
            Group:
                Added group. Use this instance to add **values**.

        """
        grp = Group(name, self)
        if self._compact:
            self.lay_main.insertWidget(self.lay_main.count()-1, grp)
        else:
            self.lay_main.addWidget(grp)

        return grp

    def clear(self):
        """ Clears the monitor. """
        if self.lay_main.count() > 0:
            for i in reversed(range(self.lay_main.count())):
                wgt = self.lay_main.takeAt(i).widget()
                if wgt:
                    wgt.setParent(None)
        if self._compact:
            self.lay_main.addStretch()
