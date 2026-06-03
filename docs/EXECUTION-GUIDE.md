# 📋 EXECUTION-GUIDE.md
## מדריך ביצוע שלב-אחר-שלב — כל הפרויקט

> זה המסמך שתעבוד ממנו יום-יום. לכל שלב בכל גל:
> **(1) מה עושים** · **(2) הפרומפט המדויק** · **(3) באיזה מודל**.
>
> עבוד בסדר. אל תדלג. כל גל מסתיים בנקודת עצירה לגיטימית.

---

## איך להשתמש במדריך הזה

1. **כל שלב הוא יחידת עבודה** — לרוב session אחת או שתיים (1.5-3 שעות).
2. **לפני כל שלב** — פתח עם שגרת ה-context (ראה למטה).
3. **העתק את הפרומפט** כמו שהוא, החלף `[בסוגריים]` בערכים שלך.
4. **בחר את המודל** המצוין ב-🔴/🟡/🟢.
5. **אחרי כל שלב** — סגור עם שגרת ה-wrap-up.

### מקרא המודלים
- 🔴 **Opus** — תכנון, security, debugging קשה, Decision Points
- 🟡 **Sonnet** — ברירת מחדל: כתיבת קוד, פיצ'רים, tests
- 🟢 **Haiku** — wrap-ups, commits, סיכומים

### שגרת פתיחה (לפני כל שלב)
**מודל:** לפי השלב.
```
תקרא את docs/CLAUDE_CONTEXT.md, docs/SECURITY-MODEL.md (אם קיים), ו-docs/DECISIONS.md.
תאשר באיזה גל ושלב אנחנו (סעיף Status ב-CONTEXT). יש משהו לא ברור?
```

### שגרת סגירה (אחרי כל שלב)
**מודל:** 🟢 Haiku
```
סיימנו את שלב [X]. תעשה wrap-up:
1. עדכן CLAUDE_CONTEXT.md סעיף Status — מה עובד עכשיו
2. עדכן DECISIONS.md אם קיבלנו החלטה טכנית
3. צור git commit עם הודעה תקנית
4. סכם ב-3 משפטים: מה הושג, שאלה פתוחה, צעד הבא
```

---
---

# 🌊 גל 1 — Secure Foundation
### תוצאה: login + מנוע ABAC עובד. הבסיס לכל המערכת.

---

## שלב 1.0 — הקמת חשבונות (ידני, ללא Claude)

**מה עושים:** פותחים את כל החשבונות והשירותים. אין כאן Claude — זו עבודה ידנית.

**מודל:** ❌ ללא Claude

**Checklist:**
- [ ] GitHub account + repo בשם `ti-platform`
- [ ] Supabase project
- [ ] Vercel account (חבר ל-GitHub)
- [ ] Railway account (חבר ל-GitHub)
- [ ] API keys: VirusTotal, AbuseIPDB, WhoisXML
- [ ] Password manager לשמירת כל ה-keys
- [ ] העלאת 7 מסמכי הפרויקט ל-`docs/` ב-repo

---

## שלב 1.1 — תכנון ה-Security Model ⭐

**מה עושים:** זו ההחלטה הכי חשובה בכל הפרויקט. מתכננים את מודל ה-ABAC המלא — איך מיוצגות הרשאות, איך נבדקת כל גישה, ואיך מונעים דליפות. **אל תכתוב קוד בשלב הזה.**

**מודל:** 🔴 **Opus** (אין פשרות — הבסיס של הכל)

**הפרומפט:**
```
אנחנו מתחילים את הפרויקט המלא. אבן היסוד היא ABAC — המערכת חייבת לתמוך
ב-classified data מהיום הראשון. זה משפיע על כל שורת קוד בהמשך.

לפני כל קוד, תכנן איתי את ה-Security Model. תקרא את PRD-v2.md סעיף 15 (ABAC)
ואת MASTER-PLAN.md עקרון-העל "Security-First".

תיצור docs/SECURITY-MODEL.md שעונה על:
1. שלושת ממדי ההרשאה (Clearance, TLP, Permissions) — איך כל אחד מיוצג ב-DB
2. ה-Policy Engine — איך נבדקת כל בקשת גישה (ה-AND הלוגי של שלושת התנאים)
3. Default Deny — איך מבטיחים שברירת המחדל היא דחייה
4. Leak surfaces — רשימה מלאה של כל המקומות שמידע יכול לדלוף:
   error messages, counts, pagination, search results, autocomplete, logs, timing
   ולכל אחד — איך חוסמים אותו
5. איך Supabase RLS משתלב עם ABAC — מה ב-DB layer, מה ב-application layer
6. Testing strategy ל-security — איך נוכיח שהמודל עובד

זו ההחלטה הכי קריטית בפרויקט. קח את הזמן. שאל אותי שאלות על המודל הארגוני שלי
(אילו clearance levels, איך TLP עובד אצלי) לפני שתכתוב את ה-design.
הצג לי את ה-design ונדון בו לעומק לפני שעוברים לקוד.
```

