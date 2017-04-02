""" 6/25/2011
"""
import time, sys
from random import choice
from collections import deque
import numpy
import networkx

from palindromes.dicttree import DictTree
from palindromes.cursor   import Cursor
from palindrome_walk import PalindromeWalk

WT_MARKER = '^'
WT_MARKER_SET = set((WT_MARKER,))
ALPHA_SET = set("abcdefghijklmnopqrstuvwxyz")

from itertools import tee

def isorted(iterable):
    iterable = iter(iterable)
    try:
        pivot = iterable.next()
    except:
        return

    a, b = tee(iterable)
    for x in isorted(filter(lambda item:item < pivot, a)):
        yield x
    yield pivot
    for x in isorted(filter(lambda item:item >= pivot, b)):
        yield x


class PalindromeSpace(object):
    def __init__(self, words, do_sort = False):
        if do_sort:
            words = isorted(words)  #lazy quick sort
        #create two independent iterables
        fwords, rwords = tee(words,2)
        #feed forward words, lazily
        self.forward_tree = DictTree(fwords)
        #reverse the words, lazily
        rwords = (w[::-1] for w in rwords)
        self.reverse_tree = DictTree(rwords)
        self.visited_states_set = set()
        self.cyclic_walks = []
        self.cyclic_digraph = networkx.DiGraph()
        self._isbuilt = False

    def build(self):
        if self._isbuilt:
            return
        #create cyclic palindrome digraph from cyclic paths
        self.cyclic_digraph.add_node((0,0))
        gen_cycles = self._xdiscover_cycles()
        for j, msg in enumerate(gen_cycles):
            msg_type, data = msg
            if msg_type in ['self-cyclic', 'join']:
                walk = data
                steps = walk.steps
                added_nodes = 0
                added_edges = 0
                for i in range(1,len(steps)-1,2):
                    node1 = steps[i-1]
                    f_letter, r_letter = steps[i]
                    node2 = steps[i+1]
                    if not self.cyclic_digraph.has_node(node1):
                        self.cyclic_digraph.add_node(node1)
                        added_nodes += 1
                    if not self.cyclic_digraph.has_node(node2):
                        self.cyclic_digraph.add_node(node2)
                        added_nodes += 1
                    if not self.cyclic_digraph.has_edge(node1,node2):
                        self.cyclic_digraph.add_edge(node1, node2, attr_dict = {'f_letter': f_letter,'r_letter': r_letter} )
                        added_edges += 1
        self._isbuilt = True

    def _xdiscover_cycles(self):
        visited_states_set = set()
        walk_queue = deque()
        new_walk = PalindromeWalk(fcur = Cursor(self.forward_tree), rcur = Cursor(self.reverse_tree))
        walk_queue.append(new_walk)
        while len(walk_queue) != 0:
            walk = walk_queue.pop()
            curr_state = walk.get_state()
            #check for cyclic paths, these are the elements of palindromes!
            if curr_state in walk.steps:
                walk.mark_state()
                steps = walk.steps
                for i in range(0,len(steps),2):
                    state = steps[i]
                    visited_states_set.add(state)
                yield "self-cyclic", walk
                continue

            if curr_state in visited_states_set:
                walk.mark_state()
                steps = walk.steps
                for i in range(0,len(steps),2):
                    state = steps[i]
                    visited_states_set.add(state)
                yield "join", walk
                continue

            #check the accesible edges
            e1, e2, overlap = walk.get_edge_overlap()
            #check for dead-ends
            if not (overlap or WT_MARKER in e1 or WT_MARKER in e2):  #dead-end path
                yield "dead", walk
                continue
      
            #keep track of states walked
            walk.mark_state()
            #follow down all common children except word endings
            for edge_letter in overlap - WT_MARKER_SET:
                new_walk = walk.clone()
                new_walk.move_down_both(edge_letter)
                #put this new walk on the queue, depth-first
                walk_queue.append(new_walk)
            #search over word endings
            if WT_MARKER in e1:   #forward tree ends word here, follow back to root
                new_walk = walk.clone()
                new_walk.move_down_fcur(WT_MARKER)
                #put this new walk on the queue, depth-first
                walk_queue.append(new_walk)
            if WT_MARKER in e2: #reverse tree ends word here, follow back to root  #FIXME if -> elif?
                new_walk = walk.clone()
                new_walk.move_down_rcur(WT_MARKER)
                #put this new walk on the queue, depth-first
                walk_queue.append(new_walk)
            #finished checking, now die quitely
        return
        
    def export(self, filename):
        pass

###############################################################################
#  TEST CODE
###############################################################################
if __name__ == "__main__":
    from itertools import islice
    import palindromes.resources
    
    N = 1000
    
    #get words generator
    words = palindromes.resources.fetch_words("most_frequent.dict")
    #limit to first N words
    words = islice(words, N)
    PS = PalindromeSpace(words, do_sort = True)
    #PS.build()

