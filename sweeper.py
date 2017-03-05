#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import os

from game import Game

class Sweeper:

    border_elements = []

    def __init__(self, game, x, y):
        self.game = game
        self._x = x
        self._y = y

    def i_am_alone(self, x, y):
        for (i, j) in self.look_around(x, y):
            if self.game.what(i, j) not in [' ', None]:
                return False
        return True

    def look_around(self, x, y):
        surround = []
        for i in [x-1, x, x+1]:
            for j in [y-1, y, y+1]:
                if not (i == x and j == y):
                    surround.append((i, j))
        return surround

    def random_click(self):
        x = random.randint(0, self._x)
        y = random.randint(0, self._y)
        if self.game.what(x, y) != ' ':
            return self.random_click()
        else:
            self.game.click(x, y)
            return (x, y)

    def sweep(self):
        (x, y) = self.random_click()
        if self.i_am_alone(x, y):
            # print('resweep')
            return self.sweep()

        loop = True
        while loop:
            self.find_border(x, y)
            border_list = self.get_border()
            self.mark_mines(border_list)
            loop = self.click_spaces(border_list)
            self.game.output()

        if not self.finish():
            # print('not finish resweep')
            return self.sweep()
        else:
            self.game.verify()

    checked_element = {}
    border_list = []

    def is_border(self, x, y):
        space = 0

        self.checked_element.setdefault(x, {})
        self.checked_element[x][y] = 1

        if self.game.what(x, y) in [' ', None]:
            return False

        for (i, j) in self.look_around(x, y):
            if self.game.what(i, j) == ' ':
                space += 1
        if space > 0:
            return True
        return False

    def find_border(self, x, y):
        loop = [(x, y)]
        while loop:
            new_loop = []
            for (i, j) in loop:
                l = self._do_find_border(i, j)
                if l:
                    new_loop += l
            loop = set(new_loop)

    def _do_find_border(self, x, y):
        if self.game.what(x, y) in [' ', None]:
            return
        if self.checked_element.get(x, {}).get(y, None):
            return

        if self.is_border(x, y):
            self.border_list.append((x, y))

        return self.look_around(x, y)

    def get_border(self):
        tmp = self.border_list
        self.border_list = []
        self.checked_element = {}
        return tmp

    def mark_mines(self, border_list):
        need_mark_list = []
        for (i, j) in border_list:
            surround = self.look_around(i, j)
            mines = []
            spaces = []
            for (a, b) in surround:
                if self.game.what(a, b) == ' ':
                    spaces.append((a, b))
                if self.game.what(a, b) == '#':
                    mines.append((a, b))
            num = self.game.what(i, j)
            if num == '#':
                num = -1
            if num - len(mines) == len(spaces):
                for (a, b) in spaces:
                    need_mark_list.append((a, b))
        for (a, b) in need_mark_list:
            self.game.flag(a, b)

    def click_spaces(self, border_list):
        need_click_list = []
        for (i, j) in border_list:
            surround = self.look_around(i, j)
            mines = []
            spaces = []
            for (a, b) in surround:
                if self.game.what(a, b) == ' ':
                    spaces.append((a, b))
                if self.game.what(a, b) == '#':
                    mines.append((a, b))
            if self.game.what(i, j) == len(mines):
                for (a, b) in spaces:
                    need_click_list.append((a, b))
        for (a, b) in need_click_list:
            self.game.click(a, b)
        return need_click_list != []

    def finish(self):
        for x in range(self._x):
            for y in range(self._y):
                if self.game.what(x, y) == ' ':
                    return False
        return True


if __name__ == '__main__':

    import sys

    x = 30
    y = 16
    n = 99

    if len(sys.argv) == 4:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        n = int(sys.argv[3])

    g = Game(x, y, n)
    s = Sweeper(g, x, y)
    s.sweep()