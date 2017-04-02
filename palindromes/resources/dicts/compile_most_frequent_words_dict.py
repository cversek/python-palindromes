import re
INPUT_FILENAME  = "500k_wordlist_coca_orig.txt"
OUTPUT_FILENAME = "most_frequent.dict"
EXCLUDED_FILENAME = "excluded.dict"

excluded_file = open(EXCLUDED_FILENAME)
EXCLUDED_SET = set( (w.strip().lower() for w in excluded_file) )

WORD_REGEX = re.compile("^[a-z]+$")

output_file = open(OUTPUT_FILENAME,'w')
for line in open(INPUT_FILENAME):
    try:
        freq, word, parts, ntexts = line.strip().split('\t')
        if WORD_REGEX.match(word) and not word in EXCLUDED_SET:
            output_file.write(word)
            output_file.write("\n")
    except ValueError:
        pass

output_file.close()