**מה לבדוק בתוצאה:** שיש התייחסות מפורשת ל-leak surfaces (לא רק "מי רואה מה"). זה ההבדל בין מערכת מסווגת אמיתית לצעצוע. במיוחד — ש"access denied" ו"not found" נראים זהים למשתמש לא מורשה.

---

## שלב 1.2 — תשתית בסיסית (Repo + Deploy)

**מה עושים:** מקימים את השלד הטכני — frontend ריק, backend ריק, deployment עובד, CI/CD. עדיין בלי ABAC ובלי פיצ'רים.

**מודל:** 🟡 **Sonnet** (boilerplate setup)

**הפרומפט:**
```
ה-Security Model אושר. עכשיו נקים את התשתית הבסיסית (עדיין בלי ABAC, בלי פיצ'רים).

תבנה לי checklist מפורט, ואז נבצע צעד-צעד. כל צעד: הוראות מדויקות (מה ללחוץ,
איפה, מה להעתיק), כי אני לא יודע פיתוח.

מה צריך:
1. מבנה repo לפי CLAUDE_CONTEXT.md סעיף 5
2. Frontend ריק (React + Vite + TS + Tailwind) deployed ל-Vercel
3. Backend ריק (FastAPI) עם /health endpoint, deployed ל-Railway
4. .env.example מתועד
5. GitHub Actions: lint + tests על כל PR

תתחיל מ-checklist + הצעד הראשון בלבד. נעבוד צעד-צעד, אישור ביניהם.
diffs קטנים. אל תכתוב קוד מורכב — הכל מינימלי.
```

---

## שלב 1.3 — שכבת ABAC (Schema + Policy Engine)

**מה עושים:** בונים את הלב של ה-security — schema של הרשאות, RLS policies, ו-Policy Engine מרכזי שכל endpoint עובר דרכו.

**מודל:** 🔴 **Opus** (security-critical — כל טעות היא דליפה)

**הפרומפט:**
```
התשתית עומדת. עכשיו נבנה את שכבת ה-ABAC לפי SECURITY-MODEL.md. זה security-critical.

צעד-צעד:
1. DB schema: users עם clearance_level, טבלת permissions, marking-definitions ל-TLP
2. Supabase RLS policies שמיישמות Default Deny (ברירת מחדל = דחייה)
3. Policy Engine ב-backend — פונקציה מרכזית אחת שכל endpoint עובר דרכה
4. Middleware שמיישם את הבדיקה על כל request

לכל צעד: קוד + test. עקרון קריטי — ה-test הראשון לכל policy הוא denial test:
מוכיח שמשתמש לא מורשה *לא* מקבל גישה. נראה אותו נכשל לפני המימוש, עובר אחרי (Red-Green).

diffs קטנים, אישור ביניהם. אל תתקדם בלי שאני מאשר שכל צעד עובד.
```

**מה לבדוק:** שה-Policy Engine הוא נקודה מרכזית אחת (לא בדיקות מפוזרות בכל endpoint). זה מה שמבטיח שלא תשכח בדיקה ב-endpoint עתידי.

---

## שלב 1.4 — User Management + Clearance

**מה עושים:** ממשק לניהול משתמשים — admin יוצר משתמשים, מקצה clearance levels, וכל שינוי מתועד.

**מודל:** 🔴 **Opus** (security-critical)

