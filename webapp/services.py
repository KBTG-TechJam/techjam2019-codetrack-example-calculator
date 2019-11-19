import operator
import re
from http import HTTPStatus

from flask import Flask, jsonify, request

app = Flask(__name__)

variable_re = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
func_map = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

variables = {}


@app.route("/calc", methods=['POST'])
def calculate_expression():
    body = request.get_json()
    left, op, right = body['expression'].split()

    left = _get_value(left)
    right = _get_value(right)

    result = func_map[op](left, right)
    result = f"{result:.2f}"
    return jsonify(result=result), HTTPStatus.OK


def _get_value(token):
    if variable_re.fullmatch(token):
        value = variables[token]
    else:
        value = token
    return float(value)


@app.route("/variable/<name>", methods=['PUT'])
def put_variable(name):
    body = request.get_json()
    if name in variables:
        status = HTTPStatus.NO_CONTENT  # 204
    else:
        status = HTTPStatus.CREATED  # 201
    variables[name] = body['value']
    return '', status


@app.route("/variable/<name>", methods=['GET'])
def get_variable(name):
    if name not in variables:
        return '', HTTPStatus.NOT_FOUND
    value = variables[name]
    value = f"{float(value):.2f}"
    return jsonify(value=value), HTTPStatus.OK
