import requests
import re

FILE_NAME = 'database.db'
URL_POSITION = 0

ARTICLE_PATTERN = r"<url>.*?<loc>(.*?)</loc>.*?<lastmod>(.*?)</lastmod>"
BODY_PATTERN = r'''<div class="zn-body__paragraph">(.*?)</div>'''
IMAGE_PATTERN = r"""<meta itemprop="image" content="(.*?)">"""

TITLE_PATTERN =  r"""<head>.*?<title>(.*?)</title>"""

SITEMAP_PATTERN = r"<sitemap>.*?<loc>(.*?)</loc>"

def add_to_database(article, database):
	try:
		database.objects.get(url = article[URL_POSITION])
	except:
		html = requests.get(article[URL_POSITION]).text
		body = ""
		for part_of_article in re.findall(BODY_PATTERN, html, re.DOTALL):
			body += part_of_article
		image = re.search(IMAGE_PATTERN, html, re.DOTALL)
		if image:
			image = image.group(0)
		else:
			image = None

		title = re.search(TITLE_PATTERN, html, re.DOTALL)
		if title:
			title = title.group(1)
		else:
			title = 'No title'	
		print title
		database.objects.create(url = article[URL_POSITION], title = title, body = body, image = image).save()

def get_current_article_list():
	return re.findall(SITEMAP_PATTERN, requests.get("http://www.cnn.com/sitemaps/sitemap-index.xml").text, re.DOTALL)

def update(database):
	to_scrape = get_current_article_list()
	print to_scrape
	for list_of_articles in to_scrape:
		articles = re.findall(ARTICLE_PATTERN, requests.get(list_of_articles).text, re.DOTALL)
		print articles
		for article in articles:
			print "Scraping article"
			add_to_database(article, database)
