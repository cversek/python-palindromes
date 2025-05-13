####################################################################################################################
""" 
cursor.pxd

desc: 

auth: Craig Wm. Versek (cversek@gmail.com)

date: 3/27/2011
"""
####################################################################################################################
from palindromes.dicttree cimport DictTree, TreeNode, TreeEdge

#declare the interface for Cursor extension type
cdef class Cursor:
    ''' Maintains a pointer to a node in a DictTree instance and provides
        methods for fetching information at that location.
    '''
    #private constants to store precomputed data structures
    cdef object    tree     #tree object
    cdef TreeNode *root     #root of the associated tree
    #make this somewhat accesible
    cdef TreeNode *cursor   #maintains location in the tree

    #C implementation functions   
    #cdef int _set_path(self,char *path) nogil
    cdef int _move_down(self, char letter) nogil
    cdef object _clone(self)

####################################################################################################################    
