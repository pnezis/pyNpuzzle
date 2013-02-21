#!/usr/bin/python

import pyNpuzzle

def main():
    s = pyNpuzzle.AStarSolver(3)

    s.initial_state = [1,6,4,8,7,0,3,2,5]

    state = s.solve()
    path = s.get_path(state)
    s.print_path(path)
    return 0
 
if __name__ == '__main__':
    main()
