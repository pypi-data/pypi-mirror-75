"""
Module with few base methods and a BaseDialog class
"""
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
import PySide2.QtCore as qc


COLORS_DARK = {
    'bg': (53, 53, 53),
    'text': (200, 200, 200),
    'base': (48, 48, 48),
    'highlight': (54, 67, 77),

    'dis_bg': (57, 57, 57),
    'dis_base': (61, 61, 61),
    'dis_text': (112, 112, 112),
}


def set_palette_dark(widget):
    """
    Sets the **dark theme** on provided widget or app

    Args:
        widget (PySide.QtCore.QObject): a widget or application to apply
                                        **dark theme** to

    """
    if isinstance(widget, qw.QApplication):
        widget.setStyle('Fusion')
    # app.setStyleSheet(CSS_DARK.format(**UI_VARS_DARK))
    palette = qg.QPalette()

    palette.setColor(qg.QPalette.Window,
                     qg.QColor(*COLORS_DARK.get('bg')))
    palette.setColor(qg.QPalette.WindowText,
                     qg.QColor(*COLORS_DARK.get('text')))

    palette.setColor(qg.QPalette.Base,
                     qg.QColor(*COLORS_DARK.get('base')))
    palette.setColor(qg.QPalette.AlternateBase,
                     qg.QColor(*COLORS_DARK.get('bg')))

    palette.setColor(qg.QPalette.ToolTipBase,
                     qc.Qt.white)
    palette.setColor(qg.QPalette.ToolTipText,
                     qc.Qt.white)

    palette.setColor(qg.QPalette.Text,
                     qg.QColor(*COLORS_DARK.get('text')))

    palette.setColor(qg.QPalette.Button,
                     qg.QColor(*COLORS_DARK.get('bg')))
    palette.setColor(qg.QPalette.ButtonText,
                     qg.QColor(*COLORS_DARK.get('text')))

    palette.setColor(qg.QPalette.BrightText,
                     qc.Qt.red)

    palette.setColor(qg.QPalette.Highlight,
                     qg.QColor(*COLORS_DARK.get('highlight')))
    palette.setColor(qg.QPalette.HighlightedText,
                     qc.Qt.white)

    widget.setPalette(palette)
