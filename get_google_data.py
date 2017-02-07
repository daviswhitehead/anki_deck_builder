#!/usr/bin/env python
# -*- coding: utf-8 -*
from bs4 import BeautifulSoup
import urllib2
import os
import pandas as pd
import re
from ast import literal_eval
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import ujson as json


def get_soup(url, header):
    return BeautifulSoup(
        urllib2.urlopen(
            urllib2.Request(url, headers=header)
        ),
        'html.parser'
    )


def image_html(file_name):
    return '<img src="{}" />'.format(file_name.split('/')[-1])


def frequency_chart(word, directory):
    # config
    start_year = 1800
    end_year = 2017
    base_url = 'https://books.google.com/ngrams/graph?content={query}&year_start={start_year}&year_end={end_year}&corpus=15&smoothing=3'
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    try:
        query = '+'.join(word.split())
        url = base_url.format(
            query=query, start_year=start_year, end_year=end_year
        )
        soup = get_soup(url, header)
        for a in re.findall('var data = (.*?);\\n', str(soup)):
            # setup df
            data = {'value': x['timeseries'] for x in literal_eval(a)}
            df = pd.DataFrame(data)
            df.insert(0, 'year', list(xrange(start_year, start_year + len(df))))

            # build chart
            plt.rcParams['font.family'] = 'AvenirNextLTW01RegularRegular'
            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches(6.5, 4)
            for spine in ax.spines.itervalues():
                spine.set_visible(False)
            ax.plot(df['year'], df['value'], linewidth=2, color='#5DADE2')
            ax.set_ylim([0, (df['value'].mean() * 2)])
            ax.set_xlim([start_year, start_year + len(df)])
            ax.set_yticks(ax.get_yticks()[::2])
            ax.set_xticks(ax.get_xticks()[::4])
            fmt = '%s%%'
            ax.yaxis.set_major_formatter(FormatStrFormatter(fmt))
            ax.text(
                df['year'].mean(),
                (df['value'].mean() * 1.85),
                word,
                ha='center',
                fontsize=20
            )
            file_name = '{}{}_frequency.png'.format(directory, word)
            fig.savefig(file_name)

            return image_html(file_name)
    except Exception as e:
        # print e
        # print word
        pass
    return ''


def find_image(word, directory):
    # config
    base_url = 'https://www.google.co.in/search?q={query}&source=lnms&tbm=isch'
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    query = '+'.join(word.split())
    url = base_url.format(query=query)
    soup = get_soup(url, header)
    images = []

    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, file_type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        images.append((link, file_type))

    success = False
    count = 0
    while not success and count < 10:
        (img, file_type) = images[count]
        try:
            req = urllib2.Request(img, headers={'User-Agent': header})
            raw_img = urllib2.urlopen(req).read()

            file_type = 'jpg' if len(file_type) == 0 else file_type
            file_name = '{}{}_image.{}'.format(directory, word, file_type)

            f = open(file_name, 'wb')

            f.write(raw_img)
            f.close()
            success = True
        except Exception as e:
            # print "could not load : " + img
            # print e
            pass
        count += 1
    if success and file_name:
        return image_html(file_name)

    return ''
