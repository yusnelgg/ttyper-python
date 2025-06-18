import curses
import random
import time

PHRASES = [
    "knowledge is power",
    "clean code clear mind",
    "type fast like lightning",
    "practice makes perfect",
    "stay focused and keep going"
]

DURATION = 30

def calculate_wpm(text, seconds):
    words = text.strip().split()
    num_words = len(words)
    minutes = seconds / 60
    return num_words / minutes if minutes > 0 else 0

def main(stdscr):
    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()
    stdscr.clear()
    stdscr.nodelay(True)

    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)

    used_phrases = set()
    user_input = []
    total_typed_text = ""

    def new_phrase():
        available = [p for p in PHRASES if p not in used_phrases]
        if not available:
            used_phrases.clear()
            available = PHRASES[:]
        phrase = random.choice(available)
        used_phrases.add(phrase)
        return phrase

    phrase = new_phrase()

    stdscr.addstr(0, 0, "🔥 Welcome to ttyper!")
    stdscr.addstr(1, 0, "You can exit anytime by pressing ESC")
    stdscr.addstr(3, 0, "Type the phrase and test your speed and accuracy:")

    start_time = time.time()

    line = 5
    col = 2

    while True:
        elapsed_time = time.time() - start_time
        time_left = DURATION - elapsed_time
        if time_left <= 0:
            break

        stdscr.addstr(2, 0, f"Time left: {int(time_left)} sec  ")
        # stdscr.addstr(5, 0, " " * 80)
        # stdscr.addstr(5, 0, phrase)

        stdscr.move(line, col)
        stdscr.clrtoeol()

        for i, ch in enumerate(phrase):
            if i < len(user_input):
                if user_input[i] == ch:
                    color = curses.color_pair(1)
                else:
                    color = curses.color_pair(2)
            else:
                color = curses.color_pair(3)
            stdscr.addstr(line, col + i, ch, color)

        stdscr.move(line, col + len(user_input))
        stdscr.refresh()

        try:
            key = stdscr.get_wch()
        except curses.error:
            continue

        if key == '\x1b':
            return
        elif key in ('\b', '\x7f', '\x08'):
            if user_input:
                user_input.pop()
        elif isinstance(key, str) and len(key) == 1 and 32 <= ord(key) <= 126:
            if len(user_input) < len(phrase):
                user_input.append(key)

        if len(user_input) == len(phrase) and ''.join(user_input) == phrase:
            total_typed_text += ''.join(user_input) + " "
            user_input = []
            phrase = new_phrase()

    wpm = calculate_wpm(total_typed_text.strip(), DURATION)

    stdscr.nodelay(False)
    stdscr.clear()
    stdscr.addstr(0, 0, "⏰ Time's up!")
    stdscr.addstr(2, 0, f"Your WPM (Words Per Minute) was: {wpm:.2f}")
    stdscr.addstr(4, 0, "Press ESC to exit...")

    while True:
        key = stdscr.getch()
        if key == 27:
            break

curses.wrapper(main)
