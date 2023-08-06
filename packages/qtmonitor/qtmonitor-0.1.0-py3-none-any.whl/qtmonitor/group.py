""" Module responsible for the Group widget """
from .base import qw
from .value import Value


class Group(qw.QGroupBox):
    """
    The widget which gets created from the main ``Monitor`` class.

    Every monitor needs at least one ``Group``,
    which than can add various ``Values``.

    """

    _css = 'QGroupBox {' \
           '    color: white;' \
           '    border: 1px solid rgb(128, 128, 128);' \
           '    border-radius: 4px;' \
           '    margin-top: 6px;' \
           '}' \
           'QGroupBox::title {' \
           '    subcontrol-origin: margin;' \
           '    left: 7px;  ' \
           '    padding: 0px 5px 0px 5px;' \
           '}'

    def __init__(self, name, parent=None):
        """
        Constructor

        Args:
            name (str): Group name
            parent (PySide2.QtWidgets.QWidget): Parent widget
        """
        super(Group, self).__init__(name, parent)

        # Layouts
        lay_main = qw.QVBoxLayout()
        self.lay_content = qw.QVBoxLayout()

        # Widgets
        wgt_scroll_area = qw.QScrollArea(self)
        wgt_content = qw.QFrame(self)

        # Styling
        self.setStyleSheet(self._css)
        self.lay_content.setContentsMargins(0, 0, 0, 0)

        # Assembling
        self.lay_content.addStretch()
        wgt_content.setLayout(self.lay_content)

        wgt_scroll_area.setWidget(wgt_content)
        wgt_scroll_area.setWidgetResizable(True)
        wgt_content.setObjectName('scrollAreaContainer')

        lay_main.addWidget(wgt_scroll_area)
        self.setLayout(lay_main)

    def add_value(self, name, func, interval=1000, value_range=None):
        """
        Adds a *trackable* value to the group.

        Args:
            name (str): Value name / description
            func: A method which will be called to get the value
            interval (int): Timeout interval in milliseconds before
                            reloading the value
            value_range (list, tuple, None): If provided a value range,
                                             it will be used to represent the
                                             current value on a progressbar
                                             within the ``Value`` widget.
                                             Default: ``None``

        Returns:
            Value:
                Added ``Value`` widget

        """
        wgt = Value(
            name=name,
            func=func,
            interval=interval,
            value_range=value_range,
            parent=self
        )

        self.lay_content.insertWidget(self.lay_content.count()-1, wgt)
        wgt.update_value()
        return wgt

    def clear(self):
        """ Cleans current group """
        if self.lay_content.count() > 0:
            for i in reversed(range(self.lay_content.count())):
                wgt = self.lay_content.takeAt(i).widget()
                if wgt:
                    wgt.setParent(None)
        self.lay_content.addStretch()
