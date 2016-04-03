from django.shortcuts import render
from news.models import Article
import threading
import scraping

scrape_thread = threading.Thread(target=scraping.update, args = (Article,))

scrape_thread.daemon = True
scrape_thread.start()

def index(req):
	return "Hi"