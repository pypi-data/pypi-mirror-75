#!/usr/bin/env python3

from .alerts import is_trace, trace, alert_level, L_TRACE

def fntrace(func):
    """Decorator: trace decorated function if trace level is set."""
    def wrapper(*args, **kwargs):
        if is_trace():
            s = "call {}({}".format(func.__name__, ', '.join(map(repr, args)))
            if kwargs:
                for k, v in kwargs.items():
                    s += ", {}={}".format(k, repr(v))
            trace(s + ")")
        return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":

    alert_level(L_TRACE)

    @fntrace
    def this_function(start, end, step=1):
        hadone = False
        print("=> i am func({}, {}, {})".format(
            repr(start), repr(end), repr(step))
        )
        for i in range(start, end, step):
            hadone = True
            print("{} ".format(i), end="")
        if hadone:
            print()


    print("Hoolalah")

    this_function(2, 35, step=2)
    this_function(1, 5)