**הפרומפט:**
```
נבנה את ניהול המשתמשים עם clearance levels. security-critical.

acceptance criteria:
1. Admin יוצר משתמש עם clearance level (UNCLASSIFIED → TOP SECRET)
2. Admin משנה clearance, וזה מתועד ב-audit log
3. משתמש רואה רק את מה שה-clearance שלו מתיר
4. כל שינוי הרשאה = audit entry (who, what, when, old/new value)

קריטי — denial tests:
- משתמש CONFIDENTIAL מנסה לגשת ל-SECRET object דרך UI → מקבל "not found"
- אותו ניסיון דרך API ישירות → גם "not found"
- "not found" ולא "access denied" — כי "access denied" מדליף שה-object קיים

צעד-צעד, אישור ביניהם.
```

---

## שלב 1.5 — Audit Log Foundation

**מה עושים:** בונים את ה-audit log ה-immutable — כל פעולת הרשאה מתועדת ולא ניתנת לעריכה.

**מודל:** 🟡 **Sonnet**

**הפרומפט:**
```
נבנה תשתית audit log (immutable / append-only).

acceptance criteria:
1. כל פעולת הרשאה מתועדת: clearance changes, access grants, denials, exports
2. ה-log הוא append-only — אי אפשר לערוך או למחוק entries
3. כל entry: timestamp, user, action, resource, result, reason
4. denials מתועדים גם (ניסיון גישה שנכשל = event חשוב)

תכתוב E2E test שמוכיח שה-log לא ניתן לעריכה (ניסיון UPDATE/DELETE נכשל).
diffs קטנים.
```

---

## שלב 1.6 — Security Audit + Decision Point של גל 1

**מה עושים:** בודקים שכל מודל ה-security עובד לפני שבונים עליו את כל השאר. זו נקודת עצירה ראשונה.

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
סיימנו את גל 1 — Secure Foundation. self-review מעמיק + security audit:

Security audit — עבור על כל leak surface מ-SECURITY-MODEL.md:
- counts/pagination מדליפים קיום של objects מסווגים? תוכיח שלא.
- error messages מבחינים בין "not found" ל-"access denied"? (אסור)
- timing attack אפשרי? (תשובה ל-object קיים מהירה יותר מ-not found?)
- logs מכילים מידע מסווג בטקסט גלוי?
- ה-Policy Engine באמת נקודה מרכזית? כל endpoint עובר דרכו?

Decision Point: האם ה-security model יציב מספיק לבנות עליו את כל השאר?
אם יש ספק — נתקן עכשיו. לתקן security foundation בגל 5 זה אסון.
תן לי המלצה מנומקת: ממשיכים לגל 2, או נשארים לחזק?
```

**🛑 נקודת עצירה 1:** אם ה-security לא יציב — אל תמשיך. זה הבסיס של הכל.

---
---

# 🌊 גל 2 — Enrichment Core
### תוצאה: IOC lookup מ-3 מקורות, מסונן לפי clearance. כלי שמיש בעבודה.

---

## שלב 2.1 — תכנון Enrichment עם Classification

**מה עושים:** מתכננים איך כל תוצאת enrichment מקבלת classification, ואיך משתמש רואה רק תוצאות ב-clearance שלו.

**מודל:** 🔴 **Opus** (design + נוגע ב-classification)

**הפרומפט:**
```
מתחילים גל 2: Enrichment Core. כמו IOC lookup רגיל, אבל עם ABAC.

האתגר: לכל enrichment result יש classification. תוצאה מ-feed ציבורי = UNCLASSIFIED.
תוצאה ממקור פנימי רגיש = יכולה להיות CONFIDENTIAL ומעלה.

תכנן (docs/WAVE-2-DESIGN.md):
1. איך נקבע ה-classification של כל enrichment result?
2. איך משתמש רואה רק תוצאות ב-clearance שלו?
3. מה קורה כש-enrichment מחזיר תוצאות מעל ה-clearance? (מסתירים בשקט, לא "hidden")
4. mock-first: mocks לכל API חיצוני לפני חיבור אמיתי
5. rate limiting (VirusTotal = 4/min!) ו-error handling

נאשר לפני קוד. עקרון: סינון ב-backend, frontend לא מקבל תוצאה מעל clearance.
```

---

## שלב 2.2 — Mock Services

**מה עושים:** בונים mocks ל-3 ה-APIs כדי לפתח בלי לבזבז quota.

**מודל:** 🟡 **Sonnet**

**הפרומפט:**
```
ה-design אושר. נתחיל מ-mock services ל-VirusTotal, AbuseIPDB, WHOIS.

דרישות:
1. mock מחזיר אותו פורמט כמו ה-API האמיתי
2. environment variable שמחליף בין mock ל-real
3. mock כולל תרחיש "API נכשל" לבדיקת error handling
4. mock כולל תוצאות עם classification levels שונים (לבדיקת clearance filtering)

תכתוב E2E test בסיסי שה-mock עובד. diffs קטנים.
```

---

## שלב 2.3 — Backend Enrichment Endpoint

**מה עושים:** בונים את ה-endpoint שמקבל IOC, מזהה סוג, ומריץ enrichment — עם clearance filtering.

**מודל:** 🟡 **Sonnet** (ביצוע), אבל **🔴 Opus** לחלק ה-clearance filtering

**הפרומפט:**
```
נבנה את endpoint ה-enrichment. צעד-צעד:
1. זיהוי סוג IOC (IP/domain/hash/URL) — בלי enrichment עדיין
2. חיבור ל-mock VirusTotal
3. AbuseIPDB
4. WHOIS
5. clearance filtering — תוצאות מעל clearance המשתמש לא מוחזרות
6. טיפול ב-API שנכשל (partial result)

לכל צעד: קוד + test. צעד 5 (clearance filtering) הוא security-critical —
denial test שמוכיח שתוצאה מסווגת לא מגיעה למשתמש לא מורשה, ולא דרך count/error.
diffs קטנים, אישור ביניהם.
```

---

## שלב 2.4 — Frontend Lookup UI

**מה עושים:** בונים את הממשק — שדה IOC, כפתור, תצוגת תוצאות בכרטיסיות.

**מודל:** 🟡 **Sonnet**

**הפרומפט:**
```
נבנה את ה-frontend לפי ה-wireframe ב-WAVE-2-DESIGN.md. צעד-צעד:
1. שדה input ל-IOC + כפתור Investigate
2. loading state
3. תצוגת תוצאות בכרטיסיות (כרטיס לכל מקור)
4. error tags כשמקור נכשל
5. validation של input לא תקין

shadcn/ui components. E2E test שמכסה את ה-acceptance criteria.
diffs קטנים, אישור ביניהם.
```

---

## שלב 2.5 — חיבור APIs אמיתיים

**מה עושים:** מחליפים mocks ב-APIs אמיתיים, בזהירות עם rate limits.

**מודל:** 🟡 **Sonnet**

**הפרומפט:**
```
הכל עובד עם mocks. נחבר ל-APIs אמיתיים.
1. איפה לשים API keys (.env) — ותזכיר לי לוודא ש-.env לא ב-git
2. מעבר מ-mock ל-real, אחד-אחד
3. בדיקה עם IOC אמיתי שאספק (8.8.8.8) אחרי כל אחד
4. ודא שה-rate limiting עובד (VirusTotal 4/min)
```

---

## שלב 2.6 — Security Check + Decision Point של גל 2

**מה עושים:** בדיקת security ממוקדת ל-enrichment + נקודת עצירה.

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
סיימנו גל 2. self-review + security check:
- תוצאה מסווגת אף פעם לא מגיעה ל-frontend? (network inspection)
- count של תוצאות לא מדליף כמה תוצאות מסווגות הוסתרו?
- error של API לא חושף מידע מסווג?
- edge cases: IOC ריק, תווים מיוחדים, IPv6, domain עם Unicode?

Decision Point: האם אני משתמש בכלי בעבודה האמיתית?
המלצה: ממשיכים לגל 3 (הגרף), או משפרים קודם?
```

**🛑 נקודת עצירה 2** + 🎯 **בדיקת מציאות:** השתמש בכלי בעבודה אמיתית לפחות פעם אחת.

---
---

# 🌊 גל 3 — Investigation Graph
### תוצאה: גרף ויזואלי אינטראקטיבי, מסונן לפי clearance. הלב של המערכת + ה-MVP המקורי.

---

## שלב 3.1 — לימוד Cytoscape.js

**מה עושים:** לומדים את הספרייה שתשמש לגרף, לפני שכותבים קוד. Cytoscape הוא מורכב — שווה להבין אותו קודם.

**מודל:** 🔴 **Opus** (טכנולוגיה חדשה ומורכבת)

