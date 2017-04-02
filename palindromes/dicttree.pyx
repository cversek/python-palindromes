####################################################################################################################
""" 
dicttree.pyx

desc: A data structure for storing a dictionary of words such that it can be quickly searched
      based on its alphabetical descendence

auth: Craig Wm. Versek (cversek@physics.umass.edu)

date: 3/27/2011
"""
####################################################################################################################
#configure cython
cimport cython


#define common literal constants
DEF TRUE      = 1
DEF FALSE     = 0
DEF ROOT_CHAR = c'#'
DEF ROOT_STR  = '#'
DEF WT_CHAR   = c'^'
DEF WT_STR    = b'^'

#define some utility functions on TreeNodes and TreeEdges
cdef TreeNode* create_node(int index) nogil:
    "allocate and initialize a vertex node structure"
    cdef TreeNode* node = <TreeNode *> malloc(sizeof(TreeNode))
    node.index       = index
    node.first_edge  = NULL
    return node

cdef TreeEdge* create_edge(char letter) nogil:
    "allocate and initialize a vertex node structure"
    cdef TreeEdge* edge = <TreeEdge *> malloc(sizeof(TreeEdge))
    edge.letter      = letter
    edge.next_edge   = NULL
    edge.down_node   = NULL
    return edge

#cdef recur_list_paths(VertexNode *node, object paths, object path_accum):
#    if node.letter == WT_CHAR:
#        paths.append( "".join(map(chr,path_accum)) )
#    if node.down_node:
#        new_path_accum = path_accum[:]     #must copy list, since it is mutated
#        new_path_accum.append(node.letter) #include this letter
#        recur_list_paths(node.down_node,new_path_accum,paths)
#    if node.next_edge:
#        recur_list_paths(node.next_edge,path_accum,paths)

cdef void destroy(TreeNode* node) nogil:
    _recur_destroy_nodes(node)
    

cdef void _recur_destroy_nodes(TreeNode* node) nogil:
    "recursively destroy the tree descending from this node"
    if node:
        if node.first_edge:   #follow along any edges first
            _recur_destroy_edges(node.first_edge)  
        free(node)

cdef void _recur_destroy_edges(TreeEdge* edge) nogil:
    if edge:
        if edge.next_edge: #go to next edge first
            _recur_destroy_edges(edge.next_edge)
        if edge.down_node: #go to descendant nodes
            _recur_destroy_nodes(edge.down_node)
        free(edge)
            

####################################################################################################################    
cdef class DictTree:
    ''' A tree based dictionary with each node representing a letter,
        and each path ending on the WORD_END node spells a valid word'''
    def __init__(self, words = None):
        #initialize the tree  
        self.root        = create_node(0)
        self.numNodes    = 1 #one for the root
        self.numWords    = 0
        if not words is None:
            self.add_words(words)
    
    def add_words(self, words):
        "add a list of words to the tree"
        for word in words:
            self.add_word(word) 

    def add_word(self, object word):
        "add a word to the tree"
        #run the low-level add mechanism
        word += WT_STR
        self._add_word(<char *> word)

    def has_word(self, object word, allow_partial = False):
        "check if word is in tree"
        if not allow_partial:
            #add the final termination character to the search
            word += WT_STR
        if self._has_word(<char *> word):
            return True
        else:
            return False

    def __del__(self):
        "recursively destroy the whole tree"
        destroy(self.root) 

    #C implementation   
    cdef void _add_word(self,char* word):
        "add a word to the tree"
        cdef TreeNode *node = self.root         #start at the root
        cdef TreeEdge *edge = NULL
        cdef unsigned int n = strlen(word)
        cdef unsigned int i = 0
        #print "adding word:", word, n
        #walk the tree and create nodes as necessary
        while TRUE:
            #print "\t", i, chr(word[i])
            #create and initialize the linked list if need
            if not node.first_edge:
                #print "\tcreate first_edge"
                node.first_edge = create_edge(word[i])
            edge = node.first_edge          
            #search linked list of letter edges
            #print "\tsearch linked list of letter edges"
            while TRUE:
                if edge.letter == word[i]:  #matched letter
                    #print "\tmatched letter:", chr(word[i])
                    i += 1
                    break
                #add a link if it doesn't already exist
                if not edge.next_edge:
                    #print "\tcreated next_edge:", chr(word[i])
                    edge.next_edge = create_edge(word[i])
                #move to next_edge sibling
                #print "\tmove to next edge"                  
                edge = edge.next_edge
            #check if word is finished
            if i >= n:
                #print "\tfinished, make edge point back to root"
                #print buff,i,buff[i]
                #make the edge point point back to the root
                edge.down_node = self.root
                break #we are finished 
            #follow down to the next state, creating it if it doesn't exists
            if not edge.down_node:
                #print "\tcreating down node:", self.numNodes
                edge.down_node = create_node(self.numNodes) #unique sequential index for the node
                self.numNodes += 1
            #move down_node
            #print "\tmove down"
            node = edge.down_node
        #finish up
        self.numWords += 1 
        return
        
    
    cdef int _has_word(self,char *word):
        #check if word is in tree
        cdef TreeNode *node = self.root    #start at the root
        cdef TreeEdge *edge = NULL
        cdef unsigned int n = strlen(word)
        cdef unsigned int i = 0
        cdef char *buff = <char *> malloc((n + 2)*sizeof(char))
        strcpy(buff,word)         #place word
        strcpy(buff + n, WT_STR)
        #walk the tree nodes according to the letters in word
        try:
            while TRUE:
                #print i, chr(buff[i])
                #check the edge list of this node
                if not node.first_edge:  #edge list does not exist
                    return FALSE
                edge = node.first_edge
                #search linked list of siblings
                while TRUE:
                    if edge.letter == buff[i]:
                        i += 1
                        break
                    if not edge.next_edge:
                        return FALSE
                    #move to next_edge sibling
                    edge = edge.next_edge
                #check if word is finished
                if i >= n:
                    break
                if not edge.down_node:
                    return FALSE
                node = edge.down_node
        finally:
            free(buff)
        return TRUE

####################################################################################################################
