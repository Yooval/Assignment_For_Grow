# -*- coding: utf-8 -*-
"""
Negative Tests - בדיקות ולידציה ומקרי קצה
Author: Yuval Yosef
Date: 27/09/2025

מטרת הקובץ: לבדוק שהאתר חוסם קלטים לא תקינים.
הטסטים בודקים האם הולידציה עובדת כראוי.

------------------------------------------------------------------
פקודת הרצה:
pytest Negative_Tests.py --headed --browser chromium --slowmo 1000
------------------------------------------------------------------

"""

from playwright.sync_api import Page, expect
import re
import time
import pytest

BASE_URL = "https://sandbox.grow.link/6f340bc4d18a0bcb559914d970ac2870-MTE4NjI"


# ========== פונקציות עזר ==========

def prep_to_personal(page: Page):
    """מכין את הדף - בוחר מוצרים ועובר לטופס פרטים אישיים"""
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")

    # בחירת מוצרים
    page.locator("input[aria-label='חומוס 30 שקלים']").click(force=True)
    page.locator("button[aria-label='להוספת כמות למוצר חומוס']").click()
    page.locator("input[aria-label='שקשוקה 40 שקלים']").click(force=True)
    page.locator("button[aria-label='להוספת כמות למוצר שקשוקה']").click()
    page.locator("input[aria-label='פיתה 2 שקלים']").click(force=True)
    page.locator("button[aria-label='להוספת כמות למוצר פיתה']").click()

    # מעבר לטופס
    page.get_by_role("button", name="המשך").click()
    page.wait_for_load_state("networkidle")


def fill_personal(page: Page, name: str, phone: str, addr: str):
    """ממלא את כל השדות בטופס הפרטים האישיים"""
    # שדות טקסט ראשיים
    vis = page.locator("input[type='text']:visible")
    vis.nth(0).fill(name, force=True)
    vis.nth(1).fill(phone, force=True)
    vis.nth(2).fill(addr, force=True)

    # שדות dropdown
    # מתי להתחיל
    page.locator("span[class^='additional-fields_dropdown-trigger-padding__']").first.click()
    page.locator("li span", has_text="מיד").click()

    # חמוצים
    pickles = page.locator("fieldset:has-text('חמוצים')")
    if pickles.count():
        pickles.locator("label:has-text('כן')").first.click()
    else:
        page.locator("label:has-text('כן')").first.click()

    # צ'יפס
    chips = page.locator("fieldset:has-text(\"צ'יפס\")")
    if chips.count():
        chips.locator("label:has-text('לא')").first.click()
    else:
        page.locator("label:has-text('לא')").nth(1).click()

    # מקור
    page.locator("span[class^='additional-fields_dropdown-trigger-padding__']").nth(1).click()
    page.locator("li span", has_text="פייסבוק").click()

    # משלוח
    page.locator("span[class^='additional-fields_dropdown-trigger-padding__']").nth(2).click()
    page.locator("li span", has_text="איסוף").click()


def accept_terms(page: Page):
    """מאשר תנאי שימוש"""
    page.locator("label[for='termsCheckbox']").click()
    try:
        page.locator("input#termsCheckbox").check(force=True)
    except:
        pass  # אם כבר מסומן


def open_pay_modal(page: Page):
    """פותח את חלון התשלום"""
    btn = page.get_by_label("המשך לשלב הבא וביצוע תשלום מאובטח", exact=True)
    btn.click()


def choose_visa(page: Page):
    """בוחר באפשרות תשלום באשראי"""
    try:
        btn = page.get_by_role("button", name="לתשלום באשראי")
        expect(btn).to_be_visible(timeout=8000)
        btn.click()
    except:
        # נסיון חלופי אם הראשון נכשל
        page.locator("img[alt='לתשלום באשראי'], img[aria-label='לתשלום באשראי']").first.locator(
            "xpath=ancestor::button[1]"
        ).click()


def find_in_frames(page: Page, selector: str, desc: str, timeout_ms: int = 10000):
    """
    מחפש אלמנט בתוך iframes.
    חלק מהטפסים באתר נמצאים בתוך iframe ולכן צריך לחפש בכולם.
    """
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        for frame in page.frames:
            element = frame.locator(selector)
            if element.count() > 0:
                return frame, element.first
        page.wait_for_timeout(200)
    raise AssertionError(f"לא הצלחתי למצוא: {desc}")


# ========== טסטים ==========

