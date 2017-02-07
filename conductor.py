#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
import get_wordnik_data as wn
import get_google_data as g

def main():
    word_api = wn.get_wordnik_credentials()

    # setup files
    files = {
        'word_list': open('data/word_list.txt', 'r'),
        'word_data': open('data/word_data.txt', 'w+')
    }
    media_directory = 'data/media/'

    # read word_list
    word_list = [x.strip('\n') for x in files['word_list'].readlines()]

    # setup fields
    fields = [
        'word', 'syllables', 'pronunciation', 'etymology', 'definitions',
        'phrases', 'synonyms', 'examples', 'audio', 'image', 'frequency'
    ]
    line = '{' + '}\t{'.join(fields) + '}'

    # get word data
    for word in word_list:
        print 'working on {}\n'.format(word)
        # write words to text file
        l = line.format(
            word=word,
            syllables=wn.format_hyphenation(word_api, word),
            pronunciation=wn.format_pronunciation(word_api, word),
            etymology=wn.format_etymologies(word_api, word),
            definitions=wn.format_definitions(word_api, word),
            phrases=wn.format_phrases(word_api, word),
            synonyms=wn.format_synonyms(word_api, word),
            examples=wn.format_examples(word_api, word),
            audio=wn.format_audio(word_api, word),
            image=g.find_image(word, media_directory),
            frequency=g.frequency_chart(word, media_directory)
        )
        files['word_data'].write('{}\n'.format(l))

    for f in files.values():
        f.close()


if __name__ == "__main__":
    main()
