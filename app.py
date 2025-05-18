from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
GRAPH_FILE = "data/synonym_graph.json"
MAX_FIRST_DEGREE = 10
MAX_SECOND_DEGREE = 5

# Load graph at startup
with open(GRAPH_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)
#
#@app.route("/")
#def hello():
#    return "hello world"
@app.route("/first-lemma")
def get_first_lemma():
    lemma_id, lemma = next(iter(data.items()))

    result = {
        "id": lemma["id"],
        "term": lemma["term"],
        "part_of_speech": lemma["part_of_speech"],
        "definition": lemma["definition"],
        "synonyms": []
    }

    for sid in lemma.get("synonyms", [])[:MAX_FIRST_DEGREE]:
        if sid in data:
            first_degree_lemma = data[sid]

            nested = {
                "id": first_degree_lemma["id"],
                "term": first_degree_lemma["term"],
                "part_of_speech": first_degree_lemma["part_of_speech"],
                "definition": first_degree_lemma["definition"],
                "synonyms": []
            }

            for ssid in first_degree_lemma.get("synonyms", [])[:MAX_SECOND_DEGREE]:
                if ssid in data and ssid != lemma_id:
                    second_degree_lemma = data[ssid]
                    nested["synonyms"].append({
                        "id": second_degree_lemma["id"],
                        "term": second_degree_lemma["term"],
                        "part_of_speech": second_degree_lemma["part_of_speech"],
                        "definition": second_degree_lemma["definition"]
                    })

            result["synonyms"].append(nested)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)