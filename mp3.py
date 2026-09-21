"""
Name: Alexandras Biskis
Date: 09/20/2026
Course Name: Artificial Intelligence 1 CPSC-57100
Semester: Fall 2026
Assignment: Machine Problem 3
"""

import random

class Park:
    def __init__(self, height, width, num_kiosks):
        """Create a new park space with given dimensions."""
        self.height = height
        self.width = width
        self.num_kiosks = num_kiosks
        self.gates = set()
        self.kiosks = set()

    def add_gate(self, row, col):
        """Add a gate at a specific location in the park."""
        self.gates.add((row, col))

    def available_spaces(self):
        """Returns all cells not currently used by a gate or kiosk."""
        # Consider all possible cells
        candidates = set(
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
        )

        # Remove all gates and kiosks
        for gate in self.gates:
            candidates.remove(gate)
        for kiosk in self.kiosks:
            candidates.remove(kiosk)
        return candidates

    def hill_climb(self, maximum=None, log=False):
        """Performs hill-climbing to find the optimal kiosk placement."""
        count = 0

        # Start by initializing kiosks randomly
        #randomly initialize kiosks from available spaces
        self.kiosks = set()
        for i in range(self.num_kiosks):
            self.kiosks.add(random.choice(list(self.available_spaces())))
        if log:
            print("Initial state: cost", self.get_cost(self.kiosks))

        # Continue until we reach the maximum number of iterations
        while maximum is None or count < maximum:
            count += 1
            best_neighbors = []
            best_neighbor_cost = None

            # Consider moving each kiosk
            for kiosk in self.kiosks:

                # Task for students: Get neighbors for each kiosk
                for replacement in self.get_neighbors(*kiosk):

                    # Generate a neighboring set of kiosks
                    neighbor = self.kiosks.copy()
                    neighbor.remove(kiosk)
                    neighbor.add(replacement)

                    # Check if neighbor is the best so far
                    cost = self.get_cost(neighbor)
                    if best_neighbor_cost is None or cost < best_neighbor_cost:
                        best_neighbor_cost = cost
                        best_neighbors = [neighbor]
                    elif best_neighbor_cost == cost:
                        best_neighbors.append(neighbor)

            # If none of the neighbors are better than the current state
            if best_neighbor_cost >= self.get_cost(self.kiosks):
                return self.kiosks

            # Move to the best neighboring state
            else:
                if log:
                    print(f"Found better neighbor: cost {best_neighbor_cost}")
                self.kiosks = random.choice(best_neighbors)

    # Task for students: Implement get_cost function
    def get_cost(self, kiosks):
        """Calculates the total distance from gates to the nearest kiosk."""
        total = 0 # initializes total cost
        for gate in self.gates: # for each gate in the set, loop through
            best = None
            for kiosk in kiosks: # then loop through each kiosk
                Manhattan_dist = abs(gate[0] - kiosk[0]) + abs(gate[1] - kiosk[1]) # find Manhattan distance between the gate and each kiosk
                if best is None or Manhattan_dist < best: # if this distance is better (less than) what we already found to be best
                    best = Manhattan_dist # then set it to the new best
            total = total + best # grab total
        return total

    # Task for students: Implement get_neighbors function
    def get_neighbors(self, row, col):
        """Returns neighbors not already containing a gate or kiosk."""
        result = set() # initializing a set

        candidates = [ # considerations
            (row - 1, col), # up
            (row + 1, col), # down
            (row, col - 1), # left
            (row, col + 1) # right
        ]

        for r, c in candidates:
            if r < 0 or r >= self.height: # checks if row is out of bounds
                continue
            if c < 0 or c >= self.width: # checks if column is out of bounds
                continue
            if (r, c) in self.gates: # checks if there is already a gate
                continue
            if (r, c) in self.kiosks: # checks if there is already a kiosk
                continue
            result.add((r, c)) # if it passes all checks then we add it to the result set of neighbors

        return result

# Create a new park and add gates
print('Artificial Intelligence')
print('MP3: Optimizing Kiosk Placement Using Hill Climbing Algorithm')
print('SEMESTER: Fall 2026')
print('NAME: Alexandras Biskis')
print()

p = Park(height=15, width=15, num_kiosks=3)
p.add_gate(2, 3)
p.add_gate(10, 6)
p.add_gate(5, 9)
p.add_gate(7, 12)
p.add_gate(12, 4)

# Use hill climbing to find the best kiosk placement
kiosks = p.hill_climb(log=True)
print("Best kiosk locations:", kiosks)
print("Minimum total distance to all gates:", p.get_cost(kiosks))
