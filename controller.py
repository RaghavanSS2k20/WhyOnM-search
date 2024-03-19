from flask import current_app
import pandas as pd
import numpy as np
from helpers import tokenize, find_cosine_sim, query_processing
def some_function():
    # Access stopwords using current_app
    stopwords = current_app.stopwords
    # Perform your operations using stopwords
    # For example:
    print("Stopwords are gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg : ", stopwords)

def getRanking(allPosts, query):
    # print(allPosts["posts"][0]['content'])
    corpus = [tokenize(post['content']) for post in allPosts["posts"]]
    post_ids  = [post["_id"] for post in allPosts["posts"]]
    N = len(corpus)
    sw = current_app.stopwords
    for i in range(len(corpus)):
        corpus[i] = [term for term in corpus[i] if term not in sw]
    unique_terms = set()

    for document in corpus:
        unique_terms = unique_terms.union(set(document))
    rows = []

    for document in corpus:
        freq_vector = dict.fromkeys(unique_terms, 0)
        for term in document:
            freq_vector[term] += 1
        rows.append(freq_vector)
    print(rows)
    tdm = pd.DataFrame(rows)
    tdm = tdm.div(tdm.sum(axis=1), axis=0)
    df = tdm.astype(bool).sum(axis=0)
    print(len(tdm.columns))
    idf = np.log((N + 1) / (df + 0.5))
    tdm = tdm.mul(idf, axis=1)
    processedQuery = [query_processing(query, unique_terms)]
    qvector = pd.DataFrame(processedQuery)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++===================================================++++++++++++++++++++++++++++++++++++", qvector)
    qvector = qvector.div(qvector.sum(axis=1), axis=0)
    qvector = qvector.mul(idf, axis=1)
    lst = []
    for q in range(len(qvector)):
        for i in range(len(tdm)):
            lst.append([post_ids[i],find_cosine_sim(tdm.iloc[i], qvector.iloc[q])])
    similarity_df = pd.DataFrame(lst, columns=['post_id', 'similarity'])
    print(similarity_df)
    similarity_df = similarity_df.sort_values(by='similarity', ascending=False)
    similarity_json = similarity_df.to_json(orient='records')

    return similarity_json




            






