#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os
import time

class Game:

    def __init__(self, x, y, n):
        if x * y <= n:
            exit('too many mines!')

        self._y = y
        self._x = x
        self._n = n
        self._board = {}
        self._board_list = []

        self._mine_list = []
        self._mine_map = {}

        self._flag_map = {}

        self._is_first_click = True
        self._first_click = (-1, -1)

        for x in range(self._x):
            self._board[x] = {}
            self._mine_map[x] = {}
            self._flag_map[x] = {}
            for y in range(self._y):
                self._board[x][y] = ' '
                self._mine_map[x][y] = 0
                self._board_list.append((x, y))
                self._flag_map[x][y] = 0

    def plant_mines(self):
        for x in range(self._x):
            for y in range(self._y):
                coord = (x, y)
                if coord != self._first_click:
                    self._mine_list.append((x,y))
        random.shuffle(self._mine_list)
        self._mine_list = self._mine_list[:self._n]
        for mine in self._mine_list:
            self._mine_map[mine[0]][mine[1]] = 1
            # self._mine_map[2][3] = 1
        # self._mine_list = [(2, 3)]

    def what(self, x, y):
        return self._board.get(x, {}).get(y, None)

    def click(self, x, y):
        if self._is_first_click:
            self._first_click = (x, y)
            self.plant_mines()
            self._is_first_click = False

        loop = [(x, y)]
        while loop:
            new_loop = []
            for (x, y) in loop:
                l = self._do_click(x, y)
                if l:
                    new_loop += l
            loop = set(new_loop)

    _already_clicked = {}

    def _do_click(self, x, y):
        if self.what(x, y) == None:
            return
        if self._already_clicked.get(x, {}).get(y, None):
            return

        if not self._mine_map[x][y]:
            val = self._check_around(x, y)
            self._board[x][y] = val

            self._already_clicked.setdefault(x, {})
            self._already_clicked[x][y] = 1

            if val == 0:
                return self._look_around(x, y)
        else:
            self._board[x][y] = '@'
            self._boom()

    def _look_around(self, x, y):
        surround = []
        for i in [x-1, x, x+1]:
            for j in [y-1, y, y+1]:
                if not (i == x and j == y):
                    surround.append((i, j))
        return surround

    def _clicked(self, x, y):
        return self.what(x, y) != ' '

    def flag(self, x, y):
        if not self._clicked(x, y):
            self._flag_map[x][y] = 1
            self._board[x][y] = '#'

    def flagged(self, x, y):
        return self._flag_map[x][y] == 1

    def unflag(self, x, y):
        if self.flagged(x, y):
            self._flag_map[x][y] = 0
            self._board[x][y] = ' '

    def _check_around(self, x, y):
        val = 0
        for i in [x-1, x, x+1]:
            for j in [y-1, y, y+1]:
                val += self._mine_map.get(i, {}).get(j, 0)
        return val

    def _boom(self):
        for m in self._mine_list:
            x = m[0]
            y = m[1]
            if self.flagged(x, y):
                self._flag_map[x][y] = 0
                self._board[x][y] = '#'
            else:
                if self._board[x][y] != '@':
                    self._board[x][y] = '*'
            for i in range(self._x):
                for j in range(self._y):
                    if self._flag_map[i][j]:
                        self._board[i][j] = 'X'
        self.output()
        exit('oops!')

    def verify(self):
        if self._flag_map == self._mine_map:
            self.output()
            print('yeah! you win!')
        else:
            self._boom()

    def _expand(self, x, y):
        self._check_around(x, y)

    def output(self):
        time.sleep(0.1)
        os.system('clear')
        for y in range(self._y):
            for x in range(self._x):
                if self._board[x][y] == 0:
                    print(self._board[x][y], end=' ')
                    # print('.', end=' ')
                else:
                    print(self._board[x][y], end=' ')
            print()
        # print()
        # for y in range(self._y):
        #     for x in range(self._x):
        #         print(self._mine_map[x][y], end=' ')
        #     print()
        # print()
        # for y in range(self._y):
        #     for x in range(self._x):
        #         print(self._flag_map[x][y], end=' ')
        #     print()


if __name__ == '__main__':

    g = Game(10, 10, 10)
    for i in range(10):
        g.click(2, i)
    g.flag(4, 8)
    g.verify()