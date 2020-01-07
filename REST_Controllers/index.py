from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/")
def hello_world():
	print(request.args.get('sensor'))
	print(request.args.get('algo'))
	return "Hello, World!"
