import cnn
import time
import Search
from threading import Thread

def update(article_database, content_database):
	search_update_thread = Thread(target=Search.update_dict)
	search_update_thread.daemon = True
	search_update_thread.start()
	while 1:
		cnn.update(article_database, content_database)
		time.sleep(300)