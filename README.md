# Assignment For Grow

## Overview
Automated testing project for a payment system.  
Includes:
- UI tests (positive & negative flows)
- API tests (validations & error handling)
- CI/CD integration with GitHub Actions

---

## Project Structure
```
Assignment_for_Grow/
├── Q1-5A-Positive_Test.py      # UI positive flow
├── Q1-5B-Negative_Tests.py     # UI negative/validation
├── Q2-1-API_Test.py            # API tests
├── .github/
│   └── workflows/
│       └── tests.yml           # CI/CD pipeline
└── README.md
```

---

## Installation
API dependencies:
```
pip install requests
```

UI dependencies:
```
pip install pytest playwright
playwright install chromium
```

---

## Running Tests
API tests:
```
python Q2-1-API_Test.py
```

UI positive tests:
```
pytest Q1-5A-Positive_Test.py --headed --browser chromium --slowmo 1000
```

UI negative tests:
```
pytest Q1-5B-Negative_Tests.py --headed --browser chromium --slowmo 1000
```

---

## CI/CD
- All tests run automatically on every push.  
- View results in GitHub:  
  **Actions → Run Tests for Q2A → test → Run API Tests**

---

## Test Coverage
**API Tests (3):**
- Valid payment request  
- Missing required field  
- Invalid sum value  

**UI Positive (1):**
- Complete purchase flow  

**UI Negative (4):**
- Name with numbers  
- Missing last name  
- Invalid address format  
- Short credit card number  

---

## Environment Variables (Optional)
```
API_BASE_URL=https://sandbox.meshulam.co.il
MESHULAM_PAGE_CODE=e19e0b687744
MESHULAM_USER_ID=52e95954cd5c1311
```

---

## Recommended Tools
- Allure – Reporting  
- Docker – Containerized tests  
- TestRail – Test case management  

---

## Author
Yooval Yosef  
September 2025
