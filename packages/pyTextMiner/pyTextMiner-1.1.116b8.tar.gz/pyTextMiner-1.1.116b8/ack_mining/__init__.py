from flair.data import Sentence
from flair.models import SequenceTagger
import re

# load the NER tagger
tagger = SequenceTagger.load('ner')

ner_results = open("ner_results.txt", "w")
#D:\\workspace\\PKDE4J2.0\\ack_filtered_results.txt
filepath = 'D:\\workspace\\PKDE4J2.0\\ack_filtered_results.txt'
with open(filepath) as fp:
    cnt = 1
    for line in fp:
        #print("Line {}: {}".format(cnt, line.strip()))
        fields=line.split('\t')
        pid=fields[0]
        sent=fields[1]
        cnt += 1
        if len(sent) > 0:
            sentence = Sentence(sent)
            tagger.predict(sentence)
            #print(sentence)
            # iterate over entities and print
            matched = ''
            for entity in sentence.get_spans('ner'):
                if entity.tag != 'MISC':
                    matched += entity.tag + ":" + entity.text + ":" + str(entity.start_pos) + "-" + str(entity.end_pos) + "\t"

            if (len(matched.strip('\t')) > 0):
                print(matched.strip('\t') + "\t" + sent)
                re.sub('\s+', ' ', matched)
                ner_results.write(matched.strip('\t') + "\t" + pid + ":" + sent + "\n")

    ner_results.close()