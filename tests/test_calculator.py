import math
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import safe_eval


class TestBasicArithmetic:
    def test_addition(self):
        assert safe_eval('2 + 3') == 5

    def test_subtraction(self):
        assert safe_eval('10 - 4') == 6

    def test_multiplication(self):
        assert safe_eval('6 * 7') == 42

    def test_division(self):
        assert safe_eval('15 / 3') == 5.0

    def test_floor_division(self):
        assert safe_eval('17 % 5') == 2

    def test_power(self):
        assert safe_eval('2 ** 10') == 1024

    def test_complex_expression(self):
        assert safe_eval('(2 + 3) * 4') == 20

    def test_nested_parentheses(self):
        assert safe_eval('((2 + 3) * (4 - 1))') == 15


class TestScientificFunctions:
    def test_sin_zero(self):
        assert safe_eval('sin(0)') == 0

    def test_cos_zero(self):
        assert safe_eval('cos(0)') == 1

    def test_tan_zero(self):
        assert safe_eval('tan(0)') == 0

    def test_sqrt(self):
        assert safe_eval('sqrt(16)') == 4

    def test_log(self):
        assert safe_eval('log(100)') == 2

    def test_ln(self):
        assert safe_eval('ln(e)') == 1

    def test_factorial(self):
        assert safe_eval('factorial(5)') == 120

    def test_abs_positive(self):
        assert safe_eval('abs(5)') == 5

    def test_abs_negative(self):
        assert safe_eval('abs(-5)') == 5

    def test_floor(self):
        assert safe_eval('floor(3.7)') == 3

    def test_ceil(self):
        assert safe_eval('ceil(3.2)') == 4


class TestConstants:
    def test_pi(self):
        assert safe_eval('pi') == math.pi

    def test_e(self):
        assert safe_eval('e') == math.e

    def test_pi_in_expression(self):
        assert safe_eval('2 * pi') == 2 * math.pi


class TestUnaryOperators:
    def test_negative(self):
        assert safe_eval('-5') == -5

    def test_positive(self):
        assert safe_eval('+5') == 5

    def test_negative_in_expression(self):
        assert safe_eval('3 + (-2)') == 1


class TestErrorHandling:
    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            safe_eval('1 / 0')

    def test_unknown_function(self):
        with pytest.raises(ValueError):
            safe_eval('unknown(5)')

    def test_unknown_constant(self):
        with pytest.raises(ValueError):
            safe_eval('unknown')

    def test_empty_expression(self):
        with pytest.raises(Exception):
            safe_eval('')


class TestAPIFlask:
    def test_calculate_endpoint(self, client):
        response = client.post('/calculate',
                             json={'expression': '2 + 3'},
                             content_type='application/json')
        data = response.get_json()
        assert response.status_code == 200
        assert data['result'] == 5

    def test_calculate_no_expression(self, client):
        response = client.post('/calculate',
                             json={},
                             content_type='application/json')
        assert response.status_code == 400

    def test_calculate_error(self, client):
        response = client.post('/calculate',
                             json={'expression': '1 / 0'},
                             content_type='application/json')
        data = response.get_json()
        assert response.status_code == 400
        assert 'error' in data

    def test_index_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
