from flask import Flask, json, jsonify
from flask_cors import CORS

from back.src.controller import save_experiment, start_new_experiment

app = Flask(__name__)
CORS(app)


@app.route("/test-token", methods=["GET"])
def get_test_token():  # noqa: ANN201
    print("GET BASIC")
    return jsonify({"id": 4})


@app.route("/json")
def send_json():  # noqa: ANN201
    data = {"name": "John", "age": 30, "city": "New York"}
    return json.dumps(data)


@app.route("/first-stimulus", methods=["GET"])
def first_stimulus():  # noqa: ANN201
    new_experiment = start_new_experiment()
    id_first_stimulus = new_experiment.choix_prochain_stimulus().numero
    save_experiment(new_experiment)
    return jsonify({"id": id_first_stimulus})


if __name__ == "__main__":
    app.run()
