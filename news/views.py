from django.shortcuts import render
from news.models import Article, Content
import threading
import scraping

scrape_thread = threading.Thread(target=scraping.update, args = (Article, Content))

scrape_thread.daemon = True
scrape_thread.start()

def search(query):
	return scraping.search(query)


def index(req):
	return "Hi"