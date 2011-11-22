This is a quick and dirty algorithm test for an interesting problem.

## Problem

Fill all the seats in a theater with groups of people, where everyone in the same group should sit close to other members of the group. Every available seat may be in use.

## Algorithm

Each group 'eats' into the grid starting at an initial position. If the current seat is available occupy it. Then moves one step in the current direction until an expanding bounding box is reached (`limit_[top|right|bottom|left]`). If the limit is reached, turn clockwise or counter-clockwise, and expand the just hit limit by one for the next round.

## Various

* Author: Chris Hager (chris@metachris.org)
* License: Do whatever you want with it.

## Demo

#### Input

	grid = Grid(rows=10, cols=15)
	...
    groups = [
        # Group(id, seats, start-position, start-direction[, rotation]))
        Group("#", 24, Pos(center, bottom), DIR_LEFT),
        Group("*", 28, Pos(left, bottom),   DIR_TOP,  ROT_COUNTERCLOCKWISE),
        Group("/", 25, Pos(right, bottom),  DIR_LEFT),
        Group("o", 36, Pos(left, top),      DIR_RIGHT),
        Group("x", 37, Pos(right, top),     DIR_LEFT, ROT_COUNTERCLOCKWISE),
    ]

#### Output

	      0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 

	 0    o  o  o  o  o  o  o  o  x  x  x  x  x  x  x 
	 1    o  o  o  o  o  o  o  o  x  x  x  x  x  x  x 
	 2    o  o  o  o  o  o  o  o  x  x  x  x  x  x  x 
	 3    o  o  o  o  o  o  o  o  x  x  x  x  x  x  x 
	 4    *  *  *  *  *  *  o  o  x  x  x  x  x  x  x 
	 5    *  *  *  *  *  *  o  o  x  x  /  /  /  /  / 
	 6    *  *  *  *  #  #  #  #  #  #  /  /  /  /  / 
	 7    *  *  *  *  #  #  #  #  #  #  /  /  /  /  / 
	 8    *  *  *  *  #  #  #  #  #  #  /  /  /  /  / 
	 9    *  *  *  *  #  #  #  #  #  #  /  /  /  /  / 

