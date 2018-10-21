#!/usr/bin/env python3

import threading
import random
import time
import os
import curses

lock = threading.RLock()
cond = threading.Condition()
event = threading.Event()


class playground(object):

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

        #threading.Thread(target=self.__monitor, daemon=True).start()

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

    def __monitor(self):

        # self.stdscr.move(0,0)

        while True:
            self.stdscr.nodelay(True)

            with lock:
                ch = self.stdscr.getch()

            if ch == ord('q'):
                event.set()
                curses.endwin()
                os.system("clear")
                break

    def matrix(self):

        attr = curses.color_pair(2)
        length = random.randint(1, 15)
        position = []
        name = threading.current_thread().name

        def gen_bin(length):
            binary = []
            for i in range(length):
                binary.append(random.choice(
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ&%$#@!~1234567890"))

            while True:
                yield from binary

        message = gen_bin(length)

        time.sleep(random.randint(0, 5000) * 0.001)

        while not event.is_set():
            with lock:
                if len(position) == 0:
                    position = [self.top + 1]
                    self.stdscr.addstr(position[0], int(
                        name), next(message), attr)
                    length = random.randint(1, 15)

                if position[0] < self.bottom - 1:
                    position.insert(0, position[0] + 1)
                    self.stdscr.addstr(position[0], int(
                        name), next(message), attr)

                if (len(position) > length or position[0] == self.bottom - 1) and len(position) > 0:
                    self.stdscr.addstr(position.pop(), int(name), " ")

                self.stdscr.refresh()

            time.sleep(0.05)


def main(stdscr):
    te = playground(stdscr)

    for i in range(te.left + 1, te.right - 1):
        temp = threading.Thread(target=te.matrix, name=i)
        temp.start()


if __name__ == "__main__":
    curses.wrapper(main)
