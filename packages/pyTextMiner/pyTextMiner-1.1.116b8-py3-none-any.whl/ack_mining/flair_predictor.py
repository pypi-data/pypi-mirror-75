from flair.models import TextClassifier
from flair.data import Sentence

classification_results = open("classification_results.txt", "w")
classifier = TextClassifier.load('./best-model.pt')
filepath = './random500.txt'
with open(filepath) as fp:
    for line in fp:
        #print("Line {}: {}".format(cnt, line.strip()))
        lines = line.split('\t')
        if len(lines) > 2:
            sentence = Sentence(lines[2])
            classifier.predict(sentence)
            print(str(sentence.labels) + "\t" + lines[2])
            classification_results.write(str(sentence.labels) + "\t" + str(lines) + "\n")

fp.close()
classification_results.close()