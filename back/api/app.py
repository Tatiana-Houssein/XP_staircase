from flask import Flask, json, jsonify, request
from flask_cors import CORS

from back.src.controller import (
    call_back_answer,
    call_back_next_stimulus,
    create_new_experiment,
)

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
    create_new_experiment()
    id_first_stimulus = call_back_next_stimulus()

    return jsonify({"id": id_first_stimulus})


@app.route("/next-stimulus", methods=["POST"])
def next_stimulus():  # noqa: ANN201
    payload = request.get_json()
    print(f"PAYLOAD: {payload}")
    call_back_answer(payload)
    id_next_stimulus = call_back_next_stimulus()

    return jsonify({"id": id_next_stimulus})


if __name__ == "__main__":
    app.run()
