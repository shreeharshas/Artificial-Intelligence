__author__ = 'Shree Harsha'
import sys
import collections
import operator

"""
-------
Report:
-------
Working of the solution:
------------------------
The solution is implemented using backtracking approach
The question corresponds to the map coloring problem where it is proved that not more than 4 colors are required to color a map

The logic of the below code is as follows:

A: start with the state with highest number of neighbours
consider next unassigned node
    B:assign a new freq to it
        loop along the domain
            C:for every unchecked domain value
            check if it conflicts with the neighbors and if it is not a legacy state
                if conflicts         - check next domain value
                    go back to C
                if no conflict
                    update fMatrix
                    go to A
                if last one also conflicts - ran out of the domain values
                    backtrack
                    go back to B

Implementation in python:
-------------------------
Following are the methods:
get_max_neigh_state - get the list of the states with decreasing order of their neighbour count
check_neighbours - checks for correctness in a state's frequency with respect to its neighbours
                 - returns true if the state's frequency allocation is valid else false

assign_frequency - used to set the given frequency for a particular state by checking if it is legacy state

backtracked_checker - main function to verify and assign/reassign frequencies to the states by backtracking
main - function as a starting point of the program

Future improvements:
--------------------
The approach backtracks but can be made minimalistic where states need not be checked for all frequencies instead,
the current state's frequency assignment may be omitted while assigning the frequencies of its neighbours

"""


states = list()
neighbors = dict()
frequencies_of_states = dict()
legacy_states = list()

#region file inputs region

#input the states info from adjacent-states file
states_neigh_inp_file = 'adjacent-states'
with open(states_neigh_inp_file) as fin:
    line_inp_nstate = fin.readlines()
for i, _ in enumerate(line_inp_nstate):
    line_inp_nstate[i] = line_inp_nstate[i].split()
for line in line_inp_nstate:
    st = line[0]
    states.append(st)
    line.remove(st)
    neighbors[st] = line

#input the constraints info from file name given as parameter by the user
if len(sys.argv) > 1:
    fname = sys.argv[1]
    with open(fname) as f:
        line_input = f.readlines()
    for i, _ in enumerate(line_input):
        line_input[i] = line_input[i].split()
        if len(line_input[i]) > 1:
            legacy_states.append(line_input[i][0])
    if line_input is not None:
        if len(line_input) > 1:
            frequencies_of_states = dict(line_input)

#endregion
frequencies = ['A', 'B', 'C', 'D']

max_neigh_count = 0
max_neigh_state = ''

neigh_count_list = dict()
rev_sorted_neigh_count_list = dict()


def get_max_neigh_state():
    global max_neigh_count
    global max_neigh_state
    global rev_sorted_neigh_count_list
    global states
    for state in states:
        neigh_count = len(neighbors.get(state))
        neigh_count_list[state] = neigh_count
        if neigh_count > max_neigh_count:
            max_neigh_count = neigh_count
            max_neigh_state = state
    rev_sorted_neigh_count_list = sorted(neigh_count_list.items(), key=operator.itemgetter(1), reverse=True) #referred (1) for sorting dictionary based on value

    """print 'before deleting'
    print states"""
    del states[:]
    """print 'after deleting'
    print states"""
    for counter in range(0, len(rev_sorted_neigh_count_list)):
        states.append(rev_sorted_neigh_count_list[counter][0])
        """print rev_sorted_neigh_count_list[counter][0]
    "print 'after reassigning'
    print states"""
#print states
get_max_neigh_state()
#print rev_sorted_neigh_count_list


def check_neighbours(state, frequency):
    if state not in legacy_states:
        neigh_list = neighbors.get(state)
        if neigh_list is not None and len(neigh_list) > 0:
            for neighbor in neigh_list:
                frequency_of_neighbor = frequencies_of_states.get(neighbor)
                if frequency_of_neighbor is not None:
                    if frequency_of_neighbor == frequency:
                        return False
    return True


backtrack_count = 0


def assign_frequency(state, frequency):
    global backtrack_count
    if state not in legacy_states:
        frequencies_of_states[state] = frequency
    test = check_neighbours(state, frequency)
    if test is False:
        backtrack_count += 1
        backtracked_checker(states[(states.index(state)-1) % 50], frequency, True)


def backtracked_checker(state, frequency, is_recheck):
    #print 'aaa'
    global backtrack_count
    #print 'frequencies_of_states' + str(frequencies_of_states) + '\n\n'
    if state not in legacy_states:
        if frequencies_of_states.get(state) is None or is_recheck is True:
            test = check_neighbours(state, frequency)
            temp_state = states[(states.index(state)-1) % 50]
            if temp_state not in legacy_states:
                if test is False and frequency == 'D':  #all domain values failed - so return to previous state and change (backtrack)
                    backtracked_checker(temp_state, frequency, True)
                elif test is False:
                    assign_frequency(state, frequencies[(frequencies.index(frequency)+1) % 4])
                    backtracked_checker(temp_state, frequency, False)

def main():
    if states is not None:
        for state in states:
            assign_frequency(state, 'A')
            backtracked_checker(state, 'A', True)

    #print frequencies_of_states to output file
    f2 = collections.OrderedDict(sorted(frequencies_of_states.items()))

    #region debug info to console
    """for key, f in f2.items():
        print(key),
        print ':',
        print(f)
    """
    #endregion

    outfile = open('results.txt', 'w')
    for key, f in f2.items():
        outstr = str(key) + ' ' + str(f) + '\n'
        outfile.write(outstr)
    outfile.close()
    print 'Number of backtracks:' + str(backtrack_count)

main()

"""References:
(1) http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
"""