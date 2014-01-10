import types
import logging as log

# Decorator log level.
DECLEV = log.DEBUG

log.basicConfig(filename='logs/mine.log',
                level=log.DEBUG,
                filemode='w',
                format=('%(filename)-12s:%(lineno)-3s %(funcName)-20s >> '
                        '%(levelname)-8s - %(message)s'))


class logwrap:
    """Wrapper function for Mine.  For use as a decorator."""

    def __init__(self, f):
        """Decorator init call"""
        self.func = f

    def __call__(self, *args, **kwargs):
        """Decorator active call to function"""
        log.log(DECLEV, '{{ Entry {0}; args: {1}, {2}'.format(
            self.func.__name__, args, kwargs))
        self.func(*args, **kwargs)
        log.log(DECLEV, '}} Exit {0}'.format(self.func.__name__))

    def __get__(self, instance, cls):
        """Decorator get call for the descriptor protocol"""
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)
