# Flask server
from flask import Flask, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder='static')

with open("data/synonym_graph.json", "r", encoding="utf-8") as f:
    graph_data = json.load(f)

# Precompute index for easy lookups
lemma_index = {lemma["id"]: lemma for lemma in graph_data.values()}
term_to_lemmas = {}
for lemma in graph_data.values():
    term_to_lemmas.setdefault(lemma["term"].lower(), []).append(lemma)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/random-lemma')
def random_lemma():
    center_lemma = random.choice(list(graph_data.values()))
    first_degree = []

    for syn in center_lemma["synonyms"]:
        if syn in term_to_lemmas:
            first_degree.extend(term_to_lemmas[syn])

    second_degree = []
    for lemma in first_degree:
        for syn in lemma["synonyms"]:
            if syn in term_to_lemmas:
                second_degree.extend(term_to_lemmas[syn])

    return jsonify({
        "center": center_lemma,
        "first_degree": first_degree,
        "second_degree": second_degree
    })

@app.route('/first-lemma')
def first_lemma():
    first_lemma = next(iter(graph_data.values()))
    first_degree = []

    for syn_id in first_lemma["synonyms"]:
        if syn_id in graph_data:
            first_degree.append(graph_data[syn_id])

    second_degree = []
    for lemma in first_degree:
        for syn_id in lemma["synonyms"]:
            if syn_id in graph_data:
                second_degree.append(graph_data[syn_id])

    return jsonify({
        "center": first_lemma,
        "first_degree": first_degree,
        "second_degree": second_degree
    })

if __name__ == '__main__':
    app.run(debug=True)