#!/usr/bin/env python
# encoding: utf-8
"""
This is a quick and dirty algorithm test for an interesting problem.

Problem:

    Fill all the seats in a theater with groups of people, where everyone in
    the same group should sit close to other members of the group. Every
    available seat may be in use.

Algorithm:

    Each group 'eats' into the grid starting at an initial position. If the
    current seat is available occupy it. Then moves one step in the current
    direction until an expanding bounding box is reached
    (`limit_[top|right|bottom|left]`). If the limit is reached, turn clockwise
    or counter-clockwise, and expand the just hit limit by one for the next
    round.

Author:

    Chris Hager <chris@metachris.org>

Date:

    November 2011

License:

    Use this code in whichever way you want (no restrictions).
"""

import sys
import os
import math

# Grid size (seats) [adjust as wanted]
ROWS = 10
COLUMNS = 15

# Do not change the settings below
DIR_RIGHT = 1
DIR_BOTTOM = 2
DIR_LEFT = 3
DIR_TOP = 4
ROT_CLOCKWISE = 1
ROT_COUNTERCLOCKWISE = 2


class Pos(object):
    """Representation of a x/y position"""
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "<Pos(%s, %s)>" % (self.x, self.y)


class Grid(object):
    """Representation of the grid (theater seats)"""
    grid = []
    rows = 0
    cols = 0

    EMPTY = "-"

    def __init__(self, rows, cols):
        """Init Grid with - (empty seats)"""
        self.rows = rows
        self.cols = cols
        for _ in xrange(rows):
            self.grid.append(self.EMPTY * cols)

    def show(self):
        """Print the grid"""
        out = "     "
        for i in xrange(self.cols):
            out += "%2s " % i
        out += "\n\n"

        cnt = 0
        for line in self.grid:
            out += "%2s   " % cnt
            cnt += 1
            for seat in line:
                out += " %s " % seat
            out += "\n"
        print out

    def is_free(self, pos):
        """Returns true if position in grid is free"""
        return self.grid[pos.y][pos.x] == self.EMPTY

    def set_used(self, pos, id):
        """Mark a seat as used"""
        self.grid[pos.y] = self.grid[pos.y][:pos.x] + id + \
                self.grid[pos.y][pos.x + 1:]

    def count_free(self):
        """Returns the count of free positions"""
        cnt = 0
        for row in self.grid:
            cnt += row.count(self.EMPTY)
        return cnt


