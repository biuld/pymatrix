#!/usr/bin/env python3

import curses
import asyncio
import random
import sys


class playground(object):

    def __init__(self, stdscr):
        self.stdscr = stdscr
        maxLine, maxColumn = stdscr.getmaxyx()

        self.top = 0
        self.left = 0
        self.right = maxColumn - 1
        self.bottom = maxLine - 1

        curses.use_default_colors()
        curses.curs_set(False)

        random.seed()

    def display_msg(self, msg):
        self.stdscr.addstr(0, 0, str(msg))
        self.stdscr.refresh()

    async def matrix(self, target):
        attr = curses.COLOR_GREEN

        def gen_bin(length):
            binary = []
            for i in range(length):
                binary.append(random.choice(
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ&%$#@!~1234567890"))

            while True:
                yield from binary

        position = []

        while True:

            if len(position) == 0:
                position = [self.top]
                length = random.randint(1, 15)
                message = gen_bin(length)
                self.stdscr.addstr(position[0], target, next(message), attr)

            if position[0] < self.bottom:
                position.insert(0, position[0] + 1)
                self.stdscr.addstr(position[0], target, next(message), attr)

            if (len(position) > length or position[0] == self.bottom) and len(position) > 0:
                self.stdscr.addstr(position.pop(), target, " ")

            self.stdscr.refresh()
            await asyncio.sleep(0.05)

    async def supervisor(self):

        tasks = []

        th = self.right - self.left

        self.display_msg("current coroutines: %d" % th)

        for i in range(self.left, self.right):
            tasks.append(asyncio.ensure_future(self.matrix(i)))

        try:
            await asyncio.gather(*tasks)
        except:
            for i in tasks:
                i.cancel()


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
