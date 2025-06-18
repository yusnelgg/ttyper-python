import curses
import json
import random
import time

def load_phrases(path):
    with open(path, 'r') as f:
        return json.load(f)

def wrap_text(text, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > max_width:
            lines.append(current)
            current = word
        else:
            if current:
                current += " " + word
            else:
                current = word
    if current:
        lines.append(current)
    return lines

def calculate_wpm(text, seconds):
    words = text.strip().split()
    num_words = len(words)
    minutes = seconds / 60
    return num_words / minutes if minutes > 0 else 0

PHRASES = load_phrases('phrases/data.json')
DURATION = 30

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
    total_typed_text = []

    def new_phrase():
        available = [p for p in PHRASES if p not in used_phrases]
        if not available:
            used_phrases.clear()
            available = PHRASES[:]
        phrase = random.choice(available)
        used_phrases.add(phrase)
        return phrase

    def get_locked_index(phrase, typed):
        words = phrase.split(' ')
        index = 0
        locked = 0
        for word in words:
            if len(typed) >= index + len(word) and ''.join(typed[index:index+len(word)]) == word:
                locked = index + len(word)
                if locked < len(phrase) and phrase[locked] == ' ':
                    locked += 1
                index = locked
            else:
                break
        return locked

    phrase = new_phrase()
    start_time = time.time()
    line = 8
    col = 5

    stdscr.addstr(2, 1, "🔥 Welcome to ttyper!")
    stdscr.addstr(3, 1, "You can exit anytime by pressing ESC")

    while True:
        elapsed_time = time.time() - start_time
        time_left = DURATION - elapsed_time
        if time_left <= 0:
            break

        max_y, max_x = stdscr.getmaxyx()
        wrapped = wrap_text(phrase, max_x - col - 2)
        stdscr.addstr(4, 1, f"Time left: {int(time_left)} sec  ")

        for i, line_text in enumerate(wrapped):
            stdscr.move(line + i, col)
            stdscr.clrtoeol()
            for j, ch in enumerate(line_text):
                idx = sum(len(w) + 1 for w in phrase.split()[:sum(len(l.split()) for l in wrapped[:i])]) + j
                if idx < len(user_input):
                    if user_input[idx] == ch:
                        color = curses.color_pair(1)
                    else:
                        color = curses.color_pair(2)
                else:
                    color = curses.color_pair(3)
                stdscr.addstr(line + i, col + j, ch, color)

        total_lines = len(wrapped)
        idx = len(user_input)
        logical_line = 0
        logical_col = 0
        count = 0
        for i, line_text in enumerate(wrapped):
            if count + len(line_text) >= idx:
                logical_line = i
                logical_col = idx - count
                break
            count += len(line_text)
        stdscr.move(line + logical_line, col + logical_col)
        stdscr.refresh()

        try:
            key = stdscr.get_wch()
        except curses.error:
            continue

        if key == '\x1b':
            return
        elif key in ('\b', '\x7f', '\x08'):
            locked = get_locked_index(phrase, user_input)
            if len(user_input) > locked:
                user_input.pop()
        elif isinstance(key, str) and len(key) == 1 and 32 <= ord(key) <= 126:
            if len(user_input) < len(phrase):
                user_input.append(key)

        if len(user_input) == len(phrase):
            total_typed_text.append(''.join(user_input))
            user_input = []
            phrase = new_phrase()

    final_text = ' '.join(total_typed_text)
    wpm = calculate_wpm(final_text.strip(), DURATION)

    stdscr.nodelay(False)
    stdscr.clear()
    stdscr.addstr(2, col, "⏰ Time's up!")
    stdscr.addstr(4, col, f"Your WPM (Words Per Minute) was: {wpm:.2f}")
    stdscr.addstr(6, col, "Press ESC to exit...")

    while True:
        key = stdscr.getch()
        if key == 27:
            break

curses.wrapper(main)