**הפרומפט:**
```
מתחילים גל 3: Investigation Graph. נשתמש ב-Cytoscape.js.

לפני קוד, תכתוב לי סיכום של עמוד אחד (docs/CYTOSCAPE-NOTES.md):
1. איך מאתחלים Cytoscape בתוך React component
2. ניהול state — מתי React state, מתי Cytoscape פנימי, איך מסנכרנים
3. custom node styling (צבע לפי סוג IOC, badge לפי confidence)
4. ה-pitfalls הנפוצים
5. ביצועים עם הרבה nodes

אל תכתוב קוד של הפרויקט עדיין. רק תלמד אותי את הכלי, במונחים פשוטים.
```

---

## שלב 3.2 — תכנון ארכיטקטורת הגרף המסווג

**מה עושים:** מתכננים את ה-data flow ואת ה-Ghost Edge policy — איך nodes מסוננים לפי clearance *לפני* שמגיעים ל-frontend.

**מודל:** 🔴 **Opus** (החלטת data flow + security)

**הפרומפט:**
```
נתכנן את ארכיטקטורת הגרף המסווג (docs/WAVE-3-DESIGN.md).

האתגר: הגרף חייב לכבד ABAC. node שדורש clearance גבוה יותר — המשתמש לא רואה
בכלל (Strict), או רואה Ghost Edge (Connectivity Hint). זו ההחלטה מ-PRD-v2 סעיף 15.5.

תכנן:
1. data flow: DB → API (מסונן לפי clearance) → Cytoscape
2. הסינון קורה ב-backend — frontend לעולם לא מקבל node אסור
3. Ghost Edge: Strict (default) vs Connectivity Hint per-investigation
4. Display Modes (Operational/Forensic) + Layer toggles
5. שמירת מצב הגרף + ביצועים עם 200+ nodes

קריטי: סינון ב-backend ולא ב-frontend. node מסווג שמגיע ל-browser ו"מוסתר" ב-CSS
= דליפה. ה-data לא יוצא מה-server. נאשר לפני קוד.
```

**מה לבדוק:** שהסינון ב-backend. אם node מסווג מגיע ל-browser ומוסתר ב-CSS — זו דליפה קלאסית.

---

## שלבים 3.3-3.8 — בנייה הדרגתית

**מה עושים:** בונים את הגרף ב-steps קטנים. כל step נבדק לפני הבא.

**מודל:** 🟡 **Sonnet** לרוב, **🔴 Opus** לבאג גרף קשה או ל-clearance filtering

**הפרומפט (לכל step):**
```
בוא נעשה Step [אות]: [תיאור]. צעד-צעד, diff קטן, E2E test, אישור לפני הבא.

Step A: Cytoscape רץ עם data דמה סטטי
Step B: טעינת investigation אמיתי מה-API (כבר מסונן לפי clearance)
Step C: click על node → details panel
Step D: double-click → enrich this node → nodes חדשים
Step E: שמירת מצב הגרף ל-DB
Step F: Ghost Edge rendering (לפי ה-mode)
Step G: Display Modes + Layer toggles

ל-Step B ו-F (clearance): denial test ש-node מסווג לא מגיע ל-frontend.
```

**כשנתקעים בבאג גרף (שכיח ב-Cytoscape):** עבור ל-🔴 Opus + Prompt #5 (Bug template) מ-PROMPTS.md.

---

## שלב 3.9 — Security Audit + Decision Point גדול

**מה עושים:** נקודת העצירה החשובה ביותר — זה ה-MVP המקורי. עצור ושאל אם אתה משתמש בכלי.

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
סיימנו גל 3. self-review + security audit ספציפי לגרף:
- node מסווג אף פעם לא מגיע ל-frontend? תוכיח עם network inspection
- Ghost edges לא מדליפים יותר מדי (timing, count)?
- pivot על node לא חושף nodes מעבר ל-clearance?
- ביצועים עם 200+ nodes סבירים?
- מצב הגרף נשמר ונטען נכון אחרי refresh?

