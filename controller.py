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
    print(tdm)
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




            
def getRankingWithTitle(allPosts, query):
    corpus = [tokenize(post['content']) for post in allPosts["posts"]]
    titleCorpus = [tokenize(post['title']) for post in allPosts["posts"]]
    post_ids  = [post["_id"] for post in allPosts["posts"]]
    N = len(corpus)
    ByTitleN = len(titleCorpus)
    cnto = 1
    for i in corpus:
        print(i, cnto)
        cnto= cnto+1
    sw = current_app.stopwords
    # print(sw)
    for i in range(len(corpus)):
        corpus[i] = [term for term in corpus[i] if term not in sw]
    for i in range(len(titleCorpus)):
        titleCorpus[i] = [term for term in titleCorpus[i]]
    cnto = 1
    for i in corpus:
        print(i, cnto)
        cnto= cnto+1
    unique_terms = set()
    unique_title_terms = set()

    for document in corpus:
        unique_terms = unique_terms.union(set(document))
    rows = []
    rows_for_title = []
    for title in titleCorpus:
        unique_title_terms = unique_title_terms.union(set(title))


    for document in corpus:
        freq_vector = dict.fromkeys(unique_terms, 0)
        for term in document:
            freq_vector[term] += 1
        rows.append(freq_vector)
    
    for title in titleCorpus:
        freq_vector_title = dict.fromkeys(unique_title_terms, 0)
        for term in title:
            freq_vector_title[term] += 1
        rows_for_title.append(freq_vector_title)
    # print(rows)
    # print("ROWWWWWWWWWWWWWWWWSSSSSSSS",rows_for_title)
    tdm = pd.DataFrame(rows)
    title_tdm = pd.DataFrame(rows_for_title)
    
    rows_with_all_zeroes = (title_tdm == 0).all(axis=1)

# Print rows with all zeroes
    for i in  unique_title_terms:
        print(i)
    print("Rows with all zeroes:")
    print(title_tdm[rows_with_all_zeroes])
    tdm = tdm.div(tdm.sum(axis=1), axis=0)
    title_tdm = title_tdm.div(title_tdm.sum(axis=1), axis=0)
    print(title_tdm)
    df = tdm.astype(bool).sum(axis=0)
    tdf = title_tdm.astype(bool).sum(axis=0)
    print(len(tdm.columns))
    for i in range(len(tdf)):
        print(tdf.iloc[i])
    idf = np.log((N + 1) / (df + 0.5))
    title_idf = np.log((ByTitleN + 1) / (tdf + 0.5))
    tdm = tdm.mul(idf, axis=1)
    print(title_tdm)
    title_tdm = title_tdm.mul(title_idf, axis=1)
    print(tdm)
    print(title_tdm)
    processedQuery = [query_processing(query, unique_terms)]
    processedQueryForTitle = [query_processing(query, unique_title_terms)]
    qvector = pd.DataFrame(processedQuery)
    titleqvector = pd.DataFrame(processedQueryForTitle)
    rows_with_all_zeroes = (titleqvector == 0).all(axis=1)
    print("QVECTOERS WITH ZEROWSSSS")
    print(len(titleqvector[rows_with_all_zeroes]))
    caution = len(titleqvector[rows_with_all_zeroes])
    print("uifhijsadbvjewqhfasdbvjieqrbfgjqwebnijq3rfkqsdnfug",titleqvector)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++===================================================++++++++++++++++++++++++++++++++++++", qvector)
    qvector = qvector.div(qvector.sum(axis=1), axis=0)
    qvector = qvector.mul(idf, axis=1)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++===================================================++++++++++++++++++++++++++++++++++++", titleqvector)
    if caution == 0:
        print("{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}")
        titleqvector = titleqvector.div(titleqvector.sum(axis=1), axis=0)
        
        titleqvector = titleqvector.mul(title_idf, axis=1)
   
    lst = []
    title_lst = []
    for q in range(len(qvector)):
        for i in range(len(tdm)):
            lst.append(find_cosine_sim(tdm.iloc[i], qvector.iloc[q]))
    if caution == 0:
        for q in range(len(titleqvector)):
            for i in range(len(title_tdm)):
                title_lst.append(find_cosine_sim(title_tdm.iloc[i], titleqvector.iloc[q]))
    else:
        for q in range(len(titleqvector)):
            for i in range(len(title_tdm)):
                title_lst.append(0)


        
    # similarity_df = pd.DataFrame(lst, columns=['post_id', 'similarity'])
    # print(similarity_df)
    # similarity_df = similarity_df.sort_values(by='similarity', ascending=False)
    # similarity_json = similarity_df.to_json(orient='records')
    # pnt = 0
    # for ls in title_lst:
    #     pnt = pnt+1
    #     print(ls, pnt)
    alpha = 0.7  # Set your alpha value

    result_lst = []

    for i in range(len(lst)):
        result = alpha * title_lst[i] + (1 - alpha) * lst[i]
        result_lst.append([post_ids[i],result])
    print(result_lst)
    similarity_df = pd.DataFrame(result_lst, columns=['post_id', 'similarity'])
    print(similarity_df)
    similarity_df = similarity_df.sort_values(by='similarity', ascending=False)
    similarity_json = similarity_df.to_json(orient='records')
    return similarity_json






