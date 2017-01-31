from wordnik import *
from pprint import pprint
import sys
import re
from collections import defaultdict
sys.path.append('/Users/dwhitehead/Documents/github/utils/')
from utils import credentials
import requests


"""
to do:
  - frequency (switch to google ngram)
  - pictures
"""


# GLOBALS
WORD_API = ''


def format_hyphenation(word):
    html = '<font style="font-family: avenir next; font-size: 14">{}</font>'
    hyphens = []

    try:
        for hyphen in WORD_API.getHyphenation(word):
            tag = '<b>{}</b>' if hyphen.type == 'stress' else '<font>{}</font>'
            hyphens.append(
                tag.format(
                    format_string(hyphen.text)
                )
            )
    except Exception as e:
        print 'hyphenation error'
        print e
        html = ''

    html = html.format(' - '.join(hyphens))

    return format_HTML(html)


def format_pronunciation(word):
    html = ''
    content = '<font style="font-family: avenir next; font-size: {}">{}</font>'

    try:
        for count, textPronunciations in enumerate(WORD_API.getTextPronunciations(word)):
            if textPronunciations.rawType != 'ahd-legacy':
                continue
            font_size = 14
            html += content.format(
                font_size,
                format_string(textPronunciations.raw)
            )
    except Exception as e:
        print 'pronunciation error'
        print e
        html = ''

    return format_HTML(html)


def format_etymologies(word):
    html = '<font style="font-family: avenir next; font-size: 14">{}</font>'


    try:
        ety = format_string(
            re.search(
                '<ety>(.+)</ety>', str(WORD_API.getEtymologies(word))
            ).groups()[0].replace(
                '<ets>', '<i>'
            ).replace(
                '</ets>', '</i>'
            )
        )
        html = html.format(ety)
    except Exception as e:
        print 'etymology error'
        print e
        html = ''

    return format_HTML(html)


def format_definitions(word):
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
        for count, definition in enumerate(WORD_API.getDefinitions(word)):
            font_size = 18 if count == 0 else 10
            html += content.format(
                font_size,
                color_map.get(format_string(definition.partOfSpeech.upper()), 'black'),
                format_string(definition.partOfSpeech.upper()),
                format_string(definition.text)
            )
        html += '</ol>'
    except Exception as e:
        print 'definitions error'
        print e
        html = ''

    return format_HTML(html)


def format_phrases(word):
    html = '<font style="font-family: avenir next; font-size: 14">{}</font>'
    phrases = []

    try:
        for phrase in WORD_API.getPhrases(word):
            phrases.append('<font>{} {}</font>'.format(
                format_string(phrase.gram1),
                format_string(phrase.gram2)
            ))

        html = html.format(', '.join(phrases))
    except Exception as e:
        print 'phrases error'
        print e
        html = ''

    return format_HTML(html)


def format_synonyms(word):
    html = ''
    content = '<font style="font-family: avenir next; font-size: {}">{}</font>'

    try:
        for count, relatedWords in enumerate(WORD_API.getRelatedWords(word)):
            if relatedWords.relationshipType != 'synonym':
                continue
            font_size = 14
            html += content.format(
                font_size,
                format_string(', '.join(relatedWords.words))
            )
    except Exception as e:
        print 'synonyms error'
        print e
        html = ''

    return format_HTML(html)


def format_examples(word):
    html = '<ol>'
    content = '<li style="font-family: avenir next; font-size: {}"><font>{}</font></li>'

    try:
        for count, example in enumerate(WORD_API.getExamples(word).examples):
            font_size = 18 if count == 0 else 10
            html += content.format(font_size, format_string(example.text))

        html += '</ol>'
    except Exception as e:
        print 'examples error'
        print e
        html = ''

    return format_HTML(html)


def format_audio(word):
    source = '[sound:{}]'
    try:
        audio = WORD_API.getAudio(word)[0]
        r = requests.get(audio.fileUrl)
        if r.status_code == 200:
            file_name = '{}_audio.mp3'.format(word)
            with open('data/media/{}'.format(file_name), 'w+') as f:
                f.write(r.content)

            return source.format(file_name)
    except Exception as e:
        print 'audio error'
        print e

    return ''


def explorer(func, name):
    # explorer(word_api, 'word_api')
    # explorer(WORD_API.getAudio(word), 'getAudio')
    # explorer(WORD_API.getDefinitions(word), 'getDefinitions')
    # explorer(WORD_API.getEtymologies(word), 'getEtymologies')
    # explorer(WORD_API.getExamples(word), 'getExamples')
    # explorer(WORD_API.getHyphenation(word), 'getHyphenation')
    # explorer(WORD_API.getPhrases(word), 'getPhrases')
    # explorer(WORD_API.getRelatedWords(word), 'getRelatedWords')
    # explorer(WORD_API.getScrabbleScore(word), 'getScrabbleScore')
    # explorer(WORD_API.getTextPronunciations(word), 'getTextPronunciations')
    # explorer(WORD_API.getWord(word), 'getWord')
    # explorer(WORD_API.getWordFrequency(word), 'getWordFrequency')

    print name
    x = func
    print x
    if isinstance(x, list):
        print 'LIST'
        for i in x:
            print i
            pprint(dir(i))
    else:
        pprint(dir(x))
    print


