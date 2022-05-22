import random
import requests

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.decode().splitlines()
N_FILES = 10
N_WORDS = 10000000
text = ""

for i in range(N_FILES):
    for j in range(N_WORDS):
        text += ' ' + random.choice(WORDS)
    with open('files/text{}.txt'.format(i), 'w') as file:
        file.write(text)
    text = ""
