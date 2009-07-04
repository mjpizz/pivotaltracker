import os
import sys

_TERMCODES = {
    "bold": 1,
    "hidden": 2,
    "underline": 4,
    "blink": 5,
    "reverse": 7,
    "formatting": 12,

    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,

    "bgred": 41,
    "bggreen": 42,
    "bgyellow": 43,
    "bgblue": 44,
    "bgmagenta": 45,
    "bgcyan": 46,
    "bgwhite": 47,
    }

_CONSOLE_SUPPORTS_COLORS = [None]

def _console_supports_colors():
    """returns True if the current console supports colors (can manually disable by ANSI_COLORS_DISABLED=0)"""
    stream = sys.stdout
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
        
    # allow override with ANSI_COLORS_DISABLED by default
    if os.getenv("ANSI_COLORS_DISABLED") == "1":
        return False

    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except ImportError, e:
        # curses is not available on this machine
        import platform
        if "indows" in platform.platform():
            # this is Windows, that's probably why (no color support)
            # TODO: check out http://code.google.com/p/testoob/source/browse/trunk/src/testoob/reporting/colored.py
            return False
        else:
            # this is not Windows, so it *might* support color
            # look at the environment variables instead
            if os.getenv("ANSI_COLORS_DISABLED") == "1":
                return False
            if os.getenv("CLICOLOR") == "1":
                return True
            if os.getenv("TERM") == "xterm-color":
                return True
            
            # no clue, just guess false
            return False

    except Exception, e:
        # guess false in case of unknown error
        return False

def styled(msg, attrs):
    """returns a string that will be styled by the terminal, if it supports it.
    The 'attrs' argument is a list of string attributes to apply to the message
    (e.g. %s)""" % ", ".join(_TERMCODES.keys())
    if _console_supports_colors():
        # colors supported, wrap it in control codes
        prefixes = ["%02i" % _TERMCODES[attr] for attr in attrs]
        return "\033[0;%sm%s\033[m" % (";".join(prefixes), msg)
    else:
        # no colors supported, return the message
        return msg
