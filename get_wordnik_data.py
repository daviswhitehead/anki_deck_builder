from wordnik import *
import sys
import re
sys.path.append('/Users/dwhitehead/Documents/github/utils/')
from utils import credentials
import requests


def get_wordnik_credentials():
    wordnik_credentials = credentials.read_cfg(
        credentials.find_pass_cfg(),
        'wordnik'
    )

    # setup wordnik client
    api_url = 'http://api.wordnik.com/v4'
    client = swagger.ApiClient(
        wordnik_credentials.get('apikey', ''),
        api_url
    )
    word_api = WordApi.WordApi(client)
    return word_api


def format_hyphenation(word_api, word):
    html = '<font style="font-family: avenir next; font-size: 14">{}</font>'
    hyphens = []

    try:
        for hyphen in word_api.getHyphenation(word):
            tag = '<b>{}</b>' if hyphen.type == 'stress' else '<font>{}</font>'
            hyphens.append(
                tag.format(
                    format_string(hyphen.text)
                )
            )
    except Exception as e:
        # print 'hyphenation error'
        # print e
        html = ''

    html = html.format(' - '.join(hyphens))

    return format_HTML(html)


def format_pronunciation(word_api, word):
    html = ''
    content = '<font style="font-family: avenir next; font-size: {}">{}</font>'

    try:
        for count, textPronunciations in enumerate(word_api.getTextPronunciations(word)):
            if textPronunciations.rawType != 'ahd-legacy':
                continue
            font_size = 14
            html += content.format(
                font_size,
                format_string(textPronunciations.raw)
            )
    except Exception as e:
        # print 'pronunciation error'
        # print e
        html = ''

    return format_HTML(html)


def format_etymologies(word_api, word):
    html = '<font style="font-family: avenir next; font-size: 14">{}</font>'

    try:
        ety = format_string(
            re.search(
                '<ety>(.+)</ety>', str(word_api.getEtymologies(word))
            ).groups()[0].replace(
                '<ets>', '<i>'
            ).replace(
                '</ets>', '</i>'
            )
        )
        html = html.format(ety)
    except Exception as e:
        # print 'etymology error'
        # print e
        html = ''

    return format_HTML(html)


def format_definitions(word_api, word):
    # colors from http://htmlcolorcodes.com/color-chart/
    color_map = {
        'NOUN': '#E74C3C',
        'PRONOUN': '#8E44AD',
        'VERB-TRANSITIVE': '#2980B9',
        'VERB-INTRANSITIVE': '#3498DB',
        'ADJECTIVE': '#16A085',
        'ADVERB': '#F1C40F',
        'PREPOSITION': '#E67E22',
        'CONJUNCTION': '#95A5A6',
        'INTERJECTION': '#2E4053'
    }
    html = '<ol>'
    content = '<li style="font-family: avenir next; font-size: {}"><font color="{}">{} - {}</font></li>'

    try:
        for count, definition in enumerate(word_api.getDefinitions(word)):
            font_size = 18 if count == 0 else 10
            html += content.format(
                font_size,
                color_map.get(format_string(definition.partOfSpeech.upper()), 'black'),
                format_string(definition.partOfSpeech.upper()),
                format_string(definition.text)
            )
        html += '</ol>'
    except Exception as e:
        # print 'definitions error'
        # print e
        html = ''

    return format_HTML(html)


def format_phrases(word_api, word):
    html = '<font style="font-family: avenir next; font-size: 14">{}</font>'
    phrases = []

    try:
        for phrase in word_api.getPhrases(word):
            phrases.append('<font>{} {}</font>'.format(
                format_string(phrase.gram1),
                format_string(phrase.gram2)
            ))

        html = html.format(', '.join(phrases))
    except Exception as e:
        # print 'phrases error'
        # print e
        html = ''

    return format_HTML(html)


def format_synonyms(word_api, word):
    html = ''
    content = '<font style="font-family: avenir next; font-size: {}">{}</font>'

    try:
        for count, relatedWords in enumerate(word_api.getRelatedWords(word)):
            if relatedWords.relationshipType != 'synonym':
                continue
            font_size = 14
            html += content.format(
                font_size,
                format_string(', '.join(relatedWords.words))
            )
    except Exception as e:
        # print 'synonyms error'
        # print e
        html = ''

    return format_HTML(html)


def format_examples(word_api, word):
    html = '<ol>'
    content = '<li style="font-family: avenir next; font-size: {}"><font>{}</font></li>'

    try:
        for count, example in enumerate(word_api.getExamples(word).examples):
            font_size = 18 if count == 0 else 10
            html += content.format(font_size, format_string(example.text))

        html += '</ol>'
    except Exception as e:
        # print 'examples error'
        # print e
        html = ''

    return format_HTML(html)


def format_audio(word_api, word):
    source = '[sound:{}]'
    try:
        audio = word_api.getAudio(word)[0]
        r = requests.get(audio.fileUrl)
        if r.status_code == 200:
            file_name = '{}_audio.mp3'.format(word)
            with open('data/media/{}'.format(file_name), 'w+') as f:
                f.write(r.content)

            return source.format(file_name)
    except Exception as e:
        # print 'audio error'
        # print e
        pass

    return ''


def format_string(string):
    return unicode(string).encode('utf-8')


def format_HTML(html):
    return html.replace('\t', '').replace('\n', '')


def main():
    word_api = get_wordnik_credentials()

    # setup files
    files = {
        'word_list': open('data/word_list.txt', 'r'),
        'word_data': open('data/word_data.txt', 'w+')
    }

    # read word_list
    word_list = [x.strip('\n') for x in files['word_list'].readlines()]

    # setup fields
    fields = [
        'word', 'syllables', 'pronunciation', 'etymology', 'definitions',
        'phrases', 'synonyms', 'examples', 'audio'
    ]
    line = '{' + '}\t{'.join(fields) + '}'

    # get word data
    for word in word_list:
        print 'working on {}\n'.format(word)
        # write words to text file
        l = line.format(
            word=word,
            syllables=format_hyphenation(word_api, word),
            pronunciation=format_pronunciation(word_api, word),
            etymology=format_etymologies(word_api, word),
            definitions=format_definitions(word_api, word),
            phrases=format_phrases(word_api, word),
            synonyms=format_synonyms(word_api, word),
            examples=format_examples(word_api, word),
            audio=format_audio(word_api, word)
        )
        files['word_data'].write('{}\n'.format(l))

    for f in files.values():
        f.close()


if __name__ == "__main__":
    main()
