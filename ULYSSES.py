import requests
from collections import Counter
import re

def chapterone(html):

    pattern = re.compile(r'<a id="chap01"></a>(.*?)<a id="chap02"></a>', re.DOTALL | re.IGNORECASE)
    match = pattern.search(html)

    chapter_html = match.group(1)

    text = re.sub(r'<[^>]+>', ' ', chapter_html)

    text = re.sub(r'\s+', ' ', text).strip()

    return text

def split_into_sentences(text):
    sentence_end_re = re.compile(r'([.!?])\s+')
    sentences = []
    start = 0
    for m in sentence_end_re.finditer(text):
        end = m.end()
        sentences.append(text[start:end].strip())
        start = end
    last = text[start:].strip()
    if last:
        sentences.append(last)
    return sentences

def split_into_words(text):
    return re.findall(r'\b\w+\b', text.lower())

def count_word_frequencies(text):
    words = split_into_words(text)
    return Counter(words)

def find_word_contexts_regex(text, word, left, right, cut_length=False, filename='contexts.txt'):
    word = word.lower()
    results = []

    if cut_length:
        sentences = split_into_sentences(text)
        for sent in sentences:
            tokens = split_into_words(sent)
            for i, token in enumerate(tokens):
                if token == word:
                    left_context = tokens[max(0, i-left):i]
                    right_context = tokens[i+1:i+1+right]
                    fragment = ' '.join(left_context + [tokens[i]] + right_context)
                    results.append(fragment)
    else:
        tokens = split_into_words(text)
        for i, token in enumerate(tokens):
            if token == word:
                left_context = tokens[max(0, i-left):i]
                right_context = tokens[i+1:i+1+right]
                fragment = ' '.join(left_context + [tokens[i]] + right_context)
                results.append(fragment)

    with open(filename, 'w', encoding='utf-8') as f:
        for fragment in results:
            print(fragment)
            f.write(fragment + '\n')


url = 'https://www.gutenberg.org/files/4300/4300-h/4300-h.htm'
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

text = chapterone(html)

freqs = count_word_frequencies(text)
print('10 самых частых слов:', freqs.most_common(10))

find_word_contexts_regex(text, word='stephen', left=3, right=3, cut_length=True, filename='stephen.txt')
