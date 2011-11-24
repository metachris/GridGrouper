This is a quick and dirty algorithm test for an interesting problem.

## Problem

Fill all the seats in a theater with groups of people, where everyone in the same group should sit close to other members of the group. Every available seat may be in use.

## Algorithm

Each group 'eats' into the grid starting at an initial position. If the current seat is available occupy it. Then moves one step in the current direction until an expanding bounding box is reached (`limit_[top|right|bottom|left]`). If the limit is reached, turn clockwise or counter-clockwise, and expand the just hit limit by one for the next round.

## Various

* Author: Chris Hager (chris@metachris.org)
* License: Do whatever you want with it.

## Usage

    $ python gridgrouper.py -h
    Usage: gridgrouper.py [options] size-group1 size-group2 ...

        Example: gridgrouper.py -s 10x15 20 30 10 14

    Options:
      -h, --help            show this help message and exit
      -s SIZE, --size=SIZE  Specify grid columns and rows (eg 15x10)
      -o FORMAT, --ouput=FORMAT
                            Type of output ('grid' or 'csv')

## Example 1

All seats are filled.

#### Input

    gridgrouper.py -s 15x10 24 28 25 36 37

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

Slighly larger grid.

#### Input

    gridgrouper.py -s 18x10 24 28 25 36 37

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


## Example 3

Output in csv format.

#### Input

    gridgrouper.py -s 18x10 24 28 25 36 37 -o csv

#### Output

    group-#; 16,8; 15,8; 14,8; 14,7; 15,7; 16,7; 17,7; 17,8; 17,9; 16,9; 15,9; 14,9; 13,9; 13,8; 13,7; 13,6; 14,6; 15,6; 16,6; 17,6; 12,9; 12,8; 12,7; 12,6
    group-*; 11,8; 10,8; 9,8; 9,7; 10,7; 11,7; 11,9; 10,9; 9,9; 8,9; 8,8; 8,7; 8,6; 9,6; 10,6; 11,6; 7,9; 7,8; 7,7; 7,6; 7,5; 8,5; 9,5; 10,5; 11,5; 12,5; 13,5; 14,5
    group-/; 6,8; 5,8; 4,8; 4,7; 5,7; 6,7; 6,9; 5,9; 4,9; 3,9; 3,8; 3,7; 3,6; 4,6; 5,6; 6,6; 2,9; 2,8; 2,7; 2,6; 2,5; 3,5; 4,5; 5,5; 6,5
    group-o; 1,8; 0,8; 0,7; 1,7; 1,9; 0,9; 0,6; 1,6; 0,5; 1,5; 0,4; 1,4; 2,4; 3,4; 4,4; 5,4; 0,3; 1,3; 2,3; 3,3; 4,3; 5,3; 6,3; 6,4; 0,2; 1,2; 2,2; 3,2; 4,2; 5,2; 6,2; 7,2; 7,3; 7,4; 0,1; 1,1
    group-x; 17,5; 16,5; 15,5; 15,4; 16,4; 17,4; 14,4; 14,3; 15,3; 16,3; 17,3; 13,4; 13,3; 13,2; 14,2; 15,2; 16,2; 17,2; 12,4; 12,3; 12,2; 12,1; 13,1; 14,1; 15,1; 16,1; 17,1; 11,4; 11,3; 11,2; 11,1; 11,0; 12,0; 13,0; 14,0; 15,0; 16,0