Decision Point גדול: זה היה ה-MVP המקורי. האם אני משתמש בכלי בעבודה?
כמה פעמים השבוע? מה הכי עזר? מה הכי הפריע?
המלצה מנומקת: (א) ממשיכים לגל 4 (ב) משפרים קודם (ג) עוצרים — יש לי כלי שלם.
```

**🛑 נקודת עצירה מרכזית:** אם אתה משתמש בכלי — מצוין, המשך. אם לא — עצור, יש לך כלי TI ויזואלי שלם. זו הצלחה.

---
---

# 🌊 גל 4 — Knowledge Base
### תוצאה: KB ארגוני עם STIX 2.1, versioning, decay, חיפוש — הכל מסווג.

---

## שלב 4.1 — תכנון KB (כל הגל)

**מה עושים:** מתכננים את כל גל 4 ומפרקים לתת-גלים. מבצעים תת-גל אחד בכל פעם.

**מודל:** 🔴 **Opus** (design גדול + STIX + classification)

**הפרומפט:**
```
מתחילים גל 4: Knowledge Base. קרא PRD-v2 סעיפים 9, 12, 16 (KB, Continuity, STIX).

נחלק לתת-גלים:
4a: KB CRUD בסיסי עם STIX 2.1 objects + classification
4b: Versioning + audit (revoked, לא deleted)
4c: Promote מ-investigation ל-KB (confirmation + undo window)
4d: Search (exact + full-text) עם clearance filtering
4e: Confidence decay + auto-revalidation
4f: Sighting → Indicator aggregation

תכנן את כל הגל (docs/WAVE-4-DESIGN.md), אבל נבצע תת-גל אחד בכל פעם.
לכל object: classification + TLP. search לא מדליף objects מעל clearance.
נאשר את ה-design הכללי, ואז נתחיל מ-4a.
```

---

## שלבים 4.2-4.7 — ביצוע תת-גלים

**מה עושים:** בונים כל תת-גל בנפרד (4a עד 4f).

**מודל:** 🟡 **Sonnet** לרוב, **🔴 Opus** ל-4d (search filtering — leak-prone) ול-4e (decay logic)

**הפרומפט (לכל תת-גל):**
```
בוא נבנה תת-גל [4x]: [תיאור].
צעד-צעד, diff קטן, E2E test לכל פיצ'ר, אישור ביניהם.

ל-4d (search): denial test ש-search לא מחזיר ולא סופר objects מעל clearance.
זה leak surface קלאסי — search שמחזיר "0 results" כשיש תוצאה מסווגת בסדר,
אבל search שמחזיר "you don't have access to 3 results" מדליף.
```

---

## שלב 4.8 — Decision Point של גל 4

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
סיימנו גל 4. self-review + security check (דגש על search leak surfaces).
Decision Point: יש לי עכשיו זיכרון ארגוני. אני משתמש בו?
המלצה: ממשיכים לגל 5, או משפרים?
```

**🛑 נקודת עצירה 4:** יש לך מערכת עם KB. ידע עובר מחקירה לחקירה.

---
---

# 🌊 גל 5 — Triage & Workflow
### תוצאה: Inbox + שלוש הזרימות המלאות + Templates + Living Report. מערכת workflow מלאה.

---

## שלב 5.1 — תכנון Workflows (כל הגל)

**מה עושים:** מתכננים את כל גל 5 — שלוש הזרימות מ-PRD-v2 — ומפרקים לתת-גלים.

**מודל:** 🔴 **Opus** (design גדול)

**הפרומפט:**
```
מתחילים גל 5: Triage & Workflow. קרא PRD-v2 סעיפים 6, 7, 8 (שלוש הזרימות).

תת-גלים:
5a: Triage Inbox + Quick Add + Source Reliability tiers
5b: 5 Entry Points ל-investigation + Templates
5c: Resume Context (welcome back, auto-save)
5d: Living Report (מתעדכן תוך כדי)
5e: Decision support (recommendations — rule-based, לא ML)
5f: FP feedback loop
5g: Cross-investigation discovery

תכנן (docs/WAVE-5-DESIGN.md). כל זרימה מודעת-clearance — Inbox מציג רק
IOCs שהמשתמש מורשה לראות. נאשר ונתחיל מ-5a.
```

---

## שלבים 5.2-5.8 — ביצוע תת-גלים

**מה עושים:** בונים כל תת-גל (5a עד 5g).

**מודל:** 🟡 **Sonnet** לרוב, **🔴 Opus** ל-5g (cross-investigation — נוגע ב-clearance בין חקירות)

**הפרומפט (לכל תת-גל):**
```
בוא נבנה תת-גל [5x]: [תיאור].
צעד-צעד, diff קטן, E2E test, אישור ביניהם.
פיצ'רים שמציגים data מרובות-חקירות: denial test לסינון clearance.
```

