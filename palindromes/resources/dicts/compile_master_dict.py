import re
MASTER_DICT_FILENANME = "master.dict"

WORD_REGEX = re.compile("^[a-z]+$")

DICT_FILENAMES = [
    'basic-english-words_1k.dict',
    'ispell-enwl-3.1.20/altamer.0',
    'ispell-enwl-3.1.20/altamer.1',
    'ispell-enwl-3.1.20/altamer.2',
    'ispell-enwl-3.1.20/american.0',
    'ispell-enwl-3.1.20/american.1',
    'ispell-enwl-3.1.20/american.2',
    'ispell-enwl-3.1.20/british.0',
    'ispell-enwl-3.1.20/british.1',
    'ispell-enwl-3.1.20/british.2',
    'ispell-enwl-3.1.20/english.0',
    'ispell-enwl-3.1.20/english.1',
    'ispell-enwl-3.1.20/english.2',
    'ispell-enwl-3.1.20/english.3',
]

dict_set = set()

for fn in DICT_FILENAMES:
    dict_file = open(fn)
    for line in dict_file:
        word = line.strip()
        word = word.lower()
        if WORD_REGEX.match(word):
            dict_set.add(word)

dict_list = list(dict_set)
dict_list.sort()


master_dict_file = open(MASTER_DICT_FILENANME,'w')
for word in dict_list:
    master_dict_file.write(word)
    master_dict_file.write("\n")

master_dict_file.close()
