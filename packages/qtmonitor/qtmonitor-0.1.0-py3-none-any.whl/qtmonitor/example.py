"""
Module for demonstrating a custom Monitor.

Usage:
    python -m qtmonitor.example

"""
import random
from qtmonitor import Monitor


STRINGS = ['blub', 'bl000b', 'foo', 'bar', 'whatever', 'and so on...']


def value_fn_int():
    """
    Example method generating random **ints**.

    Returns:
        int:
            An integer from 0 to 100
    """
    return random.randrange(0, 100)


def value_fn_float():
    """
    Example method generating random **floats**.

    Returns:
        float:
            A float from 0.0 to 1.0

    """
    return float(random.randrange(0, 100) / 100.0)


def value_fn_str():
    """
    Example method generating random **stings**.

    Returns:
        str:
            Random string

    """
    return random.choice(STRINGS)


def value_fn_bool():
    """
    Example method generating bool values

    Returns:
        True, False, None:
            A bool or ``None``

    """
    return random.choice((True, False, None))


def value_fn_list():
    """
    Example method generating **list** of ints.

    Returns:
        list:
            List of ints from 0 to 1000
    """
    ret_list = list()

    for _ in range(3):
        ret_list.append(random.randrange(0, 1000))

    return ret_list


def value_fn_dict():
    """
    Example method generating **dicts** with random ints

    Returns:
        dict:
            A dictionary with 3 keys ('tx', 'ty' and 'tz')
            with random **ints** from 0 to 1000.

    """
    return {
        'tx': random.randrange(0, 1000),
        'ty': random.randrange(0, 1000),
        'tz': random.randrange(0, 1000)
    }


class ExampleMonitor(Monitor):
    """
    Example ``Monitor`` subclass with multiple groups and values
    with various timeouts. Use it as example for creating own monitors.
    """

    def __init__(self, parent=None):
        """
        Constructor

        Args:
            parent (PySide2.QtWidgets.QWidget): Parent widget

        """
        super(ExampleMonitor, self).__init__(parent)

        # Add the first group
        grp_main = self.add_group('Main')

        # Add first group values
        grp_main.add_value('Int', value_fn_int)
        grp_main.add_value('Float', value_fn_float)
        grp_main.add_value('String', value_fn_str)
        grp_main.add_value('Bool', value_fn_bool)
        grp_main.add_value('List', value_fn_list)
        grp_main.add_value('Dict', value_fn_dict)

        # Add a rapid fire group with multiple timer intervals
        grp_rapid_fire = self.add_group('Rapid Fire')

        # Add values with various intervals
        for interval in (10000, 5000, 1000, 500, 100, 10):
            grp_rapid_fire.add_value(
                f'{interval} ms', value_fn_int, interval=interval
            )


if __name__ == '__main__':
    from qtmonitor import run
    run('Example monitor', ExampleMonitor)
