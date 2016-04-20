#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/Users/dwhitehead/Documents/github/utils/')
import credentials
import requests
import pprint
from bs4 import BeautifulSoup
from collections import defaultdict
import ujson as json
import argparse
import io


def formatter(text):
	# removing vi
	text = text.replace('<vi>', '<')
	text = text.replace('</vi>', '>')
	# formatting author
	text = text.replace('<aq>', '-- ')
	text = text.replace('</aq>', '')
	# formatting italics
	text = text.replace('<it>', '<i>')
	text = text.replace('</it>', '</i>')
	# removing fw
	text = text.replace('<fw>', '')
	text = text.replace('</fw>', '')

	return text


def parse_soup(soup):
	entry_list = soup.find_all('entry')
	words = {}

	for idx, entry in enumerate(entry_list):
		# initiate variables to fill in
		soup = entry
		pronunciations = []
		wavs = []
		definitions = defaultdict(dict)
		cur_verb_divider = ''
		cur_sense_number = ''
		cur_sense_letter = ''
		cur_sense_number_sub = ''
		cur_phrase = ''

		# actually format things from terrible api
		while soup is not None and soup.next_element not in entry_list:
			# logic
			if not soup.name:
				soup = soup.next_element
				continue
			elif soup.name == 'ew':
				word = soup.contents[0]
			elif soup.name == 'hw':
				syllables = soup.contents[0]
			elif soup.name == 'pr':
				pronunciations.append(unicode(soup.contents[0]).encode('utf-8'))
			elif soup.name == 'et':
				etymology = ''.join([formatter(unicode(x)) for x in soup.contents])
			elif soup.name == 'wav':
				wavs.append(soup.contents[0])
			elif soup.name == 'fl':
				functional_label = soup.contents[0]
			elif soup.name == 'date':
				date = soup.contents[0]
			elif soup.name == 'vt':
				# verb divider
				cur_verb_divider = soup.contents[0]
				cur_phrase = ''
				cur_sense_number = ''
				cur_sense_letter = ''
				definitions[cur_verb_divider] = {}
			elif soup.name == 'drp':
				# phrase
				cur_phrase = soup.contents[0]
				cur_verb_divider = ''
				cur_sense_number = ''
				cur_sense_letter = ''
				definitions[cur_phrase] = {}
			elif soup.name == 'sn':
				cur_sense = soup.contents[0]
				if ' ' in cur_sense:
					try:
						int(soup.contents[0].split(' ')[0])
						cur_sense_number = soup.contents[0].split(' ')[0]
						cur_sense_letter = soup.contents[0].split(' ')[1]
					except:
						cur_sense_letter = soup.contents[0].split(' ')[0]
				else:
					if '<snp>' in unicode(soup.contents[0]):
						pass
					else:
						cur_sense_letter = soup.contents[0]
			elif soup.name == 'snp':
				cur_sense_number_sub = soup.contents[0]
			elif soup.name == 'dt':
				defining_text = ''.join([formatter(unicode(x)) for x in soup.contents])
				# verb divider
				if cur_verb_divider:
					if definitions.get(':'.join([cur_verb_divider, cur_sense_number, cur_sense_letter, cur_sense_number_sub])):
						definitions[
							':'.join([cur_verb_divider, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'defining_text': defining_text})
					else:
						definitions[
							':'.join([cur_verb_divider, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'defining_text': defining_text})
				# phrase
				elif cur_phrase:
					if definitions.get(':'.join([cur_phrase, cur_sense_number, cur_sense_letter, cur_sense_number_sub])):
						definitions[
							':'.join([cur_phrase, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'defining_text': defining_text})
					else:
						definitions[
							':'.join([cur_phrase, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'defining_text': defining_text})
				# else
				else:
					definitions.update({'defining_text': defining_text})
				cur_sense_number_sub = '(1)'
			elif soup.name == 'vi':
				verbal_illustration = ''.join([formatter(unicode(x)) for x in soup.contents])
				# verb divider
				if cur_verb_divider:
					if definitions.get(':'.join([cur_verb_divider, cur_sense_number, cur_sense_letter, cur_sense_number_sub])):
						definitions[
							':'.join([cur_verb_divider, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'verbal_illustration': verbal_illustration})
					else:
						definitions[
							':'.join([cur_verb_divider, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'verbal_illustration': verbal_illustration})
				# phrase
				elif cur_phrase:
					if definitions.get(':'.join([cur_phrase, cur_sense_number, cur_sense_letter, cur_sense_number_sub])):
						definitions[
							':'.join([cur_phrase, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'verbal_illustration': verbal_illustration})
					else:
						definitions[
							':'.join([cur_phrase, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'verbal_illustration': verbal_illustration})
				# else
				else:
					definitions.update({'verbal_illustration': verbal_illustration})
				cur_sense_number_sub = '(1)'
			elif soup.name == 'sx':
				synonym = ''.join([formatter(unicode(x)) for x in soup.contents])
				# verb divider
				if cur_verb_divider:
					if definitions.get(':'.join([cur_verb_divider, cur_sense_number, cur_sense_letter, cur_sense_number_sub])):
						definitions[
							':'.join([cur_verb_divider, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'synonym': synonym})
					else:
						definitions[
							':'.join([cur_verb_divider, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'synonym': synonym})
				# phrase
				elif cur_phrase:
					if definitions.get(':'.join([cur_phrase, cur_sense_number, cur_sense_letter, cur_sense_number_sub])):
						definitions[
							':'.join([cur_phrase, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'synonym': synonym})
					else:
						definitions[
							':'.join([cur_phrase, cur_sense_number, cur_sense_letter, cur_sense_number_sub])
						].update({'synonym': synonym})
				# else
				else:
					definitions.update({'synonym': synonym})
				cur_sense_number_sub = '(1)'
			soup = soup.next_element

		# words[word + str(idx)] = {
		words[word] = {
			'word': word,
			'syllables': formatter(syllables),
			'pronunciations': pronunciations,
			'wavs': wavs,
			'functional_label': formatter(functional_label),
			'definitions': dict(definitions),
			'date': formatter(date),
			'etymology': etymology,
		}
		# .encode('utf-8')
		break
	return words


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--query', type=str, help='query to hit api with')
	query = parser.parse_args().query
	dictionaryapi = credentials.read_cfg(
		credentials.find_pass_cfg(),
		'dictionaryapi'
	)
	dictionary_url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{}'
	r = requests.get(
		dictionary_url.format(query),
		params={'key': dictionaryapi['dictionary']}
	)
	soup = BeautifulSoup(r.content, 'xml')
	words = parse_soup(soup)

	for word, values in words.iteritems():
		print values
		print json.dumps(values.get('definitions', ''))
		print '{}\t{}\t{}\t{}\t{}\t{}\t{}\t'.format(
			values.get('word', ''),
			values.get('pronunciations', [''])[0],
			values.get('syllables', ''),
			values.get('functional_label', ''),
			values.get('date', ''),
			values.get('etymology', '').encode('utf-8'),
			json.dumps(values.get('definitions', '')).encode('utf-8')
		)
		print '{}\t'.format(
			values.get('definitions', '').encode('utf-8')
		)
		x = '\t'.join([
			values.get('word', ''),
			values.get('pronunciations', [''])[0],
			values.get('syllables', ''),
			values.get('functional_label', ''),
			values.get('date', ''),
			values.get('etymology', ''),
			values.get('definitions', '')
		])
		print x
		f = io.open('{}.txt'.format(word), 'w', encoding='utf-8')
		f.write(
		)


if __name__ == '__main__':
	main()
