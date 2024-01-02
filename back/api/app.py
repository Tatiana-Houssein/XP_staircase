from flask import Flask, json, jsonify
from flask_cors import CORS

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


if __name__ == "__main__":
    app.run()
