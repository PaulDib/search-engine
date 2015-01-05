class _Getch:

    """
    Gets a single character from standard input.  Does not echo to the screen.
    """

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:

    """
    Gets a single character from UNIX standard input.  Does not echo to the screen.
    """

    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        file_descriptor = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_descriptor)
        try:
            tty.setraw(sys.stdin.fileno())
            character = sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
        return character


class _GetchWindows:

    """
    Gets a single character from Windows standard input.  Does not echo to the screen.
    """

    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        character = msvcrt.getch()
        # escaped character (special key or arrow key)
        if character == b'\xe0':
            return '\x1b'
        elif character == b'\x08':  # backspace key
            return chr(127)
        return character.decode('latin-1')


getch = _Getch()
