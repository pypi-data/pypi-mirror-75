# print alerts and other messages depending on a verbosity level

import os
import sys
import inspect

# properties of the alert levels; the decoration will be formatted with the
# locals() values
alert_levels = [
    # level name, message decoration, fd
    ("L_ERROR", "{program}: Error:", sys.stderr),
    ("L_NOTICE", None,   sys.stderr),
    ("L_INFO",   None,   sys.stderr),
    ("L_DEBUG",  "DBG",   sys.stderr),
    ("L_TRACE", "TRC",   sys.stderr),
]
# message decoration and output file descriptor by level, to be initialised
# below
alert_decoration = []
alert_fd = []

# initialise some data structures from the alert_levels[] properties
for i, props in enumerate(alert_levels):
    name, decoration, fd = props
    locals()[name] = i
    alert_decoration.append(decoration)
    alert_fd.append(fd)
alert_max_level = i

# default alert level
alert_level_level = 1

# the program 
program = os.path.basename(sys.argv[0])

alert_use_syslog = False

had_errors = False


def alert_config(*, level=None, program=None, level_fds=None,
                         use_syslog=None):
    if level is not None:
        alert_level(level)
    if program is not None:
        alert_program = program
    if level_fds is not None:
        alert_fd = level_fds
    if use_syslog is not None:
        alert_use_syslog = use_syslog


def alert_level(level=None):
    """Get or set the verbosity level for the alert functions.

    err() will print something with level 0 (and greater), i.e. always.
    notice() will print something with level 1 (and greater).
    info() will print something with level 2 (and greater).
    debug() will print something with level 3 (and greater).
    trace() will print something with level 4 (and greater).
    """
    global alert_level_level
        
    if level is not None:
        if type(level) is str:
            level = alert_level_map[level]
        alert_level_level = max(0, min(level, alert_max_level))
    return alert_level_level


def alert_level_name(level=None):
    """Return the name of the specified (or current) level number."""
    if level is None:
        level = alert_level_level
    return alert_levels[level][0]


def alert_level_up():
    """Increase the alert level by one.

    This is intended to be used as the callback function for the default value
    of a pgetopt option to increase the verbosity.

    """
    global alert_level_level
    if alert_level_level < alert_max_level:
        alert_level_level += 1
    return alert_level_level


def alert_level_zero():
    """Set the alert level to zero (errors only).

    This is intended to be used as the callback function for the default value
    of a pgetopt option to set the verbosity to zero.

    """
    global alert_level_level
    alert_level_level = 0
    return alert_level_level


def is_notice():
    """Return True iff the alert level is at least at notice."""
    return alert_level_level >= L_NOTICE

def is_info():
    """Return True iff the alert level is at least at info."""
    return alert_level_level >= L_INFO

def is_debug():
    """Return True iff the alert level is at least at debugging."""
    return alert_level_level >= L_DEBUG

def is_trace():
    """Return True iff the alert level is at least at tracing."""
    return alert_level_level >= L_TRACE


def alert_if_level(level, *msgs):
    """Print a message if `level` is <= the alert_level_level.

    If a decoration exists in `alert_decoration[]` for that level, is it
    prepended to the message. By default, all levels print to stderr; this can
    be changed in `alert_fd[]` by level.

    If one of the    {XXX TODO what tf did I want to say here?}

    """
    # make all msgs elements strings, calling those that are callable
    msgs = list(msgs)                   # is a tuple before
    for i, elem in enumerate(msgs):
        if callable(elem):
            msgs[i] = elem()
        elif type(elem) is not str:
            msgs[i] = str(elem)
    if alert_decoration[level]:
        msgs = [alert_decoration[level].format(**globals()), *msgs]

    if level <= alert_level_level:
        print(*msgs, file=alert_fd[level])

    if alert_use_syslog:
        if not syslog_opened:
            syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
        level = max(0, min(alert_max_level, level))
        message = " ".join(map(str, msgs))
        syslog.syslog(syslog_prio[level], message)


def debug_vars(*vars):
    """Print debug output for the named variables if alert level >= L_DEBUG."""
    if alert_level_level >= L_DEBUG:
        context = inspect.currentframe().f_back.f_locals
        for var in vars:
            print("VAR {}: {}".format(var, repr(context[var])),
                  file=alert_fd[L_DEBUG])


def err(*msgs):
    """Print error level output."""
    had_errors = True
    alert_if_level(L_ERROR, *msgs)

def fatal(*msgs, exit_status=1):
    """Print error level output."""
    alert_if_level(L_ERROR, "Fatal", *msgs)
    sys.exit(exit_status)

def notice(*msgs):
    """Print notice level output according to alert level."""
    alert_if_level(L_NOTICE, *msgs)

def info(*msgs):
    """Print info level output according to alert level."""
    alert_if_level(L_INFO, *msgs)

def debug(*msgs):
    """Print debug level output according to alert level."""
    alert_if_level(L_DEBUG, *msgs)

def trace(*msgs):
    """Print debug level output according to alert level."""
    alert_if_level(L_TRACE, *msgs)

# EOF
