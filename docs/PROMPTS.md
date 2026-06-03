# PROMPTS.md — חבילת Prompts מוכנה לשימוש

> **איך להשתמש:** העתק את ה-prompt המתאים לתחילת ה-session המתאימה. החלף `[בסוגריים]` בערכים האמיתיים שלך.
>
> **מסמך משלים:** ב-`EXECUTION-GUIDE.md` יש prompts ספציפיים לכל שלב בכל גל. המסמך הזה הוא ה-prompts הכלליים לסיטואציות חוזרות.

---

## 🚀 Prompt #0 — Session Opener (להשתמש בכל שיחה חדשה)

**מודל:** המודל של המשימה שתבוא אחר כך (Sonnet ברירת מחדל)

```
שלום Claude. אני [שם], חוקר TI שבונה מערכת investigation מלאה עם תמיכה ב-classified data.

לפני שנתחיל, אני צריך שתעשה את הצעדים הבאים בסדר:

1. תקרא את הקובץ docs/CLAUDE_CONTEXT.md — זה ה-source of truth שלנו
2. תקרא את docs/SECURITY-MODEL.md — מודל ה-ABAC שעליו הכל בנוי
3. תקרא את docs/MASTER-PLAN.md — תמונה אסטרטגית של 7 הגלים
4. תקרא את docs/EXECUTION-GUIDE.md — הביצוע המפורט (שלב/פרומפט/מודל)
5. תקרא את docs/DECISIONS.md — החלטות שכבר קיבלנו
6. תאשר לי שאתה מבין את:
   - מה אנחנו בונים (המערכת המלאה, לא MVP)
   - מי המשתמש (אני)
   - ABAC כאבן יסוד
   - הסטאק הטכני
   - באיזה גל ושלב אנחנו (כתוב ב-CLAUDE_CONTEXT.md סעיף 9)

אחרי האישור, נמשיך למשימה. אל תתחיל לכתוב קוד עד שאני אומר.
```

**מה לעשות אחרי שClaude מאשר:**
שאל: "יש משהו ב-context שלא היה ברור או נראה סותר?" — אם יש, תבהיר לפני שמתחילים.

---

## 🐛 Prompt #5 — Bug Report Template

**מודל:** 🟡 Sonnet (רגיל) / 🔴 Opus (קשה / חוזר / נוגע ב-security)

```
מצאתי באג. הנה הפרטים:

**מה ניסיתי לעשות:**
[תיאור הפעולה]

**מה ציפיתי שיקרה:**
[התנהגות צפויה]

**מה קרה בפועל:**
[התנהגות בפועל]

**Steps to reproduce:**
1. [צעד 1]
2. [צעד 2]
3. [צעד 3]

**Browser console errors:**
```
[paste full error here]
```

**Network tab (אם רלוונטי):**
[failed request URL + status code + response]

**Screenshot (אם רלוונטי):**
[paste image]

**מתי זה התחיל:**
[לדוגמה: אחרי השינוי של אתמול ל-X, או: זה תמיד היה ככה]

**האם זה קשור ל-security?**
[כן — הצגת data שלא היה אמור להופיע / לא — באג פונקציונלי]

לפני שאתה מתחיל לתקן:
1. תן לי 3 hypotheses אפשריות, מהכי סבירה לפחות סבירה
2. לכל hypothesis, איך נוכל לאשש או לשלול אותה (בלי לכתוב קוד עדיין)
3. אם זה security-related — האם יש leak surface חדש שצריך לתעד ב-SECURITY-MODEL?
4. אחרי שאני בוחר hypothesis לחקור — נתחיל
```

---

## 🔒 Prompt #5.1 — Security-Specific Bug

**מודל:** 🔴 Opus (תמיד — security)

