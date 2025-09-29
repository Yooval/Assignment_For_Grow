"""
Q2-1-API_Test.py - בדיקות למערכת תשלום
Author: Yuval Yosef
Date: 29/09/2025

מטרת הקובץ: בדיקת API של createPaymentProcess במערכת משולם.
הבדיקות כוללות: בקשה תקינה, שדה חובה חסר, וערך לא תקין (sum=0).

------------------------------------------------------------------
פקודת הרצה:
python Q2-1-API_Test.py

לצפייה בתוצאות ב-GitHub Actions:
Actions → Run Tests for Q2A → test → Run API Tests
------------------------------------------------------------------
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

    print(f"   שולח בקשה ל: {URL}")
    response = requests.post(URL, data=data)
    print(f"   קיבלתי סטטוס: {response.status_code}")
    print(f"   תוכן התשובה: {response.text[:300]}")  # 300 תווים ראשונים

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


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

    print(f"   שולח בקשה בלי pageCode")
    response = requests.post(URL, data=data)
    print(f"   קיבלתי סטטוס: {response.status_code}")
    response_json = response.json()
    print(f"   יש שגיאה? {'err' in response_json or response_json.get('status') == '0'}")

    assert response.status_code != 200 or 'err' in response_json


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

    print(f"   שולח בקשה עם sum=0")
    response = requests.post(URL, data=data)
    print(f"   קיבלתי סטטוס: {response.status_code}")
    response_json = response.json()
    print(f"   יש שגיאה? {'err' in response_json or response_json.get('status') == '0'}")

    assert response.status_code != 200 or 'err' in response_json


if __name__ == "__main__":
    print("בדיקות API משולם")
    print("-" * 30)

    # טסט 1א
    print("\nטסט 1א: בקשה תקינה")
    try:
        test_valid_request()
        print("✅ טסט 1א עבר - קיבלתי 200")
    except AssertionError as e:
        print(f"❌ טסט 1א נכשל - {e}")

    # טסט 1ב
    print("\nטסט 1ב: שדה חסר")
    try:
        test_missing_field()
        print("✅ טסט 1ב עבר - קיבלתי שגיאה כמצופה")
    except AssertionError as e:
        print(f"❌ טסט 1ב נכשל - {e}")

    # טסט 1ג
    print("\nטסט 1ג: סכום אפס")
    try:
        test_sum_zero()
        print("✅ טסט 1ג עבר - קיבלתי שגיאה עבור sum=0")
    except AssertionError as e:
        print(f"❌ טסט 1ג נכשל - {e}")

    print("\n" + "-" * 30)
    print("סיום")
