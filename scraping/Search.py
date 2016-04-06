search_dict = {}

def combine_matches(d1, d2):
	for key, matches in d1:
		for match in matches:
			d2[key].append(matches)
	return d2


def find_matches(query, content):
	matches = {}
	for i in xrange(1, len(query)):
		if ' '.join(query[:i]) in content.phrase:
			matches[len(query) - i].append(query[:i])
	if len(query) == 1:
		return matches
	else:
		return combine_matches(matches, find_matches(query[1:], content))


def search(query, words_database):
	query = query.lower()
	global search_dict
	if query in search_dict:
		return search_dict[query]
	matches = {}

	# Number of words excluded is the key

	for i in xrange(len(query.split())):
		matches[i] = []
	for content in words_database.objects.all():
		if query in content.phrase:
			matches[0].append(content)
		matches = combine_matches(find_matches(query.split(), content), matches)
	search_dict[query] = matches
	return matches

def update_dict():
	for query in search_dict:
		search_dict[query] = search(query)