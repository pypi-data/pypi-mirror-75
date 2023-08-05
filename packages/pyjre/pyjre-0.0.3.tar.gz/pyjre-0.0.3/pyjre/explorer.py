import requests
from bs4 import BeautifulSoup as bsoup
from pprint import pprint


class Explorer:
	SEARCH_BASE = "http://podcasts.joerogan.net/wp-admin/admin-ajax.php"
	HOME_BASE = "http://podcasts.joerogan.net/"
	HEADERS = {
		"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"Accept-Encoding" : "gzip, deflate",
		"Accept-Language" : "en-US,en;q=0.9",
		"Host" : "podcasts.joerogan.net",
		"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
		"Origin" : "http://podcasts.joerogan.net",
	}
	SESSION = requests.session()
	
	@classmethod
	def latest_podcasts(cls):
		'''
			Get the latest podcasts.
		'''
		url = cls.HOME_BASE
		headers = cls.HEADERS
		headers['Referer'] =  "http://podcasts.joerogan.net/"
		response = cls.SESSION.get(url, headers=headers)
		classes_to_look_for = [
			'podcast-thumb',
			'podcast-date',
			'episode-num',
			'podcast-content',
			'podcast-links'
		]

		if response.status_code == 200:
			soup = bsoup(response.text, 'html.parser')
			eles = soup.find_all(attrs = {'class' : classes_to_look_for})
			collection = []
			for index, ele in enumerate(eles):
				try:
					if (index + 1) % 5 == 1:
						data = {}
						data['link'] = ele.find('a')['href']
						data['thumbnail'] = ele.find('img')['src']
					elif (index + 1) % 5 == 2:
						data['data'] = ele.find('h3').text
					elif (index + 1) % 5 == 3:
						data['episode-number'] = ele.text
					elif (index + 1) % 5 == 4:
						data['title'] = ele.find('strong').text
						data['excerpt'] = ele.find('p').text
					else:
						data['related-links'] = [a['href'] for a in ele.find('ul').find_all('a')]
						collection.append(data)

				except Exception as err:
					pass
			return {"success" : True, "data" : {"total" : len(collection), "search_results" : collection}}
		return {"success" : False}

	@classmethod
	def search(cls, keyword: str):
		'''
			Search for podcasts.
		'''
		url = cls.SEARCH_BASE 
		headers = cls.HEADERS
		headers['Referer'] =  "http://podcasts.joerogan.net/?search=" + keyword
		response = cls.SESSION.post(url, headers=headers, data={"search-terms" : keyword, "action" : "search_podcasts"})
		classes_to_look_for = [
			'podcast-thumb',
			'podcast-date',
			'episode-num',
			'podcast-content',
			'podcast-links'
		]
		if response.status_code == 200:
			soup = bsoup(response.json()['response'], 'html.parser')
			eles = soup.find_all(attrs = {'class' : classes_to_look_for})
			collection = []
			for index, ele in enumerate(eles):
				try:
					if (index + 1) % 5 == 1:
						data = {}
						data['link'] = ele.find('a')['href']
						data['thumbnail'] = ele.find('img')['src']
					elif (index + 1) % 5 == 2:
						data['data'] = ele.find('h3').text
					elif (index + 1) % 5 == 3:
						data['episode-number'] = ele.text
					elif (index + 1) % 5 == 4:
						data['title'] = ele.find('strong').text
						data['excerpt'] = ele.find('p').text
					else:
						data['related-links'] = [a['href'] for a in ele.find('ul').find_all('a')]
						collection.append(data)
						
				except Exception as err:
					pass
			return {"success" : True, "data" : {"total" : len(collection), "search_results" : collection}}
		return {"success" : False}

