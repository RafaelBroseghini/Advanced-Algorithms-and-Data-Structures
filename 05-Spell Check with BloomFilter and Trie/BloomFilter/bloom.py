"""
Spell checking with a Bloom Filter.
"""

import math
import time

__author__ = "Rafael Broseghini"

class BloomFilter(object):
    def __init__(self, count, falsePosPct=0):
        m = -1 * (count * math.log(falsePosPct/100)) / ((math.log(2)) ** 2)
        k = (m/count)*math.log(2)
    
        self.bA = bytearray(int(m+7)//8)
        self.numHashes = int(k + 0.5)

        self.masks = {i : 1 << i for i in range(8)}
    
    def add(self, word):
        for i in range(self.numHashes):
            hv = hash(word + str(i))
            bitIndex = hv % (len(self.bA)*8)
            bAindex = bitIndex >> 3
            exponent = bitIndex & 7

            mask = self.masks[exponent]

            self.bA[bAindex] |= mask
    
    def __contains__(self, word):
        for i in range(self.numHashes):
            hv = hash(word + str(i))
            bitIndex = hv % (len(self.bA)*8)

            bAindex = bitIndex >> 3
            exponent = bitIndex & 7

            mask = self.masks[exponent]

            value = self.bA[bAindex] & mask

            if value == 0:
                return False
            
        return True
    
    def __str__(self):
        rv = str(self.numHashes) + " " + str(len(self.bA)) + "\n"
        for i in range(len(self.bA)-1, -1, -1):
            rv += bin(self.bA[i])
        return rv


def read_file_into_bloom_filter(filename: str, bloom: BloomFilter) -> BloomFilter:
    with open(filename, "r+") as infile:
        for word in infile:
            word = word.rstrip()
            bloom.add(word)

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
    vocab = BloomFilter(count, 0.5)
    s = time.time()
    source = read_file_into_array("declarationOfIndependence.txt")
    read_file_into_bloom_filter("wordsEn.txt", vocab)

    for word in source:
        if word not in vocab:
            print("Spelling error: [{}] is not in the English vocabulary of words.".format(word))
    e = time.time()
    print("\nFinished in: {:.2f}s".format(e-s))

if __name__ == '__main__':
    main()
