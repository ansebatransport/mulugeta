import ast
import math
import operator
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

SAFE_FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sqrt': math.sqrt,
    'log': math.log10,
    'ln': math.log,
    'factorial': math.factorial,
    'abs': abs,
    'floor': math.floor,
    'ceil': math.ceil,
}

SAFE_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
}


def safe_eval(expr):
    """Evaluate a mathematical expression safely using ast parsing."""
    tree = ast.parse(expr, mode='eval')
    return _eval_node(tree.body)


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if op_type is ast.Div and right == 0:
            raise ZeroDivisionError("Division by zero")
        return SAFE_OPERATORS[op_type](left, right)

    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return SAFE_OPERATORS[op_type](operand)

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Unsupported function call")
        func_name = node.func.id
        if func_name not in SAFE_FUNCTIONS:
            raise ValueError(f"Unknown function: {func_name}")
        args = [_eval_node(arg) for arg in node.args]
        if len(args) != 1:
            raise ValueError(f"{func_name} expects exactly 1 argument")
        return SAFE_FUNCTIONS[func_name](args[0])

    elif isinstance(node, ast.Name):
        if node.id not in SAFE_CONSTANTS:
            raise ValueError(f"Unknown constant: {node.id}")
        return SAFE_CONSTANTS[node.id]

    else:
        raise ValueError(f"Unsupported expression type: {type(node).__name__}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'expression' not in data:
        return jsonify({'error': 'No expression provided'}), 400

    expression = data['expression']
    try:
        result = safe_eval(expression)
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Invalid expression: {str(e)}'}), 400


if __name__ == '__main__':
    app.run(debug=True)
