#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
import get_wordnik_data as wn
import get_google_data as g
import datetime
import logging
from logging.config import dictConfig


def setup_logger():
    logging_config = dict(
        version = 1,
        formatters = {
            'f': {'format':
                  '[%(asctime)s | %(levelname)s] %(message)s'}
            },
        handlers = {
            'h': {'class': 'logging.StreamHandler',
                  'formatter': 'f',
                  'level': logging.DEBUG}
            },
        root = {
            'handlers': ['h'],
            'level': logging.DEBUG,
            },
    )

    dictConfig(logging_config)

    logger = logging.getLogger()
    return logger


def generate_tags(extra_tags=[]):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    tags = ['programmatic', today]
    tags.extend(extra_tags)

    return 'tags:{}'.format(' '.join(tags))



def main():
    word_api = wn.get_wordnik_credentials()
    logger = setup_logger()

    # setup files
    files = {
        'word_list': open('data/word_list.txt', 'r'),
        'word_data': open('data/word_data.txt', 'r+')
    }
    media_directory = 'data/media/'

    # read word_list
    word_list = [x.strip('\n').split('\t') for x in files['word_list'].readlines()]
    word_data = [x.strip('\n').split('\t')[0] for x in files['word_data'].readlines()]

    # setup fields and output file
    fields = [
        'word', 'syllables', 'pronunciation', 'etymology', 'definitions',
        'phrases', 'synonyms', 'examples', 'audio', 'image', 'frequency',
        'tags'
    ]
    line = '{' + '}\t{'.join(fields) + '}'
    if generate_tags(['english_vocabulary']) not in word_data[0]:
        files['word_data'].write('{}\n'.format(generate_tags(['english_vocabulary'])))

    # get word data
    total_words = len(word_list)
    for i, entry in enumerate(word_list):
        word = entry[0]
        source = entry[1]
        if word in word_data:
            continue
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
            frequency=g.frequency_chart(word, media_directory),
            tags=source
        )
        files['word_data'].write('{}\n'.format(l))
        logger.info('{} | {}/{} = {}% complete'.format(
            word, i, total_words,  round(float(i) / float(total_words), 2)
        ))

    for f in files.values():
        f.close()


if __name__ == "__main__":
    main()
