import requests
import re
import constants
import dateutil.parser

FILE_NAME = 'database.db'
URL_POSITION = 0
DATE_POSITION = 1

ARTICLE_PATTERN = r"<url>.*?<loc>(.*?)</loc>.*?<lastmod>(.*?)</lastmod>"
BODY_PATTERN = r'''<div class="zn-body__paragraph">(.*?)</div>'''
IMAGE_PATTERN = r"""<meta itemprop="image" content="(.*?)">"""

TITLE_PATTERN =  r"""<head>.*?<title>(.*?)</title>"""

SITEMAP_PATTERN = r"<sitemap>.*?<loc>(.*?)</loc>"

def add_to_database(article, article_database, content_database):
	try:
		article_database.objects.get(url = article[URL_POSITION])
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
		Article_Object = article_database.objects.create(url = article[URL_POSITION], title = title, body = body, image = image)
		Article_Object.save()

		body = body.lower()
		body = re.sub(r"<.*?>", '', body)
		for word in constants.EXCLUDED_WORDS:
			body = body.replace(word, chr(0))

		body = body.split(chr(0))
		for phrase in body:
			content_database.objects.create(phrase = phrase, article = Article_Object, date = dateutil.parser.parse(article[DATE_POSITION])).save()

def get_current_article_list():
	sitemaps = re.findall(SITEMAP_PATTERN, requests.get("http://www.cnn.com/sitemaps/sitemap-index.xml").text, re.DOTALL)
	return [sitemap for sitemap in sitemaps if "articles" in sitemap]

def update(article_database, content_database):
	to_scrape = get_current_article_list()
	print to_scrape
	for list_of_articles in to_scrape:
		articles = re.findall(ARTICLE_PATTERN, requests.get(list_of_articles).text, re.DOTALL)
		print articles
		for article in articles:
			add_to_database(article, article_database, content_database)
