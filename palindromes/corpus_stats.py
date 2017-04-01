import nltk, re, itertools, numpy

DEFAULT_WORD_REGEX = re.compile(r"^[a-z]+$")

class CorpusStats(object):
    def __init__(self,corpus_reader, word_regex = DEFAULT_WORD_REGEX, simplify_tags = False):
        self.corpus_reader = corpus_reader
        self.word_regex = word_regex   
        self.tagged_words = list((word,pos) for word, pos in self.corpus_reader.tagged_words(simplify_tags=simplify_tags) if self.word_regex.match(word))
        self.word_to_pos_cfd = nltk.ConditionalFreqDist(self.tagged_words)
        self.pos_to_word_cfd = nltk.ConditionalFreqDist((pos,word) for word, pos in self.tagged_words)
        self.pos_bigram_cfd  = nltk.ConditionalFreqDist((tag1[1],tag2[1]) for tag1, tag2 in nltk.bigrams(self.tagged_words) 
                                                                          if      self.word_regex.match(tag1[0]) 
                                                                              and self.word_regex.match(tag2[0])
                                                        )


    def sent_correlate(self, sent):
        corr_func = self.word_correlate_pos_bigram
        c = numpy.array([corr_func(w1,w2) for w1,w2 in nltk.bigrams(sent)])
        return c                                                                   
                                                        
    def word_correlate_pos_bigram(self, w1, w2):
        w1_pos_list = self.word_to_pos_cfd[w1].keys()
        w2_pos_list = self.word_to_pos_cfd[w2].keys()
        pos_pairs = list(itertools.product(w1_pos_list, w2_pos_list))
        #buff = ["-(%s,%s)" % (w1,w2)]
        total_prob = 0.0
        for p1,p2 in pos_pairs:
            Pw1p1 = self.word_to_pos_cfd[w1].freq(p1)
            Pw2p2 = self.word_to_pos_cfd[w2].freq(p2)
            Pp1p2 = self.pos_bigram_cfd[p1].freq(p2)
            prob  = Pw1p1*Pw2p2*Pp1p2
            total_prob += prob
            #buff.append("(%s %f)\t(%s %f)\t[%f]\t-> %f" % (p1,Pw1p1,p2,Pw2p2,Pp1p2, prob))
        #buff.append("-----total prob = %f" % total_prob)
        #print "\n".join(buff)    
        return total_prob

    def pickle_dump(self, filename):
        import pickle
        pf = open(filename,'w')
        pickle.dump(self,pf)
        pf.close()

    @classmethod
    def pickle_load(self, filename):
        import pickle
        pf = open(filename,'r')
        obj = pickle.load(pf)
        pf.close() 
        return obj