```
מצאתי בעיית security פוטנציאלית.

**מה ראיתי:**
[תיאור — לדוגמה: ראיתי count של 5 results אבל אני רואה רק 3]
[או: error message חשף ש-object קיים אבל אני לא אמור לדעת עליו]
[או: search הציע completion ל-object שאני לא מורשה לו]

**Steps to reproduce:**
1. [צעד 1]
2. [צעד 2]

**Clearance שלי:** [UNCLASSIFIED / CONFIDENTIAL / SECRET / TOP SECRET]
**ה-object שראיתי:** [classification שלו, אם ידוע]

לפני תיקון:
1. סווג את הבעיה — האי leak surface ידוע מ-SECURITY-MODEL.md, או חדש?
2. אם חדש — נתעד ב-SECURITY-MODEL.md לפני שנמשיך
3. תן לי 3 hypotheses לשורש הבעיה
4. תכנון תיקון שכולל denial test שמוכיח שהבעיה לא חוזרת
5. בדיקה: יש leak surfaces דומים שאולי גם פגיעים?
```

---

## 🔍 Prompt #6 — Code Review (בלי לקרוא קוד)

**מודל:** 🔴 Opus (review מעמיק שווה את המודל הטוב)

```
סיימת לכתוב את [הפיצ'ר]. לפני שאני אבדוק התנהגות, אני רוצה ש-תעשה self-review:

1. קרא שוב את הקוד שכתבת
2. תענה לי על השאלות הבאות:

**שבירות:**
- מה ה-3 הדברים הכי שבירים בקוד הזה?
- מה יקרה אם המשתמש יעשה X לא צפוי?

**Edge cases שלא טיפלת בהם:**
- מה קורה אם ה-input ריק?
- מה קורה אם ה-input מכיל תווים מיוחדים?
- מה קורה אם ה-API החיצוני מחזיר תשובה חלקית?
- מה קורה אם המשתמש מנתק רשת באמצע?
- מה קורה אם המשתמש פותח 2 tabs ועושה את אותה פעולה במקביל?

**Security (קריטי במערכת מסווגת):**
- האם הפיצ'ר עובר דרך ה-Policy Engine?
- האם ה-data מסונן ב-backend או ב-frontend? (חייב backend)
- האם counts/pagination מדליפים קיום של objects מסווגים?
- האם error messages מבחינים בין "not found" ל-"access denied"?
- האם יש leak surface חדש שלא ב-SECURITY-MODEL.md?
- האם יש timing attack אפשרי?
- האם logs מכילים מידע מסווג בטקסט גלוי?

**Input validation:**
- האם יש user input לא מאומת?
- האם יש secrets שיכולים להידלף ל-frontend?
- האם יש SQL injection risk? XSS risk?

**Tests:**
- כתבת E2E test? תראה לי את ה-test code.
- במידה ויש data מסווג — כתבת denial test? Red-Green?
- האם ה-test באמת בודק התנהגות או רק שהקוד רץ?
- מה ה-test לא מכסה?

**מה היית משנה:**
- אם היית מתחיל מחדש, מה היית עושה אחרת?
- מה ה-tech debt הראשי שיצרת?

תהיה כן. אם יש בעיות — אני מעדיף לשמוע עכשיו ולא בproduction.
```

---

## 📝 Prompt #7 — End of Session Wrap-up

**מודל:** 🟢 Haiku (משימה מוגדרת ופשוטה)

```
סיימנו את ה-session. לפני שנסגור, תבצע את ה-wrap-up הבא:

1. **עדכן את `docs/CLAUDE_CONTEXT.md`:**
   - סעיף 9 (Status) — גל ושלב נוכחיים, מה עובד עכשיו, מה בעבודה
   - סעיף 9 (Known Issues) — אם יש דברים שדחינו
   - סעיף 10 (DON'Ts) — אם משהו לא עבד וניסינו

2. **עדכן את `docs/DECISIONS.md`:**
   אם החלטנו משהו טכני בsession הזה, תוסיף entry בפורמט:
   ```
   ## YYYY-MM-DD — [שם ההחלטה]
   **Context:** [למה היה צריך להחליט]
   **Decision:** [מה החלטנו]
   **Alternatives considered:** [מה לא בחרנו ולמה]
   **Trade-offs:** [מה זה עולה לנו]
   ```

3. **עדכן את `docs/SECURITY-MODEL.md`** אם:
   - גילינו leak surface חדש
   - הוספנו policy חדשה
   - שינינו את ה-Policy Engine

4. **תיצור `SESSION-NOTES.md`** (overwrite כל פעם):
   - מה עשינו בsession
   - מה עוד צריך לעשות (TODO)
   - blockers
   - מה ה-next session אמורה להתחיל ממנו

5. **תיצור git commit עם הודעה תקנית** (לא תעשה push, רק commit מקומי)

6. **תסכם לי ב-3 משפטים:**
   - מה עשינו
   - מה השאלה הכי גדולה שנותרה פתוחה
   - מה הצעד הבא

תבצע את כל הצעדים האלה.
```

---

## 🚨 Prompt #8 — "אני תקוע / משהו השתבש"

**מודל:** 🔴 Opus (debugging קשה)

```
משהו לא עובד ואני לא מצליח להבין מה. אני צריך עזרה לפני שאני ממשיך.

**הסטוריה:**
[ספר ב-3-5 משפטים מה ניסית לעשות]

**מה שעבד פעם אחרונה:**
[איזה state היה עובד לפני]

**מה השתנה מאז:**
[רשימה של שינויים אחרונים, אם זוכר]

**מה אני רואה עכשיו:**
[התנהגות נוכחית, screenshots, errors]

**מה ניסיתי כבר:**
[מה השנייה שלא עזרה]

לפני שמנסים לתקן, אני רוצה ש:
1. תיצור לי map של כל הקומפוננטות שמעורבות בbug הזה
2. תיצור hypothesis tree — שורש הבעיה יכול להיות אחת מהן:
   - frontend bug
   - backend bug
   - DB / RLS issue
   - external API issue
   - auth / ABAC issue
   - Policy Engine bug
   - environment / deployment issue
   - browser cache
3. לכל ענף בעץ, איך נדע אם זה השורש?
4. תציע לי order לבדיקה מהפשוט ביותר לבדוק לקשה ביותר
5. נתחיל מהראשון

חשוב: אל תכתוב fix עד שאני מאשר את ההיפותזה.
```

---

## 🎯 Prompt #9 — Decision Point Review (סוף גל)

**מודל:** 🔴 Opus (החלטה אסטרטגית)

```
הגענו לסוף גל [X]: [שם הגל]. זמן ל-Decision Point פורמלי.

תעזור לי לעשות retrospective ולהחליט אם להמשיך:

**1. Actuals vs. Plan:**
- כמה זמן לקח בפועל לגל הזה? (vs. הערכה ב-MASTER-PLAN)
- אילו features לא הספקנו? למה?
- אילו features הוספנו שלא תכננו? למה?

**2. Quality:**
- כמה bugs נפתחו במהלך הגל?
- כמה מהם נפתרו? כמה עדיין פתוחים?
- ה-test coverage שלנו? (run pytest --cov)
- כמה denial tests יש לנו עכשיו?

**3. Security:**
- האם יש leak surfaces חדשים שלא ב-SECURITY-MODEL.md?
- האם כל endpoint שנוסף עובר דרך ה-Policy Engine?
- האם ה-RLS policies עודכנו?
- ביצענו security check השבועי?

**4. The Real Question:**
- האם אני משתמש בכלי בעבודה האמיתית שלי? כמה פעמים בשבוע האחרון?
- מה הדבר שעשה לי הכי הרבה רושם? למה?
- מה הדבר שהכי החלשני? למה?
- אם הייתי מתחיל מחדש היום, מה הייתי עושה אחרת?

**5. Tech Debt Inventory:**
- מה ה-tech debt שצברנו? תיצור רשימה מפורטת.
- מה ממנו חיוני לטפל לפני הגל הבא?
- מה יכול לחכות?

**6. Recommendation:**
על סמך כל הנ"ל, תן לי המלצה מנומקת:
- (א) להמשיך לגל [X+1]
- (ב) לעצור ולשפר את הקיים לפני שממשיכים
- (ג) לעצור לגמרי — הגל הנוכחי הוא מוצר שמיש, וזו נקודה לגיטימית לסיים

אל תפחד להמליץ על (ב) או (ג). אני רוצה אמת. במיוחד אחרי גל 3 (ה-MVP המקורי) וגל 5 (single-user מלא) — אלה נקודות עצירה לגיטימיות.
```

