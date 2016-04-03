import cnn
import time

def update(database):
	while 1:
		cnn.update(database)
		time.sleep(300)