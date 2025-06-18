import curses
import time

def main(stdscr):
    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()
    stdscr.clear()
    stdscr.nodelay(True)

    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)

    stdscr.addstr(0, 0, "🔥 Bienvenido a ttyper!")


curses.wrapper(main)
