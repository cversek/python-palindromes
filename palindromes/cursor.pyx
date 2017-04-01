####################################################################################################################
""" 
cursor.pyx

desc: A data structure for storing a dictionary of words such that it can be quickly searched
      based on its alphabetical descendence

auth: Craig Wm. Versek (cversek@physics.umass.edu)

date: 3/27/2011
"""
####################################################################################################################
##get common C definition
from dicttree cimport TreeNode, DictTree

#get C string handling functions
cdef extern from "string.h":
    int     strlen(char *s) nogil
    char   *strcpy(char *s1,char *s2) nogil #Copies the string s2 into the character array s1.  The value of s1 is returned.
    char   *strcat(char *s1,char *s2) nogil #Appends the string s2 to the end of character array s1.  
                                            #The first character from s2 overwrites the '\0' of s1. 
                                            #The value of s1 is returned.
#define common literal constants
DEF TRUE      = 1
DEF FALSE     = 0    
DEF ROOT_CHAR = c'#'
DEF ROOT_STR  = '#'
DEF WT_CHAR   = c'^'
DEF WT_STR    = '^'



####################################################################################################################
cdef class Cursor:
    ''' Maintains a pointer to a node in a DictTree instance and provides
        methods for fetching information at that location.
    '''
    def __init__(self, DictTree tree):
        self.tree   = tree
        self.root   = <TreeNode*>  tree.root
        self.cursor = self.root   #initialize the cursor to the tree root

    def at_index(self):
        return int(self.cursor.index)

    def reset(self):
        self.cursor = self.root   #initialize the cursor to the tree root

#    def list_paths(self):
#        paths = []
#        if self.cursor.down:
#            recur_list_paths(self.cursor.down, paths, [])
#        return paths

    def move_down(self, object path):
        """move the cursor to location in the tree specified by a letter 'path'
           returns: 
                  list of succesful moves
        """
        cdef char  *letters = path
        cdef unsigned int n = strlen(letters) 
        cdef char letter       
        cdef unsigned int i = 0

        for i from 0 <= i < n:
            letter = letters[i]
            if not self._move_down(letter):
                return path[:i] 
    
        return path
                   
    def get_edge_set(self):
        cdef TreeEdge *edge = self.cursor.first_edge
        edge_set = set()
        while TRUE:
            if not edge:
                return edge_set
            edge_set.add(chr(edge.letter))                
            edge = edge.next_edge
        #never should arrive here, with proper link-list structure
        return edge_set

    def clone(self):
        return self._clone()


    #C implementation methods
    cdef object _clone(self):
        cdef Cursor new_cur = Cursor(self.tree)
        new_cur.cursor = <TreeNode *> self.cursor
        return new_cur


    cdef int _move_down(self, char letter) nogil:
        cdef TreeEdge *edge = self.cursor.first_edge   #start at the cursor's first edge
        while TRUE:
            if not edge:       #no further edges left to check
                return FALSE
            if edge.letter == letter:
                self.cursor = edge.down_node #set the cursor down to the next state
                return TRUE                  #report sucess
            edge = edge.next_edge
###############################################################################

#def Cursor clone_cursor(Cursor c):
#    new = Cursor()
#    new.root = c.root
#    new.cursor = c.cursor
#    return new
