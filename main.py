import curses

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    stdscr.addstr(0, 0, "¡Hola ttyper!")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)