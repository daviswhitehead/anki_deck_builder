import sys
sys.path.append('/Users/dwhitehead/Documents/github/utils/')
import credentials
from pyBingSearchAPI.bing_search_api import BingSearchAPI
import subprocess
import requests

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
	params = {
		'$format': 'json',
		'$top': 10,
		'$skip': 0
	}
	test = bing.search('image', query, params).json()
	for result in test.get('d', {}).get('results', {})[0].get('Image', {}):
		print '\n', result, '\n'


def create_word_chart(query):
	args = [
		'python',
		'google-ngrams/getngrams.py',
		query,
		'-plot',
		'-noprint',
		'-caseInsensitive',
		'-endYear=2008'
	]
	p = subprocess.call(args)


def get_word_definition(query):
	r = requests.get('http://wordnetweb.princeton.edu/perl/webwn?s={}'.format(query))
	print r.text


def main():
	# print get_word_definition('tribulations')
	create_word_chart('tribulations')

	sys.exit()
	dictionaryapi = credentials.read_cfg(
		credentials.find_pass_cfg(),
		'dictionaryapi'
	)

	bing_credentials = credentials.read_cfg(
		credentials.find_pass_cfg(),
		'bing'
	)
	bing = BingSearchAPI(bing_credentials['primary_account_key'])
	get_bing_image(bing, 'chicanery')
	create_word_chart('chicanery')


if __name__ == "__main__":
	main()