---

## שלב 5.9 — Decision Point של גל 5

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
סיימנו גל 5. self-review + security check.
Decision Point משמעותי: יש לי עכשיו מערכת TI מלאה ל-single user.
גל 6 פותח multi-user — צעד גדול ורגיש ל-security.
האם אני משתמש בכלי? האם יש צורך אמיתי ב-multi-user, או single-user מספיק לי?
המלצה: ממשיכים לגל 6, או שזה המקום לעצור עם מערכת single-user שלמה?
```

**🛑 נקודת עצירה משמעותית:** אם אין צורך ב-multi-user — זה מקום מצוין לעצור. יש לך מערכת TI שלמה.

---
---

# 🌊 גל 6 — Collaboration
### תוצאה: multi-user + real-time + sharing מאובטח + handoff. הגל הכי רגיש ל-security.

---

## שלב 6.1 — תכנון Collaboration (security-critical)

**מה עושים:** מתכננים בזהירות מקסימלית — multi-user + classified = כל באג הוא דליפה בין משתמשים.

**מודל:** 🔴 **Opus** (אין פשרות — הגל הכי מסוכן)

**הפרומפט:**
```
מתחילים גל 6: Collaboration. הגל הכי רגיש ל-security בכל הפרויקט.
multi-user + classified = כל באג הוא דליפה בין משתמשים.

קרא PRD-v2 סעיף 13 (Collaboration) + 15 (ABAC) שוב.

תכנן בזהירות מקסימלית (docs/WAVE-6-DESIGN.md):
1. Real-time sync (WebSocket) — איך לא מדליפים nodes מסווגים ב-broadcast?
2. שני משתמשים באותה חקירה עם clearance שונה — כל אחד רואה view שונה
3. Invitation-only + roles (owner/editor/viewer)
4. Conflict resolution (conversation threads + diff)
5. Soft locking + structured handoff (4 types)
6. State machine + edge cases (orphaned, stale, timeout)

הסכנה הגדולה: WebSocket broadcast ששולח node מסווג לכל המחוברים, כולל מי שאסור לו.
תכנן per-user filtering על כל broadcast. נדון בזה לעומק לפני קוד.
```

**מה לבדוק:** שכל broadcast מסונן per-recipient. WebSocket עם payload אחיד לכולם = דליפה.

---

## שלבים 6.2-6.8 — ביצוע (זהירות מוגברת)

**מה עושים:** בונים את ה-collaboration. כל מה שנוגע ל-real-time filtering ו-sharing הוא Opus.

**מודל:** 🔴 **Opus** ל-real-time filtering ו-sharing, 🟡 **Sonnet** ל-UI בלבד

**הפרומפט (לכל חלק):**
```
בוא נבנה [החלק]. security-critical.
לכל פיצ'ר: denial test מקיף. במיוחד — שני משתמשים עם clearance שונה באותה חקירה
לא רואים אחד את ה-data של השני מעבר להרשאה. Red-Green: denial test נכשל לפני המימוש.
```

---

## שלב 6.9 — Security Audit מקיף

**מה עושים:** ה-security audit הכי מקיף עד כה. כאן דליפה הכי סבירה.

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
סיימנו גל 6. security audit הכי מקיף:
- penetration test מחשבתי: איך משתמש זדוני ינסה לראות data של אחר?
- WebSocket: כל broadcast מסונן per-recipient? race condition שמדליף?
- sharing: אפשר לשתף רק מה שמותר? TLP:RED לא ניתן לשיתוף?
- handoff: receiver מקבל רק מה שמותר לו?

אל תמשיך לגל 7 עד שה-security של גל 6 הוכח. תן לי דוח ממצאים מפורט.
```

**🛑 נקודת עצירה 6:** אל תמשיך עד שה-security הוכח. כאן הסיכון הכי גבוה.

---
---

# 🌊 גל 7 — Operationalize & Scale
### תוצאה: actions + ISAC + multi-tenant + production hardening. המערכת המלאה.

---

## שלב 7.1 — תכנון Scale (כל הגל)

**מה עושים:** מתכננים את הגל האחרון — actions, sharing חיצוני, multi-tenancy, ו-production readiness.

**מודל:** 🔴 **Opus** (multi-tenancy = isolation critical)

