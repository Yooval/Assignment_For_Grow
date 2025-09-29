"""
בדיקות API
"""
import requests

URL = "https://sandbox.meshulam.co.il/api/light/server/1.0/createPaymentProcess"


def test_valid_request():
    """Test 1a: Valid request returns 200"""
    data = {
        'pageCode': 'e19e0b687744',
        'userId': '52e95954cd5c1311',
        'sum': '1',
        'paymentNum': '1',
        'description': 'ORDER123',
        'pageField[fullName]': 'שם מלא',
        'pageField[phone]': '0534738605',
        'pageField[email]': 'debbie@meshulam.co.il'
    }

    response = requests.post(URL, data=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert 'url' in response.json(), "No URL in response"


def test_missing_field():
    """Test 1b: Missing field returns error"""
    data = {
        # 'pageCode': 'e19e0b687744',  # חסר
        'userId': '52e95954cd5c1311',
        'sum': '1',
        'paymentNum': '1',
        'description': 'ORDER123',
        'pageField[fullName]': 'שם מלא',
        'pageField[phone]': '0534738605',
        'pageField[email]': 'debbie@meshulam.co.il'
    }

    response = requests.post(URL, data=data)
    assert response.status_code != 200 or 'err' in response.json()


def test_sum_zero():
    """Test 1c: Sum zero returns error"""
    data = {
        'pageCode': 'e19e0b687744',
        'userId': '52e95954cd5c1311',
        'sum': '0',
        'paymentNum': '1',
        'description': 'ORDER123',
        'pageField[fullName]': 'שם מלא',
        'pageField[phone]': '0534738605',
        'pageField[email]': 'debbie@meshulam.co.il'
    }

    response = requests.post(URL, data=data)
    assert response.status_code != 200 or 'err' in response.json()
