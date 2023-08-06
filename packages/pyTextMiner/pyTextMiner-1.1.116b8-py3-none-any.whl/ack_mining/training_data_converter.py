import pandas as pd

data = pd.read_csv("./10893_sents_shuffled.csv", encoding='latin-1').sample(frac=1).drop_duplicates()
data = data[['LABEL', 'TEXT']].rename(columns={"LABEL": "label", "TEXT": "text"})

data['label'] = '__label__' + data['label'].astype(str)
data.iloc[0:int(len(data) * 0.8)].to_csv('train.csv', sep='\t', index=False, header=False)
data.iloc[int(len(data) * 0.8):int(len(data) * 0.9)].to_csv('test.csv', sep='\t', index=False, header=False)
data.iloc[int(len(data) * 0.9):].to_csv('dev.csv', sep='\t', index=False, header=False);