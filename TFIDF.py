import math

class TFIDFCalculator:
    stopwords = set(['the', 'a', 'an', 'in', 'on', 'at', 'of', 'and', 'to', 'is'])

    def __init__(self, documents):
        self.documents = documents
        self.N = len(documents)

    def get_tf(self, word, doc_num):
        words = self.documents[doc_num].lower().split()
        word = word.lower()
        return words.count(word) / len(words)

    def get_idf(self, word):
        word = word.lower() 
        n_i = sum(1 for doc in self.documents if word in doc.lower().split())
        return math.log(self.N / (n_i + 1))

    def get_tf_idf(self, word, doc_num, ignore_stopwords=True):
        if ignore_stopwords and word.lower() in self.stopwords:
            return 0
        tf = self.get_tf(word, doc_num)
        idf = self.get_idf(word)
        return tf * idf

if __name__ == '__main__':
    documents = []
    n = int(input("количество строк "))
    for i in range(n):
        doc = input(f"строка {i + 1}: ")
        documents.append(doc)

    calculator = TFIDFCalculator(documents)

    word = input("слово для расчета TFIDF: ")
    doc_num = int(input("номер строки ")) - 1

    tf_idf = calculator.get_tf_idf(word, doc_num)
    print(f"TFIDF для слова '{word}' в строке {doc_num + 1}: {tf_idf}")