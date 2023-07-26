from flask import Flask, jsonify, request, url_for, redirect
from flask_cors import CORS, cross_origin
import numpy as np
from urllib.parse import unquote

app = Flask(__name__)
cors = CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=['GET'])
@cross_origin()
def index():
    return jsonify({'about': 'Welcome to the Yamify Calculator! We support addition and multiplication, the subtraction and division of two numbers, an exponent functionality, and a polynomial root solver!'})

@app.route('/add/<num1>/<num2>', methods=['GET'])
def get_add(num1, num2):
    if num1 is None or num2 is None:
        return jsonify({'error': 'Invalid input. Both num1 and num2 are required.'}), 400
    try:
        result = float(num1) + float(num2)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. num1 and num2 must be valid numbers.'}), 400

@app.route('/sub/<num1>/<num2>', methods=['GET'])
def get_sub(num1, num2):
    if num1 is None or num2 is None:
        return jsonify({'error': 'Invalid input. Both num1 and num2 are required.'}), 400
    try:
        result = float(num1) - float(num2)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. num1 and num2 must be valid numbers.'}), 400

@app.route('/mult/<num1>/<num2>', methods=['GET'])
def get_mult(num1, num2):
    if num1 is None or num2 is None:
        return jsonify({'error': 'Invalid input. Both num1 and num2 are required.'}), 400
    try:
        result = float(num1) * float(num2)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. num1 and num2 must be valid numbers.'}), 400
    
@app.route('/div/<num1>/<num2>', methods=['GET'])
def get_div(num1, num2):
    if num1 is None or num2 is None:
        return jsonify({'error': 'Invalid input. Both num1 and num2 are required.'}), 400
    try:
        result = float(num1) / float(num2)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. num1 and num2 must be valid numbers.'}), 400
    except ZeroDivisionError:
        return jsonify({'error': 'Invalid input. Can\'t divide by zero.'}), 400

@app.route('/pow/<base>/<exp>', methods=['GET'])
def get_pow(base, exp):
    if base is None or exp is None:
        return jsonify({'error': 'Invalid input. Both num1 and num2 are required.'}), 400
    try:
        result = float(base) ** float(exp)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. num1 and num2 must be valid numbers.'}), 400

@app.route('/roots/<path:coefficients>', methods=['GET'])
def roots(coefficients):
    coefficients = unquote(coefficients).split('/')
    try:
        coefficients = [float(c) for c in coefficients]
    except ValueError:
        return jsonify({'error': 'Invalid input. The coefficients must be valid numbers.'}), 400

    try:
        roots = find_roots(coefficients)
        return jsonify({'roots': str(roots)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@app.route('/add_many/<path:nums>', methods=['GET'])
def add_many(nums):
    nums = unquote(nums).split('/')
    try:
        nums = [float(c) for c in nums]
    except ValueError:
        return jsonify({'error': 'Invalid input. The summands must be valid numbers.'}), 400

    try:
        result = sum(nums)
        return jsonify({'sum': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@app.route('/mult_many/<path:nums>', methods=['GET'])
def mult_many(nums):
    nums = unquote(nums).split('/')
    try:
        nums = [float(c) for c in nums]
    except ValueError:
        return jsonify({'error': 'Invalid input. The factors must be valid numbers.'}), 400

    try:
        result = np.prod(nums)
        return jsonify({'product': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def find_roots(coefficients):
    coefficients = np.array(coefficients)
    roots = np.roots(coefficients)
    return roots.tolist()

if __name__ == '__main__':
    app.run(debug=False)