def format_string(string):
    return unicode(string).encode('utf-8')


def format_wordFrequency(word):
    # <div class="point" style="height: 15px;"></div>

    html = """
    <html>
    <head>
        <style type="text/css">
            .masterContainer {{
              width:600px;
              height:300px;
              margin: 20px;
            }}
            .vAxisLabelContainer{{
              height: 200px;
              width: 15px;
              position: relative;
              float: left;
            }}
            .vAxisLabel{{
              font-family: avenir next;
              font-size: 10;
              position: absolute;
            }}
            .vAxisTickContainer{{
              height: 200px;
              width: 15px;
              position: relative;
              float: left;
            }}
            .vAxisTick{{
              width: 10px;
              position: relative;
              float: left;
              border-bottom: 2px solid black;
            }}
            .pointContainer{{
              height: 200px;
              width: 324px;
              position: relative;
              float: left;
            }}
            .point{{
              float: left;
              width: 0.4694835681%;
            }}
            .hAxisContainer{{
              height: 30px;
              width: 324;
              position: absolute;
              margin: 0;
              top: 195px;
              margin: 30px;
            }}
            .hAxisTick{{
              height: 10;
              border-right: 2px solid black;
              float: left;
              position: relative;
            }}
            .hAxisLabel{{
              font-family: avenir next;
              font-size: 10;
              position: absolute;
              bottom: 0px;
            }}
            .numberContainer{{
              height: 100%;
              width: 100%;
              position: absolute;
            }}
            .number{{
              font-family: avenir next;
              font-size: 75;
              float: right;
              top: -15;
              position: relative;
            }}
        </style>
    </head>
    <body>
        <div style="" class="masterContainer">
          <div class="vAxisTickContainer">
           <font class="vAxisLabel" style="top: -5px;right: 5px;">{maxCount}</font>
          <font class="vAxisLabel" style="top: 94px;right: 5px;">{maxCountHalf}</font>
          <font class="vAxisLabel" style="top: 192px;right: 5px;">0</font>
      </div>
        <div class="vAxisTickContainer">
          <div class="vAxisTick" style="height: 0px;"></div>
          <div class="vAxisTick" style="height: 97px;"></div>
          <div class="vAxisTick" style="height: 97px;"></div>

        </div>
        <div class="pointContainer">
          <div class="numberContainer">
              <font color="#D2D2D2" class="number">{totalCount}</font>
            </div>
          {points}
        </div>
        <div class="hAxisContainer">
          <div class="hAxisTick" style="width: 0px;"></div>
          <div class="hAxisTick" style="width: 159px;"></div>
          <div class="hAxisTick" style="width: 159px;"></div>
          <font class="hAxisLabel" style="left: -3.5%;">1800</font>
          <font class="hAxisLabel" style="left: 46.5%;">1906</font>
          <font class="hAxisLabel" style="left: 96.5%;">2012</font>
        </div>
    </div>
    </body>
    </html>
    """

    points = ''
    data = defaultdict(dict)
    wordFrequency = WORD_API.getWordFrequency(word)
    totalCount = wordFrequency.totalCount
    maxCount = 0

    for freq in wordFrequency.frequency:
        count = float(freq.count)
        data[int(freq.year)]['count'] = count
        if count > maxCount:
            maxCount = count
    for year in xrange(1800, 2013, 1):
        count = data.get(year, {}).get('count', 0.0)
        height = (abs(maxCount - count) / maxCount)
        data[year]['height'] = height
        px = 0 if count == 0 else 1
        points += '<div class="point" style="height: {}%;border-bottom: {}px solid black;"></div>'.format(
            height * 100,
            px
        )
    # print html
    # print points
    html = html.format(
        maxCount=int(maxCount),
        maxCountHalf=int(maxCount / 2),
        totalCount=totalCount,
        points=points
    )
    return format_HTML(html)


def format_HTML(html):
    return html.replace('\t', '').replace('\n', '')


def main():
    # get wordnik credentials
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
    global WORD_API
    WORD_API = WordApi.WordApi(client)

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
        # explorer(WORD_API.getAudio(word), 'getAudio')
        # write words to text file
        l = line.format(
            word=word,
            syllables=format_hyphenation(word),
            pronunciation=format_pronunciation(word),
            etymology=format_etymologies(word),
            definitions=format_definitions(word),
            phrases=format_phrases(word),
            synonyms=format_synonyms(word),
            examples=format_examples(word),
            audio=format_audio(word)
        )
        files['word_data'].write('{}\n'.format(l))

    for f in files.values():
        f.close()


if __name__ == "__main__":
    main()