class TestNegativeCases:
    """
    מחלקת טסטים לבדיקת ולידציה.
    כל טסט בודק האם המערכת חוסמת קלט לא תקין.
    """

    def test_name_with_numbers_blocks_payment(self, page: Page):
        """
        בודק: האם המערכת חוסמת שם שמכיל מספרים
        קלט בעייתי: "יובל123"
        תוצאה רצויה: הכפתור 'המשך לתשלום' צריך להיות מושבת
        """
        prep_to_personal(page)
        fill_personal(page, name="יובל123", phone="0501234567", addr="הרצל 10")
        accept_terms(page)

        pay_btn = page.get_by_label("המשך לשלב הבא וביצוע תשלום מאובטח", exact=True)

        # בודק אם הכפתור מושבת
        try:
            expect(pay_btn).to_be_disabled()
        except AssertionError:
            # אם לא disabled, בודק את aria-disabled
            aria = pay_btn.get_attribute("aria-disabled")
            assert aria in ("true", "disabled", "1"), "הכפתור אמור להיות חסום עבור שם עם מספרים"

        # מוודא שחלון התשלום לא נפתח
        expect(page.get_by_role("button", name="לתשלום באשראי")).to_have_count(0)

    def test_name_missing_lastname_blocks_payment(self, page: Page):
        """
        בודק: האם המערכת דורשת שם מלא (שם + משפחה)
        קלט בעייתי: "יובל" (בלי שם משפחה)
        תוצאה רצויה: הכפתור 'המשך לתשלום' צריך להיות מושבת
        """
        prep_to_personal(page)
        fill_personal(page, name="יובל", phone="0501234567", addr="הרצל 10")
        accept_terms(page)

        pay_btn = page.get_by_label("המשך לשלב הבא וביצוע תשלום מאובטח", exact=True)

        try:
            expect(pay_btn).to_be_disabled()
        except AssertionError:
            aria = pay_btn.get_attribute("aria-disabled")
            assert aria in ("true", "disabled", "1"), "הכפתור אמור להיות חסום עבור שם חלקי"

        expect(page.get_by_role("button", name="לתשלום באשראי")).to_have_count(0)

    def test_address_only_numbers_blocks_payment(self, page: Page):
        """
        בודק: האם המערכת דורשת כתובת עם טקסט (לא רק מספרים)
        קלט בעייתי: "123456"
        תוצאה רצויה: הכפתור 'המשך לתשלום' צריך להיות מושבת
        """
        prep_to_personal(page)
        fill_personal(page, name="יובל יוסף", phone="0501234567", addr="123456")
        accept_terms(page)

        pay_btn = page.get_by_label("המשך לשלב הבא וביצוע תשלום מאובטח", exact=True)

        try:
            expect(pay_btn).to_be_disabled()
        except AssertionError:
            aria = pay_btn.get_attribute("aria-disabled")
            assert aria in ("true", "disabled", "1"), "הכפתור אמור להיות חסום עבור כתובת לא תקינה"

        expect(page.get_by_role("button", name="לתשלום באשראי")).to_have_count(0)

    def test_invalid_card_number_blocks_final_payment(self, page: Page):
        """
        בודק: האם המערכת מוודאת אורך כרטיס אשראי
        קלט בעייתי: כרטיס עם 12 ספרות (במקום 16)
        תוצאה רצויה: כפתור 'לתשלום' בטופס האשראי צריך להיות מושבת
        """
        # ממלא הכל תקין כדי להגיע לטופס האשראי
        prep_to_personal(page)
        fill_personal(page, name="יובל יוסף", phone="0501234567", addr="הרצל 10")
        accept_terms(page)

        # ממתין שהכפתור יהיה זמין
        pay_btn = page.get_by_label("המשך לשלב הבא וביצוע תשלום מאובטח", exact=True)
        expect(pay_btn).to_be_enabled(timeout=10000)

        # פותח חלון תשלום
        open_pay_modal(page)
        expect(page.get_by_role("button", name="לתשלום באשראי")).to_be_visible(timeout=8000)
        choose_visa(page)

        # ממלא פרטי אשראי
        # מוצא את השדה בתוך ה-iframe
        card_frame, card = find_in_frames(
            page,
            "#card-number, input[aria-label='מספר כרטיס'], input[name='cardNumber']",
            "שדה מספר כרטיס"
        )
        expect(card).to_be_visible(timeout=10000)

        # מכניס כרטיס קצר (12 ספרות)
        try:
            card.fill("424242424242")
        except:
            # אם fill לא עובד, מנסה להקליד
            card.click()
            for digit in "424242424242":
                card_frame.keyboard.type(digit, delay=20)

        # ממלא שאר השדות תקין
        _, month = find_in_frames(page, "select#expMonth, select[name='expMonth']", "חודש")
        month.select_option("03")

        _, year = find_in_frames(page, "select#expYear, select[name='expYear']", "שנה")
        year.select_option("30")

        _, cvv = find_in_frames(page, "#cvv, input[name='cvv'], input[aria-label*='CVV']", "CVV")
        cvv.fill("123")

        # בודק שכפתור התשלום מושבת
        found = False
        for frame in page.frames:
            pay_button = frame.get_by_role("button", name=re.compile("לתשלום"))
            if pay_button.count() > 0:
                expect(pay_button.first).to_be_disabled()
                found = True
                break

        assert found, "לא מצאתי את כפתור התשלום בטופס"