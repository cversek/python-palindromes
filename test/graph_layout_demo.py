import itertools, random
import numpy
from pylab import *
from random import sample
from plot_utils import color_slice

from palindromes.space import PalindromeSpace


PLOT_FUNC = loglog

N = 1000
import palindromes.resources
#get words generator
words = palindromes.resources.fetch_words("most_frequent.dict")
#limit to first N words
words = isorted(words)
PS = PalindromeSpace(words)

PS.build()

import networkx as nx
G = PS.cyclic_digraph
pos = nx.graphviz_layout(G)

edge_dict = G.edge
edge_labels_items = []
for edge in G.edges():
    edge_data = G.get_edge_data(*edge)
    label = edge_data['f_letter'] or ''
    if label == WT_MARKER:
        label = ' '
    edge_labels_items.append((edge,label))
edge_labels = dict(edge_labels_items)

f = figure(figsize=(10,10))
ax = f.add_subplot(111)
ax.set_xticks(())
ax.set_yticks(())
nx.draw_networkx_edges(G, pos=pos, ax = ax)
nx.draw_net palindromes.resources.fetch_words("most_frequent.dict")
nx.draw_networkxworkx_nodes(G, pos=pos, ax = ax, node_size = 400)
nx.draw_networkx_labels(G, pos=pos, ax = ax, font_size = 6)
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels = edge_labels, ax = ax)
#    #networkx.draw(PG.cyclic_digraph)
f.savefig("palindrome_graph.svg")
show()

print '-'*80
items = PalindromeWalk._report_log.items()
items.sort()
for walk_id, rlog in items:
    print "w%03d:" % walk_id
    print "\t",
    print "\n\t".join(rlog)
    print '-'*80

arg_perms = itertools.product(('depth','breadth'),repeat=3)
arg_perms = itertools.islice(arg_perms,0,7)
#arg_perms = [('depth','breadth','depth')]
COLORS = color_slice('spectral',5)
for i,args in enumerate(arg_perms):
    kwargs = {'intraword':         args[0],
              'interword_forward': args[1],
              'interword_reverse': args[2],
             }
    print kwargs
    PG = PalindromeGenerator(WORDS)
    stats = PG.build(**kwargs)
    print stats
    wc = stats[:,0]
    uw = stats[:,1]
    sw = stats[:,2]
    jw = stats[:,3]
    dw = stats[:,4]
    ow = stats[:,5]
    qs = stats[:,6]
    figure()
    PLOT_FUNC(uw,"-", label="unfinished", color=COLORS[0])
    PLOT_FUNC(sw,"-", label="self", color=COLORS[1])
    PLOT_FUNC(jw,"-", label="join", color=COLORS[2])
    PLOT_FUNC(dw,"-", label="dead-end", color=COLORS[3])
    PLOT_FUNC(qs,"-", label="qsize", color=COLORS[4])
    print "Digraph stats:"
    print "\tnum nodes:", len(PG.cyclic_digraph.nodes())
    print "\tnum edges:", len(PG.cyclic_digraph.edges())
    legend(loc='best')
    xlabel("Time")
    ylabel("Memory")
    title("Palindrome Cycle Discovery: Algorithm Comparison (%d random words)" % N)


show()





sys.exit()

