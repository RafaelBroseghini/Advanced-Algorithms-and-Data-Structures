"""
Spellchecking with a Trie.
"""

import time
from trie import Trie

__author__ = "Rafael Broseghini"

def read_file_into_trie(filename: str, trie: Trie) -> None:
    with open(filename, "r+") as infile:
        for word in infile:
            word = word.rstrip()
            trie.insert(word)

def read_file_into_array(filename: str) -> list:
    content = []
    with open(filename, "r+") as infile:
        for line in infile:
            line = line.split()
            for w in range(len(line)):
                line[w] = line[w].lower().replace(".","").replace(",","") \
                .replace(":","").replace(";","").replace("--","").replace("'","").replace("&","")

                content.append(line[w])
    return content

def main():
    count = len(open("wordsEn.txt", 'rU').readlines())
    english_vocab = Trie()
    s = time.time()
    declaration_of_independence = read_file_into_array("declarationOfIndependence.txt")
    read_file_into_trie("wordsEn.txt", english_vocab)

    for word in declaration_of_independence:
        if word not in english_vocab:
            print("Spelling error: [{}] is not in the English vocabulary of words.".format(word))
    e = time.time()
    print("\nFinished in: {:.2f}s".format(e-s))

if __name__ == '__main__':
    main()