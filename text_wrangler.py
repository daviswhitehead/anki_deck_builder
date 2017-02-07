#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
from collections import defaultdict


def main():
    # setup files
    files = {
        'gre_high_frequency_words': open('data/gre_high_frequency_words.txt', 'r'),
        'vocabulary_com_top_1000': open('data/vocabulary_com_top_1000.txt', 'r'),
        'word_list': open('data/word_list.txt', 'w')
    }

    # read word_list
    vocabulary_com_top_1000 = [
        x.strip('\n') for x in files['vocabulary_com_top_1000'].readlines()
    ]
    gre_high_frequency_words = [
        x.strip('\n') for x in files['gre_high_frequency_words'].readlines()
    ]

    word_list = defaultdict(lambda: defaultdict(dict))
    for word in vocabulary_com_top_1000 + gre_high_frequency_words:
        tags = []
        if word in vocabulary_com_top_1000:
            tags.append('vocabulary_com_top_1000')
        if word in gre_high_frequency_words:
            tags.append('gre_high_frequency_words')

        word_list[word]['tags'] = ' '.join(tags)

    for word in word_list:
        files['word_list'].write('{}\t{}\n'.format(word, word_list[word]['tags']))

    for f in files.values():
        f.close()


if __name__ == "__main__":
    main()
