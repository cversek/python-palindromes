""" 6/25/2011
"""
import time, sys, itertools
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
                              

class PalindromeSpace(object):
    def __init__(self, words):
        fwords, rwords = itertools.tee(words,2)                 #create two idependent iterables
        self.forward_tree = DictTree(fwords)                    #feed forward words, lazily
        self.reverse_tree = DictTree((w[::-1] for w in rwords)) #reverse the words, lazily
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
    import itertools, random
    import numpy
    from pylab import *
    
    from random import sample

    from plot_utils import color_slice

    
    PLOT_FUNC = loglog

    N = 1000
    word_file = open('../palindromes/dicts/most_frequent.dict')
    WORDS = (w.strip().lower() for w in word_file)
    WORDS = list(WORDS)[:N]
#    WORDS = 'beware woman on a mower web'.split()
    #WORDS = 'eva can i stab bats in a cave'.split()
    #WORDS = 'race car trace cart'.split()
    WORDS.sort()
    PS = PalindromeSpace(WORDS)

    import nltk
    
    def tag(text):
        text = nltk.word_tokenize(text)
        return nltk.pos_tag(text)

    PS.build()

#    import networkx as nx
#    G = PS.cyclic_digraph
#    pos = nx.graphviz_layout(G)

#    edge_dict = G.edge
#    edge_labels_items = []
#    for edge in G.edges():
#        edge_data = G.get_edge_data(*edge)
#        label = edge_data['f_letter'] or ''
#        if label == WT_MARKER:
#            label = ' '
#        edge_labels_items.append((edge,label))
#    edge_labels = dict(edge_labels_items)
#   
#    f = figure(figsize=(10,10))
#    ax = f.add_subplot(111)
#    ax.set_xticks(())
#    ax.set_yticks(())
#    nx.draw_networkx_edges(G, pos=pos, ax = ax)
#    nx.draw_networkx_nodes(G, pos=pos, ax = ax, node_size = 400)
#    nx.draw_networkx_labels(G, pos=pos, ax = ax, font_size = 6)
#    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels = edge_labels, ax = ax)
##    #networkx.draw(PG.cyclic_digraph)
#    f.savefig("palindrome_graph.svg")
#    show()

#    print '-'*80
#    items = PalindromeWalk._report_log.items()
#    items.sort()
#    for walk_id, rlog in items:
#        print "w%03d:" % walk_id
#        print "\t",
#        print "\n\t".join(rlog)
#        print '-'*80
    
#    arg_perms = itertools.product(('depth','breadth'),repeat=3)
#    arg_perms = itertools.islice(arg_perms,0,7)
#    #arg_perms = [('depth','breadth','depth')]
#    COLORS = color_slice('spectral',5)
#    for i,args in enumerate(arg_perms):
#        kwargs = {'intraword':         args[0],
#                  'interword_forward': args[1],
#                  'interword_reverse': args[2],
#                 }
#        print kwargs
#        PG = PalindromeGenerator(WORDS)
#        stats = PG.build(**kwargs)
#        print stats
#        wc = stats[:,0]
#        uw = stats[:,1]
#        sw = stats[:,2]
#        jw = stats[:,3]
#        dw = stats[:,4]
#        ow = stats[:,5]
#        qs = stats[:,6]
#        figure()
#        PLOT_FUNC(uw,"-", label="unfinished", color=COLORS[0])
#        PLOT_FUNC(sw,"-", label="self", color=COLORS[1])
#        PLOT_FUNC(jw,"-", label="join", color=COLORS[2])
#        PLOT_FUNC(dw,"-", label="dead-end", color=COLORS[3])
#        PLOT_FUNC(qs,"-", label="qsize", color=COLORS[4])
#        print "Digraph stats:"
#        print "\tnum nodes:", len(PG.cyclic_digraph.nodes())
#        print "\tnum edges:", len(PG.cyclic_digraph.edges())
#        legend(loc='best')
#        xlabel("Time")
#        ylabel("Memory")
#        title("Palindrome Cycle Discovery: Algorithm Comparison (%d random words)" % N)
#    

#    show()

#    
    

    
    #sys.exit()


