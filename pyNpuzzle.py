import heapq

class AStarSolver:

    def __init__(self, n):
        # The default mode is the classical 8 puzzle (3x3 matix)
        self.N             = n
        self.goal_state    = range(pow(self.N,2))
        self.initial_state = range(pow(self.N,2))

        # The queue with the states to be visited
        self.queue = []

    # Calculate the manhattan distance between two puzzle states
    #
    # For the 8 puzzle assume the following two states:
    #   3 2 5       0 1 2
    #   6 0 1       3 4 5
    #   7 8 4       6 7 8
    #
    # State 1 is represented as : [3,2,5,6,0,1,7,8,4]
    # State 2 is represented as : [0,1,2,3,4,5,6,7,8]
    #
    # The manhattan distance is defined as the sum of necessary moves for each 
    # block, in order to get from State1 to State2
    # Manhattan distance    : Sum of BD for all blocks
    def manhattan_distance(self, state1, state2):
        distance = 0
        for i in range(1, pow(self.N, 2)):
            distance = distance + self.block_distance(state1.index(i), state2.index(i))
        return distance

    # For a single block the distance is the minimum number of moves across
    # x and y direction. 
    #
    # If a block is at position k in state 1 array and the desired position in
    # state2 array is l, then
    # 
    # Required x movements  : X = abs((k mod N) - (l mod N))
    # Required y movements  : Y = abs((k div N) - (l div N))
    # Single block distance : BD = X + Y
    def block_distance(self, index1, index2):
        X = abs( (index1 % self.N) - (index2 % self.N) )
        Y = abs( (index1 / self.N) - (index2 / self.N) )
        return X+Y

    # Helper function that returns the manhattan distance between a state and
    # the problem's goal state
    def h(self, state):
        return self.manhattan_distance(state, self.goal_state)

    # Add a state to the queue of states to be visited
    def enqueue(self, state):
        (layout, parent, h, g) = state

        # Calculate f
        f = h + g
        heapq.heappush(self.queue, (f,state))

    # Pop a node from the queue and return it
    def dequeue(self):
        if len(self.queue) == 0:
            return None
        (f, state) = heapq.heappop(self.queue)
        return state

    # pretty print a layout
    def pretty_print(self, layout):
       for i in range(pow(self.N,2)):
            if layout[i]:
                print '%(n)#2d' % {'n': layout[i]},
            else:
                print '  ',
            if i % self.N == self.N - 1:
                print

    # Given a state find the search path that leaded to this state
    # A list of layouts is returned
    def get_path(self, state):
        path = []
        while state:
            (layout, parent, h, g) = state
            path.insert(0, layout)
            state = parent
        return path

    # Print the given path
    def print_path(self, path):
        n = 0
        for p in path:
            print '#', n
            self.pretty_print(p)
            print
            n = n + 1


    # Given a layout return a list of all possible transitions from this state
    #
    # In order to determine the valid transitions we need to find the position
    # of the empty tile (0).
    def transitions(self, layout):
        t = []
        i = layout.index(0)

        # calculate x,y position in 2d grid
        x = i % self.N
        y = i / self.N

        possible_moves = []
        possible_moves.append((x-1,y))
        possible_moves.append((x+1,y))
        possible_moves.append((x,y+1))
        possible_moves.append((x,y-1))

        # check all possible moves
        for k in possible_moves:
            (new_x, new_y) = k
            j = new_y * self.N + new_x
            if (new_x >= 0 and new_x < self.N and new_y >= 0 and new_y < self.N) :
                t.append(self.swap(list(layout), i, j))
        return t

    # Swap item at position i with item at position j and return the new layout
    def swap(self, layout, i, j):
        tmp = layout[i]
        layout[i] = layout[j]
        layout[j] = tmp
        return layout

    # Solve the N-puzzle problem using A* algorithm
    # 
    # Returns a state. A state is a tuple consisting of the following:
    # 
    # layout : the current puzzle layout
    # parent : the parent state
    # h      : the heuristic value for the state
    # g      : the cost up to this state
    # 
    # For more details about the A* algorithm check the Wikipedia article:
    #   http://en.wikipedia.org/wiki/A*_search_algorithm
    def solve(self):
        state = (self.initial_state, None, self.h(self.initial_state), 0)

        # if this is the goal state return it
        if self.initial_state == self.goal_state:
            return state

        # add the initial state to the queue
        self.enqueue(state)

        # the main loop of A* algorithm
        while True:
            state = self.dequeue()

            if (not state):
                return None

            (layout, parent, h, g) = state
            transitions = self.transitions(layout)
            for t in transitions:
                # if it is the goal return it
                if t == self.goal_state:
                    return (t, state, 0, g+1)

                new_state = (t, state, self.h(t), g+1)
                self.enqueue(new_state)
