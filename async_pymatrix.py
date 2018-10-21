#!/usr/bin/env python3

import curses
import asyncio
import random


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

    async def matrix(self, y):
        attr = curses.color_pair(2)
        length = random.randint(1, 15)

        def gen_bin(length):
            binary = []
            for i in range(length):
                binary.append(random.choice(
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ&%$#@!~1234567890"))

            while True:
                yield from binary

        message = gen_bin(length)
        position = []

        await asyncio.sleep(random.randint(0, 5000) * 0.001)

        while True:
            if len(position) == 0:
                position = [self.top + 1]
                self.stdscr.addstr(position[0], y, next(message), attr)
                length = random.randint(1, 15)

            if position[0] < self.bottom - 1:
                position.insert(0, position[0] + 1)
                self.stdscr.addstr(position[0], y, next(message), attr)

            if (len(position) > length or position[0] == self.bottom - 1) and len(position) > 0:
                self.stdscr.addstr(position.pop(), y, " ")

            self.stdscr.refresh()

            await asyncio.sleep(0.05)

    async def supervisor(self):

        tasks = []
        for i in range(self.left + 1, self.right - 1):
            tasks.append(asyncio.ensure_future(self.matrix(i)))

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            for task in tasks:
                task.cancel()


def main(stdscr):
    te = playground(stdscr)

    loop = asyncio.get_event_loop()

    supervisor = asyncio.ensure_future(te.supervisor())

    try:
        loop.run_until_complete(supervisor)
    except KeyboardInterrupt:
        supervisor.cancel()


if __name__ == "__main__":
    curses.wrapper(main)
