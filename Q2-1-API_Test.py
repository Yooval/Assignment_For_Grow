"""
Q2A - API tests
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


if __name__ == "__main__":
    print("בדיקות API ")
    print("-" * 30)

    # טסט 1א
    try:
        test_valid_request()
        print("✅ טסט 1א עבר - קיבלתי 200")
    except AssertionError as e:
        print(f"❌ טסט 1א נכשל - {e}")

    # טסט 1ב
    try:
        test_missing_field()
        print("✅ טסט 1ב עבר - קיבלתי שגיאה כמצופה")
    except AssertionError as e:
        print(f"❌ טסט 1ב נכשל - {e}")

    # טסט 1ג
    try:
        test_sum_zero()
        print("✅ טסט 1ג עבר - קיבלתי שגיאה עבור sum=0")
    except AssertionError as e:
        print(f"❌ טסט 1ג נכשל - {e}")

    print("-" * 30)
    print("סיום")