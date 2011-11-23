This is a quick and dirty algorithm test for an interesting problem.

## Problem

Fill all the seats in a theater with groups of people, where everyone in the same group should sit close to other members of the group. Every available seat may be in use.

## Algorithm

Each group 'eats' into the grid starting at an initial position. If the current seat is available occupy it. Then moves one step in the current direction until an expanding bounding box is reached (`limit_[top|right|bottom|left]`). If the limit is reached, turn clockwise or counter-clockwise, and expand the just hit limit by one for the next round.

## Various

* Author: Chris Hager (chris@metachris.org)
* License: Do whatever you want with it.

## Example 1

#### Input

	grid = Grid(rows=10, cols=15)
	...
    groups = [
	    Group(u"#", 24),
	    Group(u"*", 28),
	    Group(u"/", 25),
	    Group(u"o", 36),
	    Group(u"x", 37),
    ]

#### Output

	      0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 

	 0    x  x  x  x  x  x  x  x  o  o  o  o  o  o  o 
	 1    x  x  x  x  x  x  x  x  o  o  o  o  o  o  o 
	 2    x  x  x  x  x  x  x  x  o  o  o  o  o  o  o 
	 3    x  x  x  x  x  x  x  x  o  o  o  o  o  o  o 
	 4    x  x  x  x  x  *  *  *  o  o  o  o  o  o  o 
	 5    /  /  /  /  /  *  *  *  *  *  #  #  #  #  o 
	 6    /  /  /  /  /  *  *  *  *  *  #  #  #  #  # 
	 7    /  /  /  /  /  *  *  *  *  *  #  #  #  #  # 
	 8    /  /  /  /  /  *  *  *  *  *  #  #  #  #  # 
	 9    /  /  /  /  /  *  *  *  *  *  #  #  #  #  # 


## Example 2

#### Input

	grid = Grid(rows=10, cols=18)

#### Output

          0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 

     0                                     x  x  x  x  x  x  x 
     1                                     x  x  x  x  x  x  x 
     2    o  o  o  o  o                    x  x  x  x  x  x  x 
     3    o  o  o  o  o  o  o  o        x  x  x  x  x  x  x  x 
     4    o  o  o  o  o  o  o  o  *  *  *  x  x  x  x  x  x  x 
     5    o  o  o  /  /  /  /  /  *  *  *  *  *  #  #  #  #  x 
     6    o  o  o  /  /  /  /  /  *  *  *  *  *  #  #  #  #  # 
     7    o  o  o  /  /  /  /  /  *  *  *  *  *  #  #  #  #  # 
     8    o  o  o  /  /  /  /  /  *  *  *  *  *  #  #  #  #  # 
     9    o  o  o  /  /  /  /  /  *  *  *  *  *  #  #  #  #  # 