**הפרומפט:**
```
מתחילים גל 7: Operationalize & Scale. הגל האחרון. קרא PRD-v2 סעיפים 8, 17.

תת-גלים:
7a: Action Outputs (blocklist, Sigma/YARA export, hunting queries)
7b: External Sharing / ISAC / Trust Circles (עם anonymization)
7c: Multi-tenancy מלא (tenant isolation)
7d: TAXII server
7e: Production hardening (backup, DR, monitoring, secret management)

תכנן (docs/WAVE-7-DESIGN.md). הקריטי ביותר: multi-tenancy + ABAC =
tenant isolation מושלם. tenant A לא רואה כלום מ-tenant B, ובתוך כל tenant
ה-clearance עדיין נאכף. נאשר ונתחיל מ-7a.
```

---

## שלבים 7.2-7.8 — ביצוע תת-גלים

**מה עושים:** בונים כל תת-גל (7a עד 7e).

**מודל:** 🔴 **Opus** ל-7b (ISAC anonymization) ו-7c (multi-tenancy) — leak-critical. 🟡 **Sonnet** לשאר.

**הפרומפט (לכל תת-גל):**
```
בוא נבנה תת-גל [7x]: [תיאור]. צעד-צעד, diff קטן, E2E test.

ל-7b (anonymization): test שמוכיח ש-PII ו-internal IPs מוסרים לפני sharing.
ל-7c (multi-tenancy): cross-tenant denial test — tenant A לא רואה כלום מ-tenant B.
```

---

## שלב 7.9 — Final Security Audit + Production Readiness

**מה עושים:** הבדיקה הסופית לפני production עם classified data אמיתי.

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
המערכת המלאה בנויה. final security audit לפני production עם classified data אמיתי:

1. עבור על כל leak surface מ-SECURITY-MODEL.md — כולם חסומים? תוכיח כל אחד.
2. tenant isolation מושלם? cross-tenant test.
3. clearance enforcement בכל endpoint? tabulate כל endpoint וה-policy שלו.
4. audit log שלם וimmutable?
5. backup/DR נבדקו בפועל (לא רק הוגדרו)?
6. secret management — אין key ב-git, אין key ב-logs?

תיצור docs/SECURITY-AUDIT-FINAL.md עם הממצאים.
המלצה: האם המערכת מוכנה ל-classified data אמיתי? אם לא — מה חסר?
```

**🛑 נקודת עצירה 7:** המערכת המלאה. לפני classified data אמיתי — ודא שה-audit הסופי נקי.

---
---

# 🔁 שגרות קבועות (לאורך כל הגלים)

## שגרת באג
**מודל:** 🟡 Sonnet (רגיל) / 🔴 Opus (קשה או חוזר)
השתמש ב-Prompt #5 (Bug Report) מ-PROMPTS.md.

## שגרת Security Check שבועי
**מודל:** 🔴 Opus
```
security check שבועי. עבור על מה שבנינו השבוע:
- endpoint חדש? עובר דרך ה-Policy Engine?
- מקום חדש שמציג data? מסונן לפי clearance?
- leak surface חדש (count, error, log)? חסום?
תן לי רשימת ממצאים ותיקונים נדרשים.
```

## שגרת learning
**מודל:** 🟡 Sonnet / 🔴 Opus (מושג מורכב)
השתמש ב-Prompt #10 (Learning Mode) מ-PROMPTS.md.

---

# 📊 סיכום — כמה Opus באמת צריך?

בפרויקט מסווג, חלק ה-Opus גדול מהרגיל. הנה הפילוח המשוער:

| סוג עבודה | מודל | % מהזמן |
|---|---|---|
| תכנון גלים + security design | 🔴 Opus | ~15% |
| קוד security/clearance/RLS | 🔴 Opus | ~20% |
| Decision Points + audits | 🔴 Opus | ~5% |
| כתיבת קוד רגיל + UI | 🟡 Sonnet | ~45% |
| tests + refactoring | 🟡 Sonnet | ~10% |
| wrap-ups + commits | 🟢 Haiku | ~5% |

**~40% Opus** בפרויקט הזה (לעומת ~15% בפרויקט רגיל). זה המחיר של classified data — וזו השקעה נכונה, כי דליפה עולה הרבה יותר.

---

**זה המדריך המלא. כל שלב, כל פרומפט, כל מודל. הצעד הבא: שלב 1.0 — הקמת חשבונות.**