class Group(object):
    """Representation of one group"""
    id = None
    count = 0
    seats = []

    # Current position and direction
    cur_pos = None
    cur_dir = None
    rotation = None

    # If reaching one of the limits, turn clockwise and expand limit
    limit_left = None
    limit_top = None
    limit_right = None
    limit_bottom = None

    def __init__(self, id, count, start_pos, start_dir,
            rotation=ROT_CLOCKWISE):
        self.seats = []
        self.id = id
        self.count = count
        self.cur_pos = start_pos
        self.cur_dir = start_dir
        self.rotation = rotation

    def __str__(self):
        return "<Group-%s(%s)>" % (self.id, self.count)

    def eatIn(self, grid):
        """Eat into grid"""
        self.grid = grid

        # Error out if there are not enough seats
        count_free = self.grid.count_free()
        if self.count > count_free:
            raise IndexError("Not enough available positions in the grid " + \
                    "(%s available, %s required)" % (count_free, self.count))

        # Set initial limits (1 in each direction)
        self.limit_left = self.cur_pos.x - 1 if self.cur_pos.x - 1 >= 0 else 0
        self.limit_right = self.cur_pos.x + 1 if self.cur_pos.x + 1 < \
                grid.cols else grid.cols - 1
        self.limit_top = self.cur_pos.y - 1 if self.cur_pos.y - 1 >= 0 else 0
        self.limit_bottom = self.cur_pos.y + 1 if self.cur_pos.y + 1 < \
                grid.rows else grid.rows - 1

        # Occupy seats until we have enough
        while (len(self.seats) < self.count):
            if self.grid.is_free(self.cur_pos):
                self.grid.set_used(self.cur_pos, self.id)
                self.seats.append(self.cur_pos)

            # Update the current position, and change direction if necessary
            self.updatePos()

    def updatePos(self):
        """
        Update current position based on the current direction and the limits.
        If outside of limit, update direction and expand the limit.
        """
        if self.cur_dir == DIR_RIGHT:
            x = self.cur_pos.x + 1
            if x > self.limit_right:
                # cannot move to the right. turn now and expand.
                self.updateDir()
            else:
                self.cur_pos.x = x

        elif self.cur_dir == DIR_BOTTOM:
            y = self.cur_pos.y + 1
            if y > self.limit_bottom:
                # cannot move. turn now and expand.
                self.updateDir()
            else:
                self.cur_pos.y = y

        elif self.cur_dir == DIR_LEFT:
            x = self.cur_pos.x - 1
            if x < self.limit_left:
                # cannot move to the right. turn now and expand.
                self.updateDir()
            else:
                self.cur_pos.x = x

        elif self.cur_dir == DIR_TOP:
            y = self.cur_pos.y - 1
            if y < self.limit_top:
                # cannot move to the right. turn now and expand.
                self.updateDir()
            else:
                self.cur_pos.y = y

    def updateDir(self):
        """Updates self.cur_dir with a 90 degree turn"""
        if self.rotation == ROT_CLOCKWISE:
            self.updateDirClockwise()
        else:
            self.updateDirCounterClockwise()

    def updateDirClockwise(self):
        """Turn clockwise and expand limit"""
        if self.cur_dir == DIR_RIGHT:
            self.cur_dir = DIR_BOTTOM
            if self.limit_right + 1 < self.grid.cols:
                self.limit_right += 1

        elif self.cur_dir == DIR_BOTTOM:
            self.cur_dir = DIR_LEFT
            if self.limit_bottom + 1 < self.grid.rows:
                self.limit_bottom += 1

        elif self.cur_dir == DIR_LEFT:
            self.cur_dir = DIR_TOP
            if self.limit_left - 1 > 0:
                self.limit_left -= 1

        elif self.cur_dir == DIR_TOP:
            self.cur_dir = DIR_RIGHT
            if self.limit_top - 1 >= 0:
                self.limit_top -= 1

    def updateDirCounterClockwise(self):
        """Turn counter clockwise and expand limit"""
        if self.cur_dir == DIR_RIGHT:
            self.cur_dir = DIR_TOP
            if self.limit_right + 1 < self.grid.cols:
                self.limit_right += 1

        elif self.cur_dir == DIR_TOP:
            self.cur_dir = DIR_LEFT
            if self.limit_top - 1 >= 0:
                self.limit_top -= 1

        elif self.cur_dir == DIR_LEFT:
            self.cur_dir = DIR_BOTTOM
            if self.limit_left - 1 > 0:
                self.limit_left -= 1

        elif self.cur_dir == DIR_BOTTOM:
            self.cur_dir = DIR_RIGHT
            if self.limit_bottom + 1 < self.grid.rows:
                self.limit_bottom += 1


def get_groups():
    # Helpers for initial positioning the groups
    center = COLUMNS / 2
    left = 0
    top = 0
    right = COLUMNS - 1
    bottom = ROWS - 1

    # List of groups (id, seats, start-position, start-direction[, rotation]))
    return [
        Group("#", 30, Pos(center, bottom), DIR_LEFT),
        Group("*", 28, Pos(left, bottom),   DIR_TOP,  ROT_COUNTERCLOCKWISE),
        Group("/", 26, Pos(right, bottom),  DIR_LEFT, ROT_COUNTERCLOCKWISE),
        Group("o", 30, Pos(left, top),      DIR_RIGHT),
        Group("x", 36, Pos(right, top),     DIR_LEFT, ROT_COUNTERCLOCKWISE),
    ]


def main():
    # Instantiate the grid
    grid = Grid(ROWS, COLUMNS)

    # Let groups eat into the grid, one by one
    for group in get_groups():
        group.eatIn(grid)

    # Pretty print the final grid
    grid.show()


if __name__ == '__main__':
    main()
