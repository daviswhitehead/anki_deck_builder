import sys
sys.path.append('/Users/dwhitehead/Documents/github/utils/')
import credentials
from pyBingSearchAPI.bing_search_api import BingSearchAPI
import subprocess
import requests
import shutil

'''
Outline:

1) list of words
2) get data on words
	- definitions from wordnet
	- image from bing
	- trend from google books
	- collocations?
	- other
3) combine words into flash cards

'''


def get_bing_image(bing, query):
	'Imaging...'
	params = {
		'$format': 'json',
		'$top': 10,
		'$skip': 0
	}
	search_result = bing.search('image', query, params).json()
	top_image = search_result.get('d', {}).get('results', {})[0].get('Image', {})[0].get('MediaUrl')
	if top_image:
		response = requests.get(top_image, stream=True)
		with open('data/{}/{}_image.png'.format(query, query), 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
			del response
	'done.'


def create_word_chart(query):
	print 'Charting...'
	ngram_args = [
		'python',
		'google-ngrams/getngrams.py',
		query,
		'-plot',
		'-noprint',
		'-caseInsensitive',
		'-endYear=2008'
	]
	subprocess.call(ngram_args)
	print 'done.'


def get_word_definition(query):
	r = requests.get('http://wordnetweb.princeton.edu/perl/webwn?s={}'.format(query))
	print r.text


def main():
	# load credentials
	# dictionaryapi = credentials.read_cfg(
		# credentials.find_pass_cfg(),
		# 'dictionaryapi'
	# )
	bing_credentials = credentials.read_cfg(
		credentials.find_pass_cfg(),
		'bing'
	)

	f = open('words.txt', 'r')
	wordlist = [x.strip('\n') for x in f.readlines()]

	for word in wordlist:
		print 'Word: {}'.format(word)

		subprocess.call(['mkdir', 'data/{}'.format(word)])

		# creates a chart of a word's usage overtime
		# word.png
		create_word_chart(word)

		# download the first image associated with a word
		bing = BingSearchAPI(bing_credentials['primary_account_key'])
		get_bing_image(bing, word)

		print 'done: {}'.format(word)
		print


if __name__ == "__main__":
	main()
