"""
qtMonitor helps creating simple UIs to show real-time
values for (robotics) debugging
"""
import sys
from .base import qw
from .base import set_palette_dark
from .monitor import Monitor


__version__ = '0.1.0'


def run(name, monitor_widget):
    """
    Convenience method for running the monitor. Create a custom monitor class
    and pass it as ``monitor_widget`` argument along with a ``name``.

    Args:
        name (str): Title for the dialog
        monitor_widget: custom ``qtmonitor.Monitor`` subclass

    """
    app = qw.QApplication(sys.argv)
    if name:
        app.setApplicationName(name)

    dlg = monitor_widget()

    if not isinstance(dlg, Monitor):
        raise AttributeError(f'Please provide a qtmonitor.monitor.Monitor '
                             f'instance as ``monitor``. '
                             f'Found: {monitor_widget} | '
                             f'Type: {type(monitor_widget)}')

    set_palette_dark(dlg)
    dlg.show()
    sys.exit(app.exec_())