---

## 🔒 Prompt #9.1 — Security Audit (סוף גל)

**מודל:** 🔴 Opus (תמיד)

```
סיימנו גל [X]. לפני Decision Point — security audit מקיף.

תבצע audit מלא לפי SECURITY-MODEL.md:

**1. Leak Surfaces Check:**
עבור על כל leak surface ב-SECURITY-MODEL.md סעיף 3 ובדוק:
- האם הפיצ'רים החדשים שהוספנו פגיעים לאחד מהם?
- האם הוספנו leak surfaces חדשים שלא תועדו?
- תן לי דוגמה ספציפית של denial test לכל סוג leak

**2. Policy Engine:**
- האם כל endpoint חדש עובר דרך ה-Policy Engine?
- האם יש endpoint שעוקף את ה-Engine?
- האם ה-Engine מתעד denials ב-audit log?

**3. Backend vs Frontend Filtering:**
- האם יש קוד שמסנן data ב-frontend? (אסור)
- network inspection: האם classified data דולף ב-API responses?
- האם counts/pagination מחושבים אחרי filtering?

**4. Tests:**
- כל פיצ'ר עם classified data — יש לו denial test?
- ה-denial tests באמת מוכיחים denial, או רק שהקוד רץ?
- Red-Green: ראינו את ה-tests נכשלים לפני המימוש?

**5. Audit Log:**
- כל action sensitive מתועד?
- denials מתועדים גם?
- audit log עדיין immutable?

תיצור דוח ממצאים מפורט. רשימה של findings, חומרה (Critical/High/Medium/Low), והמלצת תיקון לכל אחד.

אם יש Critical findings — אל תמשיך לגל הבא לפני שתוקנו.
```

---

## 📚 Prompt #10 — Learning Mode (כשאני רוצה להבין משהו)

**מודל:** 🟡 Sonnet (הסברים רגילים) / 🔴 Opus (מושג מורכב)

```
[שאלה טכנית]

לפני שאתה עונה, אני רוצה להזכיר:
- אני לא מפתח. הסבר לי במונחים פשוטים.
- אם יש מונח טכני, תסביר אותו בפעם הראשונה שמופיע.
- אל תניח שיש לי ידע מקדים.
- תן דוגמה קונקרטית מהפרויקט שלנו, לא דוגמה כללית.
- אם זה קשור ל-security — תסביר גם את ה-security implications.

אחרי ההסבר, תשאל אותי: "מה לא ברור?" — אני רוצה להרגיש בנוח לחזור על שאלה.
```

---

## 🔧 שימוש מומלץ של הPrompts

**בכל יום:**
- פתח עם Prompt #0
- אם משימה לפי גל ושלב → השתמש בפרומפט מ-EXECUTION-GUIDE.md
- אם באג רגיל → Prompt #5
- אם באג security → Prompt #5.1
- אם תקוע → Prompt #8
- אם רוצה ללמוד → Prompt #10
- סגור עם Prompt #7

**פעם בשבוע:**
- security check שבועי (יש prompt ב-EXECUTION-GUIDE.md סעיף "שגרות קבועות")
- לעבור על SESSION-NOTES של השבוע
- לראות אם DECISIONS.md מתחיל להיראות עמוס מדי

**סוף כל גל:**
- Prompt #9.1 (Security Audit) — חובה
- Prompt #9 (Decision Point) — חובה
- אל תדלג עליהם, גם אם זה מרגיש מיותר

---

**זכור:** Prompts הם נקודת התחלה. כשאתה מבין יותר את הזרימה, אתה תפתח prompts משלך. הקובץ הזה הוא scaffolding, לא חוק.
