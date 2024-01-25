from flask import Flask, jsonify, request
from flask_cors import CORS

from back.src.controller import (
    call_back_answer,
    call_back_next_stimulus,
    create_new_experiment,
)

app = Flask(__name__)
CORS(app)


@app.route("/first-stimulus", methods=["GET"])
def first_stimulus():  # noqa: ANN201
    create_new_experiment()
    dict_next_stimulus = call_back_next_stimulus()

    return jsonify(dict_next_stimulus)


@app.route("/next-stimulus", methods=["POST"])
def next_stimulus():  # noqa: ANN201
    payload = request.get_json()
    print(f"PAYLOAD: {payload}")
    call_back_answer(payload)
    dict_next_stimulus = call_back_next_stimulus()

    return jsonify(dict_next_stimulus)


if __name__ == "__main__":
    app.run()
