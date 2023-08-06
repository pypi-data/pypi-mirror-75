"""Timer.

For more information on the underlying Qt5 object see [QTimer](https://doc.qt.io/qt-5/qtimer.html).
"""

from .qt import QtCore
from .qt import bind

from .base import Base

__all__ = ['Timer', 'single_shot']

def single_shot(interval, timeout):
    QtCore.QTimer.singleShot(interval * 1e3, timeout)

@bind(QtCore.QTimer)
class Timer(Base):
    """Timer.

    >>> timer = Timer(interval=1.0, timeout=lambda: print("Done!"))
    >>> timer.start()
    """

    QtTimerTypes = {
        'precise': QtCore.Qt.PreciseTimer,
        'coarse': QtCore.Qt.CoarseTimer,
        'very_coarse': QtCore.Qt.VeryCoarseTimer
    }

    def __init__(self, *, interval=0, single_shot=False, timer_type=None,
                 timeout=None, **kwargs):
        super().__init__(**kwargs)
        self.interval = interval
        self.single_shot = single_shot
        if timer_type is not None:
            self.timer_type = timer_type
        self.timeout = timeout
        # Connect signals
        self.qt.timeout.connect(self.__handle_timeout)

    @property
    def interval(self):
        return self.qt.interval() / 1e3

    @interval.setter
    def interval(self, value):
        self.qt.setInterval(value * 1e3)

    @property
    def single_shot(self):
        return self.qt.isSingleShot()

    @single_shot.setter
    def single_shot(self, value):
        self.qt.setSingleShot(value)

    @property
    def timer_type(self):
        index = list(self.QtTimerTypes.values()).index(self.qt.timerType())
        return list(self.QtTimerTypes.keys())[index]

    @timer_type.setter
    def timer_type(self, value):
        self.qt.setTimerType(self.QtTimerTypes[value])

    @property
    def timeout(self):
        """Event called on timer timeout."""
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        self.__timeout = value

    def __handle_timeout(self):
        if callable(self.timeout):
            self.timeout()

    @property
    def active(self):
        return self.qt.isActive()

    @property
    def remaining_time(self):
        value = self.qt.remainingTime()
        if value < 0:
            return 0.
        return value * 1e3

    @property
    def timer_id(self):
        return self.qt.itmerId()

    def start(self, interval=None):
        if interval is None:
            self.qt.start()
        else:
            self.qt.start(interval * 1e3)

    def stop(self):
        self.qt.stop()
