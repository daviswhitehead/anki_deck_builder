#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/Users/dwhitehead/Documents/github/utils/')
import credentials
import requests
import pprint
from bs4 import BeautifulSoup
from collections import defaultdict


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

def main():
	query = 'read'
	dictionaryapi = credentials.read_cfg(
		credentials.find_pass_cfg(),
		'dictionaryapi'
	)
	dictionary_url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{}'
	r = requests.get(
		dictionary_url.format(query),
		params={'key': dictionaryapi['dictionary']}
	)
	print 'r', r
	print 'r.content', r.content

	soup = BeautifulSoup(r.content, 'xml')
	# print soup.prettify()
	entry_list = soup.find_all('entry')
	words = {}
	print
	print

	for idx, entry in enumerate(entry_list):

		# initiate variables to fill in
		soup = entry
		pronunciations = []
		wavs = []
		definitions = {}
		cur_verb_divider = None
		cur_sense_number = None
		cur_sense_letter = None
		cur_sense_number_sub = None
		cur_phrase = None

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
				pronunciations.append(unicode(soup.contents[0]))
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
				cur_sense_number = None
				cur_sense_number_sub = None
				definitions[cur_verb_divider] = {}
			elif soup.name == 'drp':
				# phrase
				cur_phrase = soup.contents[0]
				definitions[cur_phrase] = {}
				cur_verb_divider = None
				cur_sense_number = None
				cur_sense_number_sub = None
			elif soup.name == 'sn':
				cur_sense = soup.contents[0]
				### TO DO ####
				# Make this into regex
				if ' ' in cur_sense:
					cur_sense_number = soup.contents[0].split(' ')[0]
					cur_sense_letter = soup.contents[0].split(' ')[1]
				else:
					cur_sense_letter = soup.contents[0]
				# if len(soup.contents) > 1:
					# cur_sense_number = soup.contents[0]
				# else:
					# print soup.contents
					# soup = soup.next_element
					# continue
				cur_sense_number_sub = None
				if cur_verb_divider:
					definitions[cur_verb_divider][cur_sense_number][cur_sense_letter] = {}
				elif cur_phrase:
					definitions[cur_phrase][cur_sense_number][cur_sense_letter] = {}
				else:
					definitions[cur_sense_number][cur_sense_letter] = {}
			elif soup.name == 'snp':
				cur_sense_number_sub = soup.contents[0]
				if cur_verb_divider and cur_sense_number and cur_sense_letter:
					definitions[cur_verb_divider][cur_sense_number][cur_sense_letter][cur_sense_number_sub] = {}
				elif cur_phrase and cur_sense_number and cur_sense_letter:
					definitions[cur_phrase][cur_sense_number][cur_sense_letter][cur_sense_number_sub] = {}
				elif cur_sense_number and cur_sense_letter:
					definitions[cur_sense_number][cur_sense_letter][cur_sense_number_sub] = {}
				else:
					definitions[cur_sense_number_sub] = {}
			elif soup.name == 'dt':
				defining_text = ''.join([formatter(unicode(x)) for x in soup.contents])
				# verb divider
				if cur_verb_divider and cur_sense_number and cur_sense_number_sub:
					definitions[cur_verb_divider][cur_sense_number][cur_sense_number_sub].update({'defining_text': defining_text})
				elif cur_verb_divider and cur_sense_number:
					definitions[cur_verb_divider][cur_sense_number].update({'defining_text': defining_text})
				elif cur_verb_divider:
					definitions[cur_verb_divider].update({'defining_text': defining_text})
				# phrase
				elif cur_phrase and cur_sense_number and cur_sense_number_sub:
					definitions[cur_phrase][cur_sense_number][cur_sense_number_sub].update({'defining_text': defining_text})
				elif cur_phrase and cur_sense_number:
					definitions[cur_phrase][cur_sense_number].update({'defining_text': defining_text})
				elif cur_phrase:
					definitions[cur_phrase].update({'defining_text': defining_text})
				# sense number
				elif cur_sense_number and cur_sense_number_sub:
					definitions[cur_sense_number][cur_sense_number_sub].update({'defining_text': defining_text})
				elif cur_sense_number:
					definitions[cur_sense_number].update({'defining_text': defining_text})
				elif cur_sense_number_sub:
					definitions[cur_sense_number_sub].update({'defining_text': defining_text})
				# else
				else:
					definitions.update({'defining_text': defining_text})
			elif soup.name == 'vi':
				verbal_illustration = ''.join([formatter(unicode(x)) for x in soup.contents])
				# verb divider
				if cur_verb_divider and cur_sense_number and cur_sense_number_sub:
					definitions[cur_verb_divider][cur_sense_number][cur_sense_number_sub].update({'verbal_illustration': verbal_illustration})
				elif cur_verb_divider and cur_sense_number:
					definitions[cur_verb_divider][cur_sense_number].update({'verbal_illustration': verbal_illustration})
				elif cur_verb_divider:
					definitions[cur_verb_divider].update({'verbal_illustration': verbal_illustration})
				# phrase
				elif cur_phrase and cur_sense_number and cur_sense_number_sub:
					definitions[cur_phrase][cur_sense_number][cur_sense_number_sub].update({'verbal_illustration': verbal_illustration})
				elif cur_phrase and cur_sense_number:
					definitions[cur_phrase][cur_sense_number].update({'verbal_illustration': verbal_illustration})
				elif cur_phrase:
					definitions[cur_phrase].update({'verbal_illustration': verbal_illustration})
				# sense number
				elif cur_sense_number and cur_sense_number_sub:
					definitions[cur_sense_number][cur_sense_number_sub].update({'verbal_illustration': verbal_illustration})
				elif cur_sense_number:
					definitions[cur_sense_number].update({'verbal_illustration': verbal_illustration})
				elif cur_sense_number_sub:
					definitions[cur_sense_number_sub].update({'verbal_illustration': verbal_illustration})
				# else
				else:
					definitions.update({'verbal_illustration': verbal_illustration})
			elif soup.name == 'sx':
				synonym = ''.join([formatter(unicode(x)) for x in soup.contents])
				# verb divider
				if cur_verb_divider and cur_sense_number and cur_sense_number_sub:
					definitions[cur_verb_divider][cur_sense_number][cur_sense_number_sub].update({'synonym': synonym})
				elif cur_verb_divider and cur_sense_number:
					definitions[cur_verb_divider][cur_sense_number].update({'synonym': synonym})
				elif cur_verb_divider:
					definitions[cur_verb_divider].update({'synonym': synonym})
				# phrase
				elif cur_phrase and cur_sense_number and cur_sense_number_sub:
					definitions[cur_phrase][cur_sense_number][cur_sense_number_sub].update({'synonym': synonym})
				elif cur_phrase and cur_sense_number:
					definitions[cur_phrase][cur_sense_number].update({'synonym': synonym})
				elif cur_phrase:
					definitions[cur_phrase].update({'synonym': synonym})
				# sense number
				elif cur_sense_number and cur_sense_number_sub:
					definitions[cur_sense_number][cur_sense_number_sub].update({'synonym': synonym})
				elif cur_sense_number:
					definitions[cur_sense_number].update({'synonym': synonym})
				elif cur_sense_number_sub:
					definitions[cur_sense_number_sub].update({'synonym': synonym})
				# else
				else:
					definitions.update({'synonym': synonym})
			soup = soup.next_element

		words[word + str(idx)] = {
			'word': word,
			'syllables': formatter(syllables),
			'pronunciations': pronunciations,
			'wavs': wavs,
			'functional_label': formatter(functional_label),
			'definitions': definitions,
			'date': formatter(date),
			'etymology': etymology,
		}
		# pprint.pprint(entry.vi.__dict__)

	pprint.pprint(words)

	for word, values in words.iteritems():
		print '\n'*2
		print word
		pprint.pprint(values)

	# f = open('test.txt', 'w')
	# f.write(words['testing']['pronunciation'].encode('utf-8'))


if __name__ == '__main__':
	main()
