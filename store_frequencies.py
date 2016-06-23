import re
import json
from nltk.corpus import movie_reviews

file_name = "Data/count.json"
indented_file_name = "Data/count_indented.json"

word_list = movie_reviews.words()
n = len(word_list)
print("Word list fetched")

d = {}
for i in range(n):
	word = word_list[i].lower()
	re_pattern = r"^[a-z]+$"
	if re.match(re_pattern,word):
		if word in d:
			d[word] += 1
		else:
			d[word] = 1
print("Count done")

with open(file_name, 'w') as f:
	json.dump(d,f)
with open(indented_file_name, 'w') as f:
	json.dump(d,f,indent=4)
print("Result stored in file")