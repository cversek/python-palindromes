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

#def isorted(iterable):
#    iterable = iter(iterable)
#    pivot = next(iterable)

#    a, b = tee(iterable)
#    for x in isorted(filter(lambda item:item < pivot, a)):
#        yield x
#    yield pivot
#    for x in isorted(filter(lambda item:item >= pivot, b)):
#        yield x


class PalindromeSpace(object):
    def __init__(self, words,
                 do_sort = False
                ):
#        if do_sort:
#            words = isorted(words)  #lazy quick sort
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
                    marker = None
                    if f_letter == r_letter:
                        marker = f_letter
                    elif f_letter == WT_MARKER:
                        marker = '>'
                    elif r_letter == WT_MARKER:
                        marker = '<'
                    else:
                        raise ValueError("bad match, f_letter '%s' != r_letter '%s' and neither is word termination" % (f_letter,r_letter))
                    node2 = steps[i+1]
                    if not self.cyclic_digraph.has_node(node1):
                        self.cyclic_digraph.add_node(node1)
                        added_nodes += 1
                    if not self.cyclic_digraph.has_node(node2):
                        self.cyclic_digraph.add_node(node2)
                        added_nodes += 1
                    if not self.cyclic_digraph.has_edge(node1,node2):
                        self.cyclic_digraph.add_edge(node1, node2, marker=marker)
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
        
    def export_csv(self, filename, attr_keys = ['marker']):
        G = self.cyclic_digraph
        #remap nodes to simple integers in order
        nodes = G.nodes()
        nodes.sort()
        node_map = dict((n,i) for i,n in enumerate(nodes))
        #iterate through nodes, writing out the edge list
        with open(filename,'w') as out_file:
            for source in nodes:
                #build the new graph from simplified nodes
                items = sorted(G.edge[source].items())
                for target, attrs in items:
                    vals = ",".join([attrs[key] for key in attr_keys])
                    out_file.write("%d,%d,%s\n" % (node_map[source],node_map[target], vals))
    def export_json(self, filename):
        G = self.cyclic_digraph
        #remap nodes to simple integers in order
        nodes = G.nodes()
        nodes.sort()
        node_map = dict((n,i) for i,n in enumerate(nodes))
        #iterate through nodes, writing out the edge list
        with open(filename,'w') as out_file:
            out_file.write("[\n")
            for i, source in enumerate(nodes):
                #build the new graph from simplified nodes
                buff = []
                for target, attrs in G.edge[source].items():
                    key = attrs['marker']
                    buff.append("\"%s\":%d," % (key,node_map[target]))
                buff.sort() #arrange in alphabetical order
                buff[-1] = buff[-1].rstrip(',') #remove last comma
                buff = "".join(buff)
                out_file.write("{")
                out_file.write(buff)
                if i < len(nodes) - 1:
                    out_file.write("},\n")
                else:
                    out_file.write("}\n]")
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
    PS = PalindromeSpace(words)
    PS.build()
    G = PS.cyclic_digraph
    from networkx.readwrite import *


