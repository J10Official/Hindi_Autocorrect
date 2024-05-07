import string

def read_corpus(filename, output_filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        words = []
        for line in lines:
            word = line.split('\t')[0].strip()  # strip leading/trailing whitespace
            if word:  # only add word if it's not empty
                # remove punctuation, pipe character, digits, and ascii letters
                word = word.translate(str.maketrans('', '', string.punctuation + '।' + string.digits + "०१२३४५६७८९" + "’–"+ '…' + string.ascii_letters + '—”“è'))
                if word:  # only add word if it's not empty after removing punctuation
                    words.append(word + '\n')  # add newline character to each word

    with open(output_filename, 'w', encoding='utf-8') as file:
        file.writelines(words)

# invoke this function
read_corpus(r'Hindi_corpus.txt', r'output_corpus.txt')