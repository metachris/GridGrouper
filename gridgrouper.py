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

# Do not change the settings below
DIR_RIGHT = 0
DIR_BOTTOM = 1
DIR_LEFT = 2
DIR_TOP = 3
ROT_CLOCKWISE = 0
ROT_COUNTERCLOCKWISE = 1


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

    EMPTY = u" "

    def __init__(self, rows, cols):
        """Init Grid with - (empty seats)"""
        self.rows = rows
        self.cols = cols
        for _ in xrange(rows):
            self.grid.append(self.EMPTY * cols)

    def is_free(self, pos):
        """Returns true if position in grid is free"""
        return self.grid[pos.y][pos.x] == self.EMPTY

    def set_used(self, pos, id):
        """Mark a seat as used"""
        self.grid[pos.y] = unicode(self.grid[pos.y][:pos.x] + id + \
                self.grid[pos.y][pos.x + 1:])

    def count_free(self):
        """Returns the count of free positions"""
        cnt = 0
        for row in self.grid:
            cnt += row.count(self.EMPTY)
        return cnt

    def show(self):
        """Pretty print the grid"""
        # Add the header line with column index
        out = "     "
        for i in xrange(self.cols):
            out += "%2s " % i
        out += "\n\n"

        # Add the content lines, preceded by the line number
        cnt = 0
        for line in self.grid:
            out += "%2s   " % cnt
            cnt += 1
            for seat in line:
                out += " %s " % seat
            out += "\n"

        # Print the pretty grid representation
        print out


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

    def __init__(self, id, count, start_pos=None, start_dir=DIR_LEFT,
            rotation=ROT_CLOCKWISE):
        self.seats = []
        self.count = count
        self.cur_pos = start_pos
        self.cur_dir = start_dir
        self.rotation = rotation

        # Only accept a valid id (single-digit)
        if id is None or len(unicode(id)) != 1:
            raise TypeError("Group id needs to be one digit, not '%s'" % id)
        self.id = unicode(id)

    def __str__(self):
        return "<Group-%s(%s)>" % (self.id, self.count)

    def find_initial_pos(self):
        """
        Find an initial position in the grid, start at the bottom right and
        move left and up if too far left.
        """
        # Tweak the number of minimum required free columns on the left
        MIN_LEFT = 2

        # Set initial position (almost) bottom right
        pos = Pos(self.grid.cols - 2, self.grid.rows - 2)

        # Search until found or out of space
        found = False
        while not found:
            if self.grid.is_free(pos):
                return pos
            pos.x -= 1
            if pos.x < MIN_LEFT:
                pos.x = self.grid.cols - 1
                pos.y -= 1
                if pos.y < 0:
                    raise IndexError("Could not find an initial position")

    def occupy(self, grid):
        """Occupy this groups part in the grid"""
        self.grid = grid

        # Error out if there are not enough seats
        count_free = self.grid.count_free()
        if self.count > count_free:
            raise IndexError("Not enough available positions in the grid " + \
                    "(%s available, %s required)" % (count_free, self.count))

        if not self.cur_pos:
            self.cur_pos = self.find_initial_pos()

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
            self.move()

    def move(self):
        """
        Move in current direction by 1. If outside of limit, update direction
        and expand the limit.
        """
        if self.cur_dir == DIR_RIGHT:
            if self.cur_pos.x + 1 > self.limit_right:
                self.turn()
            else:
                self.cur_pos.x = self.cur_pos.x + 1

        elif self.cur_dir == DIR_BOTTOM:
            if self.cur_pos.y + 1 > self.limit_bottom:
                self.turn()
            else:
                self.cur_pos.y = self.cur_pos.y + 1

        elif self.cur_dir == DIR_LEFT:
            if self.cur_pos.x - 1 < self.limit_left:
                self.turn()
            else:
                self.cur_pos.x = self.cur_pos.x - 1

        elif self.cur_dir == DIR_TOP:
            if self.cur_pos.y - 1 < self.limit_top:
                self.turn()
            else:
                self.cur_pos.y = self.cur_pos.y - 1

    def turn(self):
        """
        Expands the limit in the current direction by one and updates
        self.cur_dir with a 90 degree turn either cw or ccw.
        """
        self.expand_limit()
        if self.rotation == ROT_CLOCKWISE:
            # Turn clockwise
            self.cur_dir = (self.cur_dir + 1) % 4
        else:
            # Turn counter-clockwise
            self.cur_dir = (self.cur_dir - 1) % 4

    def expand_limit(self):
        """Expands the limit in the current direction by 1, if enough space"""
        if self.cur_dir == DIR_RIGHT:
            if self.limit_right + 1 < self.grid.cols:
                self.limit_right += 1

        elif self.cur_dir == DIR_BOTTOM:
            if self.limit_bottom + 1 < self.grid.rows:
                self.limit_bottom += 1

        elif self.cur_dir == DIR_LEFT:
            if self.limit_left - 1 >= 0:
                self.limit_left -= 1

        elif self.cur_dir == DIR_TOP:
            if self.limit_top - 1 >= 0:
                self.limit_top -= 1


def main():
    # Instantiate the grid (adjust size as wanted)
    grid = Grid(rows=10, cols=19)

    # Let groups eat into the grid, one by one
    for group in get_groups(grid.rows, grid.cols):
        group.occupy(grid)

    # Pretty print the final grid
    grid.show()


def get_groups(rows, cols):
    """Return the initial list of Groups"""
    # 5 groups without start-parameters (will auto-position)
    return [
        Group(u"♥", 24),
        Group(u"☼", 28),
        Group(u"✌", 25),
        Group(u"☺", 36),
        Group(u"♪", 37),
    ]

    # You can manually set the initial position and other params like this:
    # center = cols / 2
    # left = 0
    # top = 0
    # right = cols - 1
    # bottom = rows - 1
    # return [
    #     Group(u"♥", 24, Pos(center, bottom), DIR_LEFT),
    #     Group(u"☼", 28, Pos(left, bottom),   DIR_TOP,  ROT_COUNTERCLOCKWISE),
    #     Group(u"☺", 25, Pos(right, bottom),  DIR_LEFT),
    #     Group(u"✌", 36, Pos(left, top),      DIR_RIGHT),
    #     Group(u"♪", 37, Pos(right, top),     DIR_LEFT, ROT_COUNTERCLOCKWISE),
    # ]


if __name__ == '__main__':
    main()
