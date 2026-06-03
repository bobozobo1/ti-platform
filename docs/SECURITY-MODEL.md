# 🔐 SECURITY-MODEL.md
## מודל האבטחה של המערכת — תבנית למילוי בשלב 1.1

> **סטטוס: תבנית.** המסמך הזה הוא שלד. בשלב 1.1 תמלא אותו יחד עם Claude (במודל Opus).
> זה המסמך הכי חשוב בפרויקט — הוא מגדיר איך מידע מסווג מוגן.
> כל החלקים מסומנים `[למילוי]` ייקבעו יחד עם Claude.

---

## 0. עקרונות-על (קבועים — לא משתנים)

שלושה כללי ברזל שכל המערכת בנויה סביבם:

1. **Default Deny** — כל גישה נדחית כברירת מחדל. גישה ניתנת רק כשכל תנאי ההרשאה מתקיימים.
2. **Test the Denial** — לכל פיצ'ר, ה-test הראשון מוכיח שמשתמש לא מורשה *לא* רואה את המידע.
3. **No Leak Surfaces** — מידע מסווג לא דולף דרך: error messages, counts, search, autocomplete, logs, או timing.

---

## 1. שלושת ממדי ההרשאה

המערכת בודקת שלושה ממדים בכל גישה — **AND לוגי** (כל השלושה חייבים להתקיים).

### 1.1 Clearance Level
סולם עולה של רמות סיווג. משתמש ברמה X רואה objects עד רמה X.

`[למילוי: אילו רמות בדיוק במודל הארגוני שלך?]`
ברירת מחדל מ-PRD-v2:
- UNCLASSIFIED
- CONFIDENTIAL
- SECRET
- TOP SECRET

`[למילוי: איך clearance מיוצג ב-DB? — נקבע עם Claude]`

### 1.2 TLP Marking
מגביל שיתוף, בנפרד מ-classification.

`[למילוי: אילו TLP levels רלוונטיים אצלך? WHITE/GREEN/AMBER/RED?]`
`[למילוי: איך TLP מיוצג כ-marking-definition ב-STIX? — נקבע עם Claude]`

### 1.3 Permissions
פעולות מפורשות פר-משתמש: read, write, promote, export, revoke, admin.

`[למילוי: מבנה ה-permissions ב-DB — נקבע עם Claude]`

---

## 2. Policy Engine

הפונקציה המרכזית שכל בקשת גישה עוברת דרכה.

`[למילוי: איך נראה ה-Policy Engine? — נקבע עם Claude בשלב 1.1]`

עקרונות שחייבים להתקיים:
- נקודה מרכזית אחת (לא בדיקות מפוזרות)
- מחזיר decision בינארי: allow / deny
- deny הוא ברירת המחדל אם משהו לא ברור
- כל decision (כולל deny) נכתב ל-audit log

---

## 3. Leak Surfaces — מיפוי מלא

**זה החלק הקריטי ביותר.** כל מקום שמידע מסווג יכול לדלוף, ואיך חוסמים אותו.

| Leak Surface | הסיכון | החסימה |
|---|---|---|
| **Error messages** | "access denied" מדליף שה-object קיים | `[למילוי]` — תמיד "not found", לעולם לא "denied" |
| **Counts / pagination** | "showing 5 of 50" מדליף 45 מסווגים | `[למילוי]` — counts אחרי filtering בלבד |
| **Search results** | "3 results hidden" מדליף קיום | `[למילוי]` — search לא מזכיר hidden |
| **Autocomplete** | השלמה אוטומטית חושפת שמות מסווגים | `[למילוי]` |
| **Logs** | מידע מסווג בטקסט גלוי בלוגים | `[למילוי]` — לא לוגים PII/classified |
| **Timing** | תשובה מהירה ל-object קיים vs not found | `[למילוי]` — constant-time response |
| **Graph nodes** | node מסווג שמגיע ל-frontend ומוסתר ב-CSS | `[למילוי]` — סינון ב-backend, לא frontend |
| **WebSocket broadcast** | payload אחיד לכל המחוברים | `[למילוי]` — per-recipient filtering |
| **API direct access** | עקיפת ה-UI דרך call ישיר ל-API | `[למילוי]` — Policy Engine על כל endpoint |

`[למילוי: leak surfaces נוספים שעולים בדיון עם Claude]`

---

## 4. DB Layer vs Application Layer

חלוקת האחריות בין Supabase RLS ל-application code.

`[למילוי: מה ב-RLS, מה ב-application — נקבע עם Claude]`

עיקרון: **defense in depth** — גם RLS וגם application layer בודקים. אם אחד נכשל, השני תופס.

---

## 5. Testing Strategy ל-Security

איך מוכיחים שהמודל עובד.

`[למילוי: אסטרטגיית בדיקות — נקבע עם Claude]`

עקרונות:
- כל פיצ'ר: denial test ראשון (Red-Green)
- denial test = משתמש לא מורשה מנסה ומקבל "not found"
- בדיקה דרך UI *וגם* דרך API ישיר
- cross-user test (גל 6): משתמש A לא רואה data של B
- cross-tenant test (גל 7): tenant A לא רואה כלום מ-tenant B

---

## 6. Audit Requirements

מה מתועד ואיך.

`[למילוי: מבנה ה-audit log — נקבע עם Claude]`

עקרונות:
- append-only (immutable)
- כל decision של ה-Policy Engine, כולל denials
- שדות: timestamp, user, action, resource, result, reason
- exportable ל-SIEM

---

## 7. Decisions Log (security-specific)

החלטות security שמתקבלות במהלך הפרויקט.

`[למילוי תוך כדי: כל החלטת security שמתקבלת — תאריך, מה, למה]`

---

**מסמך זה ממולא בשלב 1.1 עם Claude (Opus). אל תתחיל קוד לפני שהוא מלא ומאושר.**
