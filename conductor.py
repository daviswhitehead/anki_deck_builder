import sys
sys.path.append('/Users/dwhitehead/Documents/github/utils/')
import credentials
from bing_test import BingSearchAPI


if __name__ == "__main__":
	bing_credentials = credentials.read_cfg(
		credentials.find_pass_cfg(),
		'bing'
	)

	query_string = "chicanery"
	bing = BingSearchAPI(bing_credentials['primary_account_key'])
	params = {
		'$format': 'json',
		'$top': 10,
		'$skip': 0
	}
	# print bing.search('image+web', query_string, params).json()
	test = bing.search('image', query_string, params).json()
	for result in test.get('d', {}).get('results', {})[0].get('Image', {}):
		print '\n', result, '\n'
	# pprint.pprint(test)
