# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 17:27:58 2022

@author: Team Lego Coders
"""


#below dependency are for nltk work
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.cluster.util import cosine_distance


import numpy as np
import networkx as nx

def read_article(file_name):
 #   print("I AM IN READ FUNCTION")
    file = open(file_name, 'r', encoding='utf-8')
    filedata = file.readlines()
   # print("this is file data value in read_article :")
    #print(filedata)   
   # article = filedata[0].split(".")
    article = filedata
   # print("this is value of article in read_article :")
  #  print(article)
    sentences = []
    for sentence in article:
    #    print("I AM IN READ FUNCTION and FOR LOOP")
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
   # print("final o/p :", sentences)
    return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
   # print("I AM IN similarity FUNCTION")
    if stopwords is None:
        stopwrds = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    
    for w in sent1:
      #  print("I AM IN simi FUNCTION and loop for vector 1")
        if w in stopwords:
            continue
        vector1[all_words.index(w)]  += 1
   # print(vector1)
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)]  += 1
    return 1 - cosine_distance(vector1, vector2)    
        

def get_sim_matrix(sentences, stop_words):
  #  print('Parth parth')
  #  print(len(sentences))
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
  #  print("Blank Matrix :" ,similarity_matrix); 
    for idx1 in range(len(sentences)): 
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix

def generat_summary(file_name, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []
    sentences = read_article(file_name)
    # print('This is return from read article func :')
    # print(sentences)
    sentence_similarity_matrix = get_sim_matrix(sentences, stop_words)
   # print("Is my code failed here ?", sentence_similarity_matrix)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
  #  print("Is my code failed here ?", sentence_similarity_graph)
    scores = nx.pagerank(sentence_similarity_graph)
    #print("Is my code failed here ?", scores)
    #ranked_sentence = sorted(((scores[i], s)for i,s in enumerate(sentences)))
    #print(type(ranked_sentence))
    ranked_sentence = list(((scores[i], s)for i,s in enumerate(sentences)))
    #final = []
    
    for i in range(top_n):
       # print(i)
        summarize_text.append(" ".join(ranked_sentence[i][1]))
        
    return summarize_text
    #print("Summary \n",  ". ".join(summarize_text))
    
final = generat_summary('clean_file.txt', 6) 
number = 1  
with open('your_mom.txt', 'w') as op:
    
    op.write('MOM From Todays Call :'); op.write('\n')
    for line in final:
        line = str(number) + ". " + line
        op.write(line); op.write('\n')
        number +=1
        
op.close()        
        
        
        
    
        
    



 