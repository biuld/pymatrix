#!/usr/bin/env python3

import threading
import random
import time
import curses

lock = threading.RLock()
cond = threading.Condition()
event = threading.Event()


class playground(object):
    MESSAGE = "*"

    def __init__(self, stdscr):
        self.stdscr = stdscr
        maxLine = curses.LINES
        maxColumn = curses.COLS

        random.seed()

        self.top = int(maxLine * 0.1)
        self.bottom = int(maxLine * 0.8)
        self.left = int(maxColumn * 0.1)
        self.right = int(maxColumn * 0.9)

        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.curs_set(False)

        self.__drawboder(stdscr, self.top, self.bottom, self.left, self.right)

    def __drawboder(self, stdscr, top, bottom, left, right):
        stdscr.addstr(top, left, "+")
        stdscr.addstr(bottom, left, "+")
        stdscr.addstr(top, right, "+")
        stdscr.addstr(bottom, right, "+")

        for i in range(top + 1, bottom):
            stdscr.addstr(i, left, "|")
            stdscr.addstr(i, right, "|")

        for i in range(left + 1, right):
            stdscr.addstr(top, i, "-")
            stdscr.addstr(bottom, i, "-")

        stdscr.refresh()

    def matrix(self):

        while True:

            length = random.randint(3, 15)
            binary = []
            name = threading.current_thread().name

            time.sleep(random.randint(0, 5000) * 0.001)

            for i in range(length):
                binary.append(random.choice('01'))

            position = [i for i in range(self.top + 1, self.top + length)]

            while True:

                with lock:
                    for y, i in zip(position, binary):
                        self.stdscr.addstr(
                            y, int(name), i, curses.color_pair(2))
                        self.stdscr.refresh()

                self.stdscr.addstr(position[0], int(name), " ")

                del position[0]

                try:
                    head = position[-1] + 1
                except IndexError:
                    break

                if head < self.bottom:
                    position.append(head)

                time.sleep(0.09)

        self.stdscr.getch()


def main(stdscr):
    te = playground(stdscr)

    for i in range(te.left + 1, te.right):
        temp = threading.Thread(target=te.matrix, name=i)
        temp.start()


if __name__ == "__main__":
    curses.wrapper(main)
