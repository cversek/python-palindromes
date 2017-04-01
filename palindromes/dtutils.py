from palindromes import dicttree

if __name__ == "__main__":
    wlist = [
            "a", "apple","application","ape",
            "bear","beaver","bean","beach","box","bondage","beware",
            "car","carp","cython",
            "python","pear","pen",
            "mower",
            "web",
            ]
    FT = dicttree.DictTree()
    FT.add_words(wlist)
    RT = dicttree.DictTree()
    RT.add_words((w[::-1] for w in wlist))
    FC = dicttree.Cursor(FT)
    RC = dicttree.Cursor(RT)
