""" 4/03/2011
"""
import time, sys

from palindromes.cursor   import Cursor

WT_MARKER = '^'
WT_MARKER_SET = set((WT_MARKER,))
ALPHA_SET = set("abcdefghijklmnopqrstuvwxyz")

class PathStep(object):
    def __init__(self, edge_letter, node_index):
        self.edge_letter = edge_letter
        self.node_index  = node_index
        

def x_id(start = 0):
    i = start
    while True:
        yield i
        i += 1

class PalindromeWalk(object):
    _gen_id = x_id()
    _report_log = {}
    def __init__(self, fcur, rcur, steps = None):
        self.fcur = fcur
        self.rcur = rcur
        self.steps = steps or []
        self._id = next(PalindromeWalk._gen_id)

    def get_state(self):
        f_index = self.fcur.at_index()
        r_index = self.rcur.at_index()
        state = (f_index, r_index)
        return state

    def mark_state(self):
        self.steps.append(self.get_state())

    def move_down_both(self, step_letter):
        if step_letter is None:
            return
        else:
            self.fcur.move_down(step_letter)
            self.rcur.move_down(step_letter)
            self.steps.append((step_letter, step_letter))

    def move_down_fcur(self, step_letter):
        if step_letter is None:
            return
        else:
            self.fcur.move_down(step_letter)
            self.steps.append((step_letter, None))
        
    def move_down_rcur(self, step_letter):
        if step_letter is None:
            return
        else:
            self.rcur.move_down(step_letter)
            self.steps.append((None, step_letter))
        
    def reset_fcur(self):
        self.fcur.reset()

    def reset_rcur(self):
        self.rcur.reset()

    def get_edge_overlap(self):
        e1 = self.fcur.get_edge_set()
        e2 = self.rcur.get_edge_set()
        return e1, e2, e1 & e2

    def clone(self):  
        new_walk = PalindromeWalk(fcur = self.fcur.clone(),
                                  rcur = self.rcur.clone(),
                                  steps = self.steps[:],
                                  )
        return new_walk

    def _report(self, msg):
        rlog = PalindromeWalk._report_log.get(self._id, [])
        rlog.append(msg)
        PalindromeWalk._report_log[self._id] = rlog

    def __len__(self):
        return len(self.steps)
    def __str__(self):
        fletters = []
        rletters = []
        for step in self.steps:
            f_step, r_step = step
            if f_step == WT_MARKER:
                fletters.append(" ")
            elif f_step in ALPHA_SET:
                fletters.append(f_step)
            if r_step == WT_MARKER:
                rletters.append(" ")
            elif r_step in ALPHA_SET:
                rletters.append(r_step)
            
        fletters = "".join(fletters)
        rletters = "".join(rletters[::-1]) #traverse rpath backwards
        return "%s|%s" % (fletters,rletters)
                              


###############################################################################
# TEST CODE
###############################################################################
if __name__ == "__main__":
    pass

