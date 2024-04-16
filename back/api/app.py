from flask import Flask, jsonify, request
from flask_cors import CORS

from back.src.controller import (
    call_back_answer,
    call_back_next_stimulus,
    create_new_experiment,
    get_dict_tache_interferente,
    save_form_data,
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
    call_back_answer(payload)
    dict_next_stimulus = call_back_next_stimulus()

    return jsonify(dict_next_stimulus)


@app.route("/submit", methods=["POST"])
def submit_form():  # noqa: ANN201
    form_data = request.json
    # Process form data here
    save_form_data(form_data=form_data)
    print("Received form data:", form_data)
    return jsonify({"message": "Form submitted successfully"}), 200


@app.route("/tache-interferente", methods=["GET"])
def get_tache_interferente_parameters():  # noqa: ANN201
    dict_tache_inter = get_dict_tache_interferente()
    return jsonify(dict_tache_inter)


if __name__ == "__main__":
    app.run()
