from transformers import BertModel, BertForSequenceClassification
from torch import nn, optim
import torch
import os

class PYBERTClassifier(nn.Module):
    '''
     Customized BERT Sequence Model
    '''
    def __init__(self, n_classes, model_name):
        #PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
        super(PYBERTClassifier, self).__init__()
        if 'etri' in model_name or 'mecab' in model_name:
            self.bert = BertModel.from_pretrained(os.path.abspath('pytorch_model.bin'),
                                  output_hidden_states = False)
        else:
            self.bert = BertModel.from_pretrained(model_name)
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

    def forward(self, input_ids, attention_mask):
        _, pooled_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        output = self.drop(pooled_output)
        return self.out(output)


class PYBERTClassifierGenAtten(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size=768,
                 num_classes=2,
                 dr_rate=None,
                 params=None):
        super(PYBERTClassifierGenAtten, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size, num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids=token_ids, token_type_ids=segment_ids.long(),
                              attention_mask=attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)

class PYBertForSequenceClassification:
    '''
        Use pytorch's BERTForSeqeunceClassification
        Bert Model transformer with a sequence classification/regression head on top (a linear layer on top of the pooled output) e.g. for GLUE tasks.
        labels (torch.LongTensor of shape (batch_size,), optional, defaults to None)
        – Labels for computing the sequence classification/regression loss. Indices should be in [0, ..., config.num_labels - 1]. If config.num_labels == 1 a regression loss is computed (Mean-Square loss),
        If config.num_labels > 1 a classification loss is computed (Cross-Entropy).
    '''
    def __init__(self, n_classes, model_name):
        self.model = BertForSequenceClassification.from_pretrained(
                                    model_name,  # Use the 12-layer BERT model, with an uncased vocab.
                                    num_labels=n_classes,  # The number of output labels--2 for binary classification.
                                    # You can increase this for multi-class tasks.
                                    output_attentions=False,  # Whether the model returns attentions weights.
                                    output_hidden_states=False,  # Whether the model returns all hidden-states.
                                )
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(device)

    def __call__(self, *args, **kwargs):
        return self.model