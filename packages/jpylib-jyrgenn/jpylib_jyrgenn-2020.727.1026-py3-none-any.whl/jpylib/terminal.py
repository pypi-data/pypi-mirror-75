import fcntl
import struct
import termios

def terminal_size():
    """Return `columns, rows`; `None, None` if not supported by device."""
    try:
        packed_args = struct.pack('HHHH', 0, 0, 0, 0)
        packed_result = fcntl.ioctl(0, termios.TIOCGWINSZ, packed_args)
        rows, cols, *_ = struct.unpack('HHHH', packed_result)
        return cols, rows
    except OSError:
        return None, None

