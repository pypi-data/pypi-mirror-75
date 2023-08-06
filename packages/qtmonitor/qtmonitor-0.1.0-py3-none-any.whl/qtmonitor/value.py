""" Module provides a widget for storing value data """
from .base import qw, qg, qc


class Value(qw.QFrame):
    """ The widget for storing monitore value data """

    _css = 'QFrame#value {' \
           '    border-radius: 4px;' \
           '    background: rgb(70, 70, 70);' \
           '}' \
           'QLabel {color:white;}'

    def __init__(self, name, func, interval, value_range, parent=None):
        """
        Constructor

        Args:
            name (str): Value name or short description
            func: A method which will be called to get the value
            interval (int): Timeout interval in milliseconds before
                            reloading the value
            value_range (list, tuple, None): If provided a value range,
                                             it will be used to represent the
                                             current value on a progressbar
                                             within the ``Value`` widget.
                                             Default: ``None``
            parent (PySide2.QtWidgets.QWidget): Parent widget

        """
        super(Value, self).__init__(parent)

        self._func = func
        self._repeat = interval
        self._range = value_range

        # Layouts
        lay_main = qw.QHBoxLayout()

        # Widgets
        lbl_name = qw.QLabel(name, self)
        lbl_sep = qw.QLabel(':', self)
        self.lbl_value = qw.QLabel(self)

        # Styling
        self.setObjectName('value')
        self.setStyleSheet(self._css)
        font = qg.QFont()
        font.setBold(True)
        lbl_name.setFont(font)

        # Assembling
        lay_main.addWidget(lbl_name)
        lay_main.addWidget(lbl_sep)
        lay_main.addStretch()
        lay_main.addWidget(self.lbl_value)

        for lbl in (lbl_name, lbl_sep):
            lay_main.setAlignment(lbl, qc.Qt.AlignTop)

        self.setLayout(lay_main)

        # Timer
        self._timer = qc.QTimer(self)
        self._timer.setInterval(interval)

        # Connections
        self._timer.timeout.connect(self.on_timer_ended)

        # Pre-run
        self._timer.start()

    @qc.Slot()
    def on_timer_ended(self):
        """ Slot for handling QTimer timeout signals """
        self.update_value()

    def update_value(self):
        """
        Method get executed every time the inter timer has a timeout
        and updates the represented **value**.
        """
        try:
            value = self._func()

            if isinstance(value, (bool, int, float)) or value is None:
                value = str(value)

            if isinstance(value, (list, tuple)):
                value = '<br>'.join([str(x) for x in value])

            if isinstance(value, dict):
                value = '<br>'.join([f'{k}: {v}' for k, v in value.items()])

        except Exception as exp:
            value = f'{exp.__class__.__name__}: {str(exp)}'

        self.lbl_value.setText(value)
