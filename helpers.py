from flask import current_app
import requests
import re
import numpy as np
def tokenize(post):
    print(post)
    tokens = []
    for string in post.split():
        
        # print("======================================================")
        tokens.append(re.sub('[^a-zA-Z0-9]', '', string).lower())
        # return tokens
    return tokens
def find_cosine_sim(document, query):
    return np.dot(document, query) / ((np.dot(document, document) * np.dot(query, query)) ** 0.5)

def query_processing(query, unique_terms):
    sw = current_app.stopwords
    # print("sttttttttttoppppppppwordddssss : ", sw)
    query = tokenize(query)
    unique = set(query)
    q = []
    for w in unique:
        if w not in sw:
            q.append(w)
    print("++++++++++++++++++++++",q)
    freq =  dict.fromkeys(unique_terms,0)
    for term in q:
        if term in unique_terms:
            freq[term]+=1
    return freq


def getAllPosts():
    url = "https://whyonm-api.onrender.com/api/post"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(response.json()["posts"])
            # If the request is successful, return the JSON response
            return response.json()
        else:
            # If there's an error, print the status code
            print("Error:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        # If there's a connection error, print the exception
        print("Connection Error:", e)
        return None