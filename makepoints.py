import re
import json
import time

t0 = time.time()

with open('Data/count.json', 'r') as f:
	words = json.loads(f.read())

word_list = [word for word in words]
n = len(word_list)

print("Word list loaded")
print("Time lapsed : "+str(time.time()-t0))

re_pattern = re.compile(r"^[a-zA-Z]+$")

for i in range(n):
	word_list[i] = word_list[i].lower()
word_list = list(set(word_list))
n = len(word_list)
print("Unique words found : "+str(n))
print("Time lapsed : "+str(time.time()-t0))

nodes = []
for i in range(n):
	word = word_list[i]
	if re.match(re_pattern,word):
		obj = {}
		obj['word'] = word
		obj['word_len'] = len(word)
		for c in word:
			if c.isalpha():
				if c in obj:
					obj[c] += 1
				else:
					obj[c] = 1
		# for c in ascii_lowercase:
		# 	obj[c] = 0
		# for c in word:
		# 	if c.isalpha():
		# 		obj[c] = 1
		nodes.append(obj)
print("Nodes made")
print("Time lapsed : "+str(time.time()-t0))

with open('Data/nodes.json', 'w') as f:
	json.dump(nodes,f)
with open('Data/nodes_indented.json', 'w') as f:
	json.dump(nodes,f,indent=4)
print("Nodes saved in file")
print("Time lapsed : "+str(time.time()-t0))