# -*- coding: utf-8 -*-
"""Codeling NL2bash.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19dxu1lzsmTrSeZ4Y_8w9xvfyJfo8CRr6
"""

#Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
import string
from string import digits
import re
from sklearn.utils import shuffle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import LSTM, Input, Dense,Embedding, Concatenate, TimeDistributed
from tensorflow.keras.models import Model,load_model, model_from_json
from tensorflow.keras.utils import plot_model
from tensorflow.keras.preprocessing.text import one_hot, Tokenizer
from tensorflow.keras.callbacks import EarlyStopping
import pickle as pkl
import numpy as np
import json

from google.colab import drive
drive.mount('/content/drive')

path = "/content/drive/MyDrive/nl2bash-data.json"

df = pd.read_json(path)

with pd.option_context('display.max_colwidth',None):
  display(df.head(5))

import json
import re

with open(path) as f:
    data = json.load(f)

inputs = []
targets = []

# Define regular expressions for preprocessing
# Remove non-alphanumeric characters, except for spaces and hyphens
non_alpha = re.compile(r'[^a-zA-Z0-9\s\-]+')
# Replace multiple spaces and hyphens with a single space
multi_space = re.compile(r'[ \-]+')
# Remove leading/trailing spaces and convert to lowercase
clean_text = lambda text: text.strip().lower()

for key, value in data.items():
    # preprocess input
    input_text = key
    #input_text = non_alpha.sub('', input_text)  # remove non-alphanumeric characters
    input_text = multi_space.sub(' ', input_text)  # replace multiple spaces/hyphens
    input_text = clean_text(input_text)  # remove leading/trailing spaces and convert to lowercase
    inputs.append(input_text)

    # preprocess target
    target_text = value['cmd']
    #target_text = non_alpha.sub('', target_text)  # remove non-alphanumeric characters
    target_text = multi_space.sub(' ', target_text)  # replace multiple spaces/hyphens
    target_text = clean_text(target_text)  # remove leading/trailing spaces and convert to lowercase
    targets.append(target_text)

print('Number of examples:', len(inputs))

# Save preprocessed data to file
with open('inputs.txt', 'w') as f:
    f.write('\n'.join(inputs))

with open('targets.txt', 'w') as f:
    f.write('\n'.join(targets))

import json
import string
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower() # convert to lowercase
    #text = re.sub(r'\d+', '', text) # remove digits
    #text = text.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
    text = ' '.join([word for word in text.split() if word not in stop_words]) # remove stop words
    text = ' '.join([nltk.PorterStemmer().stem(word) for word in text.split()]) # stemming
    return text

with open(path ,'r') as f:
    data = json.load(f)

inputs = []
targets = []

for key in data.keys():
    input_text = preprocess_text(data[key]['invocation'])
    target_text = preprocess_text(data[key]['cmd'])
    inputs.append(input_text)
    targets.append(target_text)

print(inputs)
print(targets)

!pip install os
!pip install bashlint
!pip install tokenizer
import json
import random
import os
import bashlint
import tokenizer


def tokenize_eng(text):
    return tokenizer.ner_tokenizer(text)[0]   #tokenizer for english 

def tokenize_bash(text):
    return bash_tokenizer(text,  loose_constraints=True, arg_type_only=True)  #bash tokenizer 

#preprocess function 
def preprocess(data_dir, data_file):
    data = {}
    with open(os.path.join(data_dir,data_file)) as f:
        raw_data = json.load(f)
    for i in  range(1, len(raw_data.keys())+1):
        data[str(i)] = raw_data[str(i)]
        data[str(i)]['cmd'] = [raw_data[str(i)]['cmd']]

    rand_seed = 94726
    random.seed(rand_seed)
    train_data, test_data = {}, {}
    all_index = [i for i in range(1, len(data.keys())+1)]
    random.shuffle(all_index)
    for i in all_index[:int(len(all_index)*0.8)]:
        train_data[str(i)] = data[str(i)]
    for j in all_index[int(len(all_index)*0.8):]:
        test_data[str(j)] = data[str(j)]

    with open('src/data/train_data.json', 'w') as f:
        json.dump(train_data, f)
    with open('src/data/test_data.json', 'w') as f:
        json.dump(test_data, f)

    for split, data in zip(['train', 'test'],[train_data, test_data]):
        english_txt = []
        bash_txt = []
        for i in data:
            english_txt.append(data[i]['invocation'])
            bash_txt.append(data[i]['cmd'][0])

        processed_cmd = []
        processed_nl = []

        for cmd, nl in zip(bash_txt, english_txt):
            processed_cmd.append(' '.join(tokenize_bash(cmd)))
            processed_nl.append(' '.join(tokenize_eng(nl)))

        with open('{}/cmds_proccess_{}.txt'.format(data_dir, split), 'w') as outF:
            for line in processed_cmd:
                outF.write(line)
                outF.write("\n")

        with open('{}/invocations_proccess_{}.txt'.format(data_dir, split), 'w') as outF:
            for line in processed_nl:
                outF.write(line)
                outF.write("\n")
    print(train_data)
    print(test_data)
    # return command here (what are we returning)
    #call preprocess function; pass data directory and path

import json
from torchtext.legacy.data import Field, Dataset


#import Dataset

with open('/content/drive/MyDrive/train_data.json', 'r') as f:
    train_data = json.load(f)

# Load test data from JSON
with open('/content/drive/MyDrive/test_data.json', 'r') as f:
    test_data = json.load(f)

print(train_data)

SRC = Field(tokenize='spacy', tokenizer_language='en_core_web_sm', lower=True)
TRG = Field(tokenize='spacy', tokenizer_language='en_core_web_sm', lower=True)

# Create examples using the train and test JSON data
train_examples = []
for data in train_data.values():
    src = data["invocation"]
    trg = data["cmd"]
    #example = Example.fromlist([src, trg], fields=[('src', SRC), ('trg', TRG)])
    train_examples.append((src,trg))
print(train_examples)
test_examples = []
for data in test_data.values():
    src = data["invocation"]
    trg = data["cmd"]
    #example = Example.fromlist([src, trg], fields=[('src', SRC), ('trg', TRG)])
    test_examples.append((src,trg))
# Build vocabulary for the source and target fields
print(test_examples)
specials = ['<pad>', '<unk>', '<sos>', '<eos>']
SRC.build_vocab(train_examples, max_size=10000)
TRG.build_vocab(train_examples, max_size=10000)

# Create train and test datasets
train_dataset = Dataset(train_examples, fields=[('src', SRC), ('trg', TRG)])
test_dataset = Dataset(test_examples, fields=[('src', SRC), ('trg', TRG)])

for example in train_dataset:
    src = example[0]  # Access the 'src' field of the example
    trg = example[1]  # Access the 'trg' field of the example
    
    # Print the content of src and trg
    print("Source: ", src)
    print("Target: ", trg)

#ENCODER AND DECODER
import torch
import torch.nn as nn
import torch.optim as optim

class Encoder(nn.Module):
    def __init__(self, input_dim, emb_dim, hid_dim, n_layers, dropout):
        super().__init__()

        self.hid_dim = hid_dim
        self.n_layers = n_layers

        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.rnn = nn.LSTM(emb_dim, hid_dim, n_layers, dropout=dropout)
        self.dropout = nn.Dropout(dropout)

    def forward(self, src):
        embedded = self.dropout(self.embedding(src))
        outputs, (hidden, cell) = self.rnn(embedded)
        return hidden, cell


class Decoder(nn.Module):
    def __init__(self, output_dim, emb_dim, hid_dim, n_layers, dropout):
        super().__init__()

        self.output_dim = output_dim
        self.hid_dim = hid_dim
        self.n_layers = n_layers

        self.embedding = nn.Embedding(output_dim, emb_dim)
        self.rnn = nn.LSTM(emb_dim, hid_dim, n_layers, dropout=dropout)
        self.fc_out = nn.Linear(hid_dim, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input, hidden, cell):
        input = input.unsqueeze(0)
        embedded = self.dropout(self.embedding(input))
        output, (hidden, cell) = self.rnn(embedded, (hidden, cell))
        prediction = self.fc_out(output.squeeze(0))
        return prediction, hidden, cell


class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, device):
        super().__init__()

        self.encoder = encoder
        self.decoder = decoder
        self.device = device

        assert encoder.hid_dim == decoder.hid_dim, \
            "Hidden dimensions of encoder and decoder must be equal!"
        assert encoder.n_layers == decoder.n_layers, \
            "Encoder and decoder must have equal number of layers!"

   

    def forward(self, src, trg, teacher_forcing_ratio=0.5):
      batch_size = trg.shape[1]
      max_len = trg.shape[0]
      trg_vocab_size = self.decoder.output_dim

      outputs = torch.zeros(max_len, batch_size, trg_vocab_size).to(self.device)

      hidden, cell = self.encoder(src)

      input = trg[0, :]

      for t in range(1, max_len):
          output, hidden, cell = self.decoder(input, hidden, cell)
          outputs[t] = output
          teacher_force = torch.rand(1) < teacher_forcing_ratio
          top1 = output.argmax(1)
          input = trg[t] if teacher_force else top1
          input = input.unsqueeze(0)  # Convert input to tensor of shape (1, batch_size) for consistency

      return outputs

import itertools
import torch
import torchtext
import numpy as np


def complex_equation(x, y):
    # Perform complex mathematical operations
      result = (x**2 + y**3) / (np.sqrt(x + y) + np.exp(x * y)) - (np.sin(x) + np.cos(y))
      # Convert result to percentage
      result_percentage = result * 100
      return result_percentage

Call the function with specific input values
# Define hyperparameters to search
params = {
    'enc_emb_dim': [128, 256, 512],
    'dec_emb_dim': [128, 256, 512],
    'hid_dim': [256, 512, 1024],
    'n_layers': [1, 2, 3],
    'enc_dropout': [0.2, 0.5, 0.8],
    'dec_dropout': [0.2, 0.5, 0.8],
    'learning_rate': [1e-3, 1e-4, 1e-5],
}



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def string_to_tensor(string, vocab):
    # Tokenize the input string
    tokens = torchtext.data.utils.get_tokenizer('basic_english')(string)
    
    # Convert tokens to indices using the vocabulary
    indices = [vocab.stoi[token] for token in tokens]
    
    # Convert indices to a torch tensor
    tensor = torch.LongTensor(indices)
    
    return tensor.unsqueeze(0)
import torch

def accuracy(predictions, targets):
    # Convert predictions to class labels by taking the index of the highest value
    predicted_labels = torch.argmax(predictions, dim=1)
    
    # Compare predicted labels with target labels
    correct=0
    u=0
    for i in predicted_labels:
      if(i==targets[u]):
        correct=correct+1
      u=u+1
    
    
    # Calculate accuracy as ratio of correct predictions to total predictions
    accuracy = correct / len(targets)
    
    return accuracy
x,y = 3,3
result = complex_equation(x, y)

def train(model, iterator, optimizer, criterion, clip):
    # Set model to training mode
    model.train()

    # Initialize variables to keep track of loss and accuracy
    epoch_loss = 0
    epoch_acc = 0
    print(iterator)
    #Iterate over the data
    for batch in iterator:
        print("batch-->",batch)
        # Reset gradients
    # Extract src from the batch
        input = batch[0]  # Extract src from the batch
        target = batch[1][0]  # Extract trg from the batch as a string
        # print("inpuit",input)
        # print("target",target[0])

        #target_tensor = target_tensor.unsqueeze(1)  # Extract trg from the batch
        print("inputs-->",input)
       # print(in[])
        print("targets-->",target)
        src_vocab = torchtext.vocab.build_vocab_from_iterator([input.split()])
        trg_vocab = torchtext.vocab.build_vocab_from_iterator([target.split()])
        src_tensor = string_to_tensor(input, src_vocab)
        trg_tensor = string_to_tensor(target, trg_vocab)
        print(trg_tensor.size())
        print(src_tensor.size())

        # Forward pass
        predictions = model.forward(src_tensor, trg_tensor, teacher_forcing_ratio=0.5)
        print("predictions--->",predictions.size())
       # _, predicted_indices = torch.max(predictions.squeeze(0), dim=)

        # Clip gradients to prevent exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)

        # Update weights
        optimizer.step()

        # Update loss and accuracy
      #  epoch_loss += loss.item()
        epoch_acc += accuracy(predictions, targets)

    # Calculate average loss and accuracy for the epoch
    epoch_loss /= len(iterator)
    epoch_acc /= len(iterator)

    return epoch_loss, epoch_acc


# Define function to train and evaluate a model with given hyperparameters
def train_eval_model(enc_emb_dim, dec_emb_dim, hid_dim, n_layers, enc_dropout, dec_dropout, learning_rate):
    # Define model architecture
    enc = Encoder(len(SRC.vocab), enc_emb_dim, hid_dim, n_layers, enc_dropout)
    dec = Decoder(len(TRG.vocab), dec_emb_dim, hid_dim, n_layers, dec_dropout)
    model = Seq2Seq(enc, dec, device).to(device)

    # Define optimizer and loss function
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss(ignore_index=TRG.vocab.stoi[TRG.pad_token])

    # Train model
    train_loss, train_acc = train(model, train_dataset, optimizer, criterion, clip=1)
    print("train loss--->",train_loss)
    print("train acc-->",train_acc)

    #print(f'Test Loss: {test_loss:.3f} | Test BLEU Score: {test_bleu*100:.2f}%')

    # Evaluate model on validation set
    #valid_loss, valid_acc = evaluate(model, valid_iterator, criterion)

    return {'params': (enc_emb_dim, dec_emb_dim, hid_dim, n_layers, enc_dropout, dec_dropout, learning_rate),
            'train_loss': train_loss,
            'train_acc': train_acc}
           # 'valid_loss': valid_loss,
           # 'valid_acc': valid_acc}

# # Perform grid search over hyperparameters
results = []
for values in itertools.product(*params.values()):
    kwargs = dict(zip(params.keys(), values))
    result = train_eval_model(**kwargs)
    results.append(result)
    print(f"Params: {kwargs} | Train loss: {result['train_loss']:.3f} | Train acc: {result['train_acc']:.3f}")


best_result = max(results, key=lambda x: x['train_acc'])
print(f"\nBest hyperparameters: {best_result['params']}, Accuracy:{format(result)}")

