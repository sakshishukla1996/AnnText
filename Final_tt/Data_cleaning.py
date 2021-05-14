import pandas as pd
import string
import numpy as np
import re
import spacy
import csv
nlp = spacy.load('en_core_web_sm')
from spacy.lang.en.stop_words import STOP_WORDS

input_folder_path= '/Users/sakshishukla/Desktop/text_tech/new_data.csv'
output_folder_path= '/Users/sakshishukla/Desktop/text_tech/'

# reading the folder name 
# converting into dataframe
def read_data(input_folder_path): 
    data = pd.read_csv(input_folder_path)
    data.columns=['No.', 'Tweet_id', 'tweet', 'moment', 'label']
    return data

# removes punctuation 
# numbers from the tweets
def remove_puncts_nums(text):
    text = re.sub("'", '', text.lower())
    text = re.sub("[^A-Za-z]", ' ', text)
    return text.strip()

# removes emoji from the tweets
def strip_emoji(text):
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    return RE_EMOJI.sub(r'', text)

# removes stop_words from the tweets
def remove_stop_words(text):
    text_list=[]
    for word in text.split():
        if word not in (STOP_WORDS - {'cannot','not', 'nothing'}) :
            text_list.append(word)
    return ' '.join(text_list)

# generates lemmatization
def gen_lemma(text):
    string =''
    for word in nlp(text):
        word = word.lemma_
        string = string + ' '+ word
    return string.strip()

# cleans the data and returns it
# uses sub_funcs in this cleaning func
def clean_data(data):
    data['tweet']= data.tweet.str.lower()
    data['tweet'] = data.tweet.apply(remove_puncts_nums)
    data['tweet'] = data.tweet.apply(strip_emoji)
    data['tweet'] = data.tweet.apply(remove_stop_words)
    data['tweet'] = data.tweet.apply(gen_lemma)
    return data

# transforms data to generate primary data information, 
# label data information, segmentation data information
def transform_data(data):
    f_char= 0
    i= 0
    seg_list=[]
    tweet_list=[]
    label_list=[]
    for row in data.iterrows():
        tweet_list.append({'tweet':row[1]['tweet']})
        label_list.append({'label':row[1]['label']})
        seg_list.append({'Segmentation_id' :'seg-r' + str(i), 'first_anchor' :f_char, 
                        'last_anchor' :f_char + len(row[1]['tweet']) - 1})
        f_char = f_char + len(row[1]['tweet'])
        i+= 1
    return tweet_list, label_list, seg_list

# writing files into primary, annotation & segmentation 
# wrt LAF/GrAF standards
def write_file(tweet_list, label_list, seg_list):
    with open(output_folder_path + 'primary_data.csv', 'w+', newline='') as csvfile:
        field_names = ['tweet']
        writer = csv.DictWriter(csvfile, field_names, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(tweet_list)

    with open(output_folder_path + 'annotation_data.csv', 'w+', newline='') as csvfile_2:
            field_names = ['label']
            writer = csv.DictWriter(csvfile_2, field_names, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(label_list)

    with open(output_folder_path + 'segmenatation_data.csv', 'w+', newline='') as csvfile_3:
            field_names = ['Segmentation_id', 'first_anchor', 'last_anchor']
            writer = csv.DictWriter(csvfile_3, field_names, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(seg_list)

def main():
    data = read_data(input_folder_path)
    data = clean_data(data)
    primary, annotation, segmentation = transform_data(data)
    write_file(primary, annotation, segmentation)

if __name__ == '__main__':
    main()