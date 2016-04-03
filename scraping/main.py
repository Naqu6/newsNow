import cnn
import time

def update(article_database, content_database):
	while 1:
		cnn.update(article_database, content_database)
		time.sleep(300)