from flask import Flask, jsonify, current_app, request
from controller import getRanking
from helpers import getAllPosts
app = Flask(__name__)
import os
import nltk
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from controller import some_function
load_dotenv()
# print(os.getenv("TEST"))

cluster = MongoClient(os.getenv("DB_URL"))
with app.app_context():
    nltk.download('stopwords')
    current_app.stopwords = set(nltk.corpus.stopwords.words('english'))

@app.route('/')
def hello_world():
    some_function()
    return jsonify({"message":200})
    
    
@app.route('/search', methods=["POST"])
def search():
    data = request.json
    term = data["term"]
    allPosts = getAllPosts()
    rankedPosts = getRanking(allPosts, term)
    return rankedPosts, 200

    

    val = getRanking()
if __name__ == "__main__":

    app.run(debug = True)