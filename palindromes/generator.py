""" 4/24/2011
"""
import time, sys, itertools, random, copy
from random import choice
from collections import deque
import numpy
import networkx

from palindromes.space import PalindromeSpace
from palindromes.corpus_stats import CorpusStats

    

ROOT_NODE = (0,0)
WT_MARKER = '^'
WT_MARKER_SET = set((WT_MARKER,))
ALPHA_SET = set("abcdefghijklmnopqrstuvwxyz")
                              

class PartialPalindrome(object):
    def __init__(self, init_walk = None):
        self.walk    = []    
        self.f_words = []
        self.r_words = []
        self.f_buff = []
        self.r_buff = []
        self.current_node = ROOT_NODE
        if not init_walk is None:
            self.extend(init_walk)

    def append(self, step):
        self.walk.append(step)
        n1, f_letter, r_letter, n2 = step
        self.current_node = n2
        if not f_letter is None:
            if f_letter == WT_MARKER:
                self.f_words.append("".join(self.f_buff))
                self.f_buff = []
            else:
                self.f_buff.append(f_letter)
        if not r_letter is None:
            if r_letter == WT_MARKER:
                self.r_buff.reverse()
                self.r_words.append("".join(self.r_buff))
                self.r_buff = []
            else:
                self.r_buff.append(r_letter)    
    
    def extend(self, walk):
        for step in walk:
            self.append(step)

    def clone(self):
        cls = self.__class__
        new_pp = cls(init_walk = self.walk)
        return new_pp

    def __str__(self):
        s = []
        s.append(' '.join(self.f_words))
        s.append(' ')
        if self.f_buff:
            s.append('(%s' % ''.join(self.f_buff))
        s.append('|')
        if self.r_buff:
            s.append('%s)' % ''.join(self.r_buff[::-1]))
        s.append(' ')
        s.append(' '.join(self.r_words[::-1]))
        s = ''.join(s)
        return s
            
            
            

class PalindromeGenerator(object):
    def __init__(self, palindrome_space):
        self.palindrome_space = palindrome_space
        if not self.palindrome_space._isbuilt:
            t1 = time.time() 
            print "building palindrome space..."
            self.palindrome_space.build()
            t2 = time.time()
            print "(%0.3f seconds)" % (t2-t1)
        try:
            t1 = time.time()
            print "looking for cached corpus statistics..."   
            self.corpus_stats = CorpusStats.pickle_load('brown_corpus_stats.pkl')
            t2 = time.time()
            print "found. (%0.3f seconds)" % (t2-t1)   
        except:
            t1 = time.time()
            print "not found, computing..."           
            from nltk.corpus import brown
            self.corpus_stats = CorpusStats(brown)
            self.corpus_stats.pickle_dump('brown_corpus_stats.pkl')
            t2 = time.time()
            print "cached. (%0.3f seconds)" % (t2-t1)  

    def word_walks(self, start_node = None, start_walk = None):  
        if start_walk is None:
            start_walk = []
            if start_node is None:
                start_node = ROOT_NODE
        elif start_node is None:
            last_step  = start_walk[-1]
            start_node = last_step[3]  #the last node stepped to
        return self._recur_word_walks(n1 = start_node, walk = start_walk)

    def _recur_word_walks(self, n1, walk):
        cyclic_digraph = self.palindrome_space.cyclic_digraph
        for n2 in cyclic_digraph.successors(n1):
            edge_data = cyclic_digraph.get_edge_data(n1,n2)
            f_letter = edge_data['f_letter']
            r_letter = edge_data['r_letter']
            step = (n1,f_letter,r_letter, n2)
            new_walk = walk[:]
            new_walk.append(step)
            #print step
            if f_letter == WT_MARKER or r_letter == WT_MARKER:
                yield new_walk
            else:
                for w in self._recur_word_walks(n1=n2, walk=new_walk):
                    yield w

    def generate_palindrome(self):
        #init_walks = self.word_walks()
        #ppq = deque([PartialPalindrome(init_walk = w) for w in init_walks])
        ppq = deque([PartialPalindrome()])        
        while True:
            pp = ppq.pop()
            start_node = pp.current_node
            ranked_pps = []     
            for i, new_walk in enumerate(self.word_walks(start_node = start_node)):
                new_pp = pp.clone()
                new_pp.extend(new_walk)
                score = 0.0
                if new_pp.current_node == ROOT_NODE: #if is a palindrome
                    corr  = self.corpus_stats.sent_correlate(new_pp.f_words + new_pp.r_words[::-1])
                    #print "corr:", corr
                    score = corr.mean()
                else:
                    f_corr = self.corpus_stats.sent_correlate(new_pp.f_words)
                    r_corr = self.corpus_stats.sent_correlate(new_pp.r_words[::-1])
                    #print "f_corr:", f_corr
                    #print "r_corr:", r_corr
                    if   len(f_corr) == 0 and len(r_corr) >= 1:
                        score = r_corr.mean()
                    elif len(r_corr) == 0 and len(f_corr) >= 1:
                        score = f_corr.mean()
                    elif len(r_corr) == 0 and len(f_corr) == 0:
                        score = 0.0
                    else:   
                        score = (f_corr.mean() + r_corr.mean())/2.0       
                #print "score:", score
                #print "-"*10
                ranked_pps.append((score,new_pp))
            ranked_pps.sort()
            rank_quantiles = numpy.array([score for score, new_pp in ranked_pps])
            rank_quantiles = rank_quantiles.cumsum()
            #print "*"*10
            qmax = rank_quantiles.max()
            #print "qmax:",qmax
            choice_index = None
            if qmax == 0.0:  #degenerate scores, fully random select
                choice_index = random.randrange(len(rank_quantiles))
            else:
                rank_quantiles /= rank_quantiles.max()
                #print "rank_quantiles:", rank_quantiles
                t = random.random()
                #print "t:",t
                index_bins = numpy.where(t < rank_quantiles)[0]
                choice_index = int(index_bins[0])
            choice_score, choice_pp = ranked_pps[choice_index]
            #print "choice_index:", choice_index
            #print "choice_score:", choice_score
            #print "choice_pp:", choice_pp
            #print "max_score:", max_score
            #print "max_pp:",    max_pp
            #print "*"*10
            if choice_pp.current_node == ROOT_NODE:
                #print "<<<PALINDROME>>", choice_pp
                return score, choice_pp
            else:
                #print "<<<appending to ppq>>>"
                ppq.append(choice_pp)

#    def _palindrome(self):
        #print "f_buff:", f_buff, "f_words", f_words
        #print "r_buff:", r_buff, "r_words", r_words
        #print "-"*10
        #yield f_words, r_words, f_buff, r_buff               
        
#                if n2 == ROOT_NODE:
#                    if i >= min_size:
#                        fbuff1.extend(fbuff2[:])
#                        if rbuff2[-2::-1] != fbuff2[:-1]:
#                            rbuff1.extend(rbuff2[:])
#                        #print 'fbuff2[:-1]',fbuff2[:-1]
#                        #print 'rbuff2[-2::-1]',rbuff2[-2::-1]
#                        break
#                    else:
#                        fbuff1.extend(fbuff2[:])
#                        rbuff1.extend(rbuff2[:])
#                        fbuff2 = []
#                        rbuff2 = []
            
                    
    @classmethod
    def from_words(cls,words):
        palindrome_space = PalindromeSpace(words)
        return cls(palindrome_space)

    

###############################################################################
#  TEST CODE
###############################################################################

if __name__ == "__main__":
    t1 = time.time()
    print "loading palindrome generator..."
    EXCLUDED = set(w.strip() for w in open('dicts/excluded.dict'))
    
    N = 30000
    word_file = open('dicts/most_frequent.dict')    
    WORDS = (w.strip().lower() for w in word_file)
    WORDS = set(itertools.islice(WORDS,0,N))
    #WORDS = 'beware woman on a mower web'.split()
    PG = PalindromeGenerator.from_words(sorted(WORDS - EXCLUDED))
    t2 = time.time()
    print "(%0.3f seconds)" % (t2-t1) 
    

    M = 1000
    CHUNK = 1000
    t1 = time.time() 
    print "generating palindromes:"
    P_data = []
    try:   
        for i in xrange(M):
            for j in xrange(CHUNK):
                index = i*CHUNK + j
                score, pp = PG.generate_palindrome()
                P_data.append((score,index,str(pp)))
    except KeyboardInterrupt:
        pass
    t2 = time.time()
    print "(%0.3f seconds)" % (t2-t1)
    t1 = time.time() 
    print "sorting and writing output:"
    P_data.sort()
    P_data.reverse()
    outfile = open("palindromes-output.txt",'a')
    used_phrases = set()
    for p in P_data:
        score, index, phrase = p
        if not phrase in used_phrases:
            used_phrases.add(phrase)
            outfile.write("%f %s\n" % (score,phrase))
    outfile.close()
    t2 = time.time()
    print "(%0.3f seconds)" % (t2-t1)

#        sent = p.split()
#        c = CS.sent_correlate(sent)
#        #print "%f\t%s" % (c.mean(),p)
#        P_data.append((float(c.mean()), i, p, c))


    

    

