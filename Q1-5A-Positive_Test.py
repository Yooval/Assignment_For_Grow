# -*- coding: utf-8 -*-
"""
Happy Path Test - בדיקת תהליך רכישה מלא
Author: Yuval Yosef
Date: 27/09/2025

מטרת הקובץ: בדיקת תרחיש רכישה מלא מתחילה ועד סוף.
הטסט עובר על כל השלבים ומוודא שהתהליך עובד כשהכל תקין.

------------------------------------------------------------------
פקודת הרצה:
pytest Q1-5A-Positive_Test.py --headed --browser chromium --slowmo 1000
------------------------------------------------------------------

"""

from playwright.sync_api import Page, expect
import re, time, pytest


class TestHappyPath:
    BASE_URL = "https://sandbox.grow.link/6f340bc4d18a0bcb559914d970ac2870-MTE4NjI"
    VALID_CARD = "4580458045804580"
    VALID_CVV = "123"
    VALID_MONTH = "03"  # expMonth option value
    VALID_YEAR = "30"  # expYear option value => 2030

    def _find_in_frames(self, page: Page, selector: str, desc: str, timeout_ms: int = 10000):
        """מאתר אלמנט בכל iframes ומחזיר locator כשהוא נמצא."""
        deadline = time.time() + timeout_ms / 1000
        while time.time() < deadline:
            for f in page.frames:
                loc = f.locator(selector)
                if loc.count() > 0:
                    return f, loc.first
            page.wait_for_timeout(200)
        raise AssertionError(f"'{desc}' לא נמצא באף iframe")

    def test_complete_purchase(self, page: Page):
        # 1) כניסה
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")

        # 2) בחירת מוצרים
        page.locator("input[aria-label='חומוס 30 שקלים']").click(force=True)
        page.locator("button[aria-label='להוספת כמות למוצר חומוס']").click()
        page.locator("input[aria-label='שקשוקה 40 שקלים']").click(force=True)
        page.locator("button[aria-label='להוספת כמות למוצר שקשוקה']").click()
        page.locator("input[aria-label='פיתה 2 שקלים']").click(force=True)
        page.locator("button[aria-label='להוספת כמות למוצר פיתה']").click()

        # 4) מעבר לפרטים אישיים
        page.get_by_role("button", name="המשך").click()
        page.wait_for_load_state("networkidle")

        # 5) מילוי שדות בסיס
        visible_inputs = page.locator("input[type='text']:visible")
        visible_inputs.nth(0).fill("יובל יוסף", force=True)  # שם
        visible_inputs.nth(1).fill("0501234567", force=True)  # טלפון
        visible_inputs.nth(2).fill("הר אדר מבוא הבוסתן 10", force=True)  # כתובת/הערות

        # מתי להתחיל → "מיד"
        page.locator("span[class^='additional-fields_dropdown-trigger-padding__']").first.click()
        page.locator("li span", has_text="מיד").click()

        # חמוצים בצד → "כן"
        pickles_fs = page.locator("fieldset:has-text('חמוצים')")
        if pickles_fs.count():
            pickles_fs.locator("label:has-text('כן')").first.click()
        else:
            page.locator("label:has-text('כן')").first.click()

        # צ'יפס בצד → "לא"
        chips_fs = page.locator("fieldset:has-text(\"צ'יפס\")")
        if chips_fs.count():
            chips_fs.locator("label:has-text('לא')").first.click()
        else:
            page.locator("label:has-text('לא')").nth(1).click()

        # מאיפה שמעת עלינו → "פייסבוק"
        page.locator("span[class^='additional-fields_dropdown-trigger-padding__']").nth(1).click()
        page.locator("li span", has_text="פייסבוק").click()

        # משלוח → "איסוף"
        page.locator("span[class^='additional-fields_dropdown-trigger-padding__']").nth(2).click()
        page.locator("li span", has_text="איסוף").click()

        # תנאי שימוש
        page.locator("label[for='termsCheckbox']").click()
        try:
            page.locator("input#termsCheckbox").check(force=True)
        except:
            pass

        # 6) המשך לתשלום
        pay_secure_btn = page.get_by_label("המשך לשלב הבא וביצוע תשלום מאובטח", exact=True)
        expect(pay_secure_btn).to_be_enabled(timeout=10000)
        pay_secure_btn.click()

        # 7) בחירת VISA
        try:
            btn = page.get_by_role("button", name="לתשלום באשראי")
            expect(btn).to_be_visible(timeout=8000)
            btn.click()
        except:
            page.locator("img[alt='לתשלום באשראי'], img[aria-label='לתשלום באשראי']").first.locator(
                "xpath=ancestor::button[1]"
            ).click()

        # 8) מילוי אשראי (בתוך iframe)
        card_frame, card = self._find_in_frames(page,
                                                "#card-number, input[aria-label='מספר כרטיס'], input[name='cardNumber']",
                                                "מספר כרטיס"
                                                )
        expect(card).to_be_visible(timeout=10000)
        try:
            card.fill(self.VALID_CARD)
        except:
            card.click()
            for ch in self.VALID_CARD:
                card_frame.keyboard.type(ch, delay=20)

        _, month = self._find_in_frames(page, "select#expMonth, select[name='expMonth']", "חודש")
        month.select_option(self.VALID_MONTH)

        year_frame, year = self._find_in_frames(page, "select#expYear, select[name='expYear']", "שנה")
        year.select_option(self.VALID_YEAR)

        _, cvv = self._find_in_frames(page, "#cvv, input[name='cvv'], input[aria-label*='CVV']", "CVV")
        cvv.fill(self.VALID_CVV)

        # 9) תשלום
        paid = False
        for f in page.frames:
            pay_btn = f.get_by_role("button", name=re.compile("לתשלום"))
            if pay_btn.count():
                expect(pay_btn).to_be_enabled(timeout=8000)
                pay_btn.click()
                paid = True
                break
        if not paid:
            page.get_by_role("button", name=re.compile("לתשלום")).click()

        # 10) הצלחה
        expect(page.locator("text=התשלום בוצע בהצלחה")).to_be_visible(timeout=10000)
