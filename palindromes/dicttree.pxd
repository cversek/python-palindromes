###############################################################################
""" 
dicttree.pxd

desc: A data structure for storing a dictionary of words such that it can be 
      quickly searched based on its alphabetical descendence

auth: Craig Wm. Versek (cversek@physics.umass.edu)

date: 3/27/2011
"""
###############################################################################
#import standard C library functions
cdef extern from "stdlib.h":
    void  free(void* ptr)     nogil #free memory at pointer
    void* malloc(size_t size) nogil #allocate memory
    void* realloc(void* ptr, size_t size) nogil 
    

#get C string handling functions
cdef extern from "string.h":
    int     strlen(char* s) nogil
    char*   strcpy(char* s1, char* s2) nogil #Copies the string s2 into the character array s1.  The value of s1 is returned.
    char*   strcat(char* s1, char* s2) nogil #Appends the string s2 to the end of character array s1.  
                                             #The first character from s2 overwrites the '\0' of s1. 
                                             #The value of s1 is returned.

#create a vector structure for simplifying calculations
cdef struct TreeNode
cdef struct TreeEdge

cdef struct TreeNode:
    int       index
    TreeEdge* first_edge

cdef struct TreeEdge:
    char      letter
    TreeEdge* next_edge
    TreeNode* down_node
    
#declare some utility functions on TreeNodes
cdef TreeNode* create_node(int index) nogil

cdef TreeEdge* create_edge(char letter) nogil

#cdef recur_list_paths(TreeNode *node, object paths, object path_accum)

cdef void destroy(TreeNode* node) nogil

#declare the interface for DictTree extension type
cdef class DictTree:
    ''' A tree based dictionary with each node representing a letter,
        and each path ending on the WORD_END node spells a valid word'''
    #generic python attributes

    #readonly python accessible attributes
    cdef readonly int     numNodes   #number of nodes in tree
    cdef readonly int     numWords   #number of nodes in tree

    #private constants to store precomputed data structures
    cdef TreeNode *root     #root of the tree

    #C implementation functions   
    cdef void _add_word(self,char *word)
    cdef int  _has_word(self,char *word)

###############################################################################    
