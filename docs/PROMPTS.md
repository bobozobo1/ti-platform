# PROMPTS.md — חבילת Prompts מוכנה לשימוש

> **איך להשתמש:** העתק את ה-prompt המתאים לתחילת ה-session המתאימה. החלף `[בסוגריים]` בערכים האמיתיים שלך.

---

## 🚀 Prompt #0 — Session Opener (להשתמש בכל שיחה חדשה)

```
שלום Claude. אני [שם], חוקר TI שבונה מערכת investigation אישית.

לפני שנתחיל, אני צריך שתעשה את הצעדים הבאים בסדר:

1. תקרא את הקובץ docs/CLAUDE_CONTEXT.md — זה ה-source of truth שלנו.
2. תקרא את docs/PRD-MVP.md — מה אנחנו בונים.
3. תקרא את docs/DECISIONS.md — החלטות שכבר קיבלנו.
4. תאשר לי שאתה מבין את:
   - מה אנחנו בונים
   - מי המשתמש (אני)
   - הסטאק הטכני
   - באיזה Phase אנחנו (זה כתוב ב-CLAUDE_CONTEXT.md סעיף 8)

אחרי האישור, נמשיך למשימה. אל תתחיל לכתוב קוד עד שאני אומר.
```

**מה לעשות אחרי שClaude מאשר:**
שאל: "יש משהו ב-context שלא היה ברור או נראה סותר?" — אם יש, תבהיר לפני שמתחילים.

---

## 🏗 Prompt #1 — Phase 0 Kickoff (Foundation)

```
אנחנו מתחילים Phase 0 — Foundation.

המטרה של ה-phase הזה: להקים את כל ה-infrastructure הבסיסי. בלי עדיין שום פיצ'ר TI.

acceptance criteria ל-Phase 0:
1. Repo קיים ב-GitHub עם המבנה שמתואר ב-CLAUDE_CONTEXT.md סעיף 5
2. Frontend ריק (React + Vite + TS + Tailwind) deployed ל-Vercel
3. Backend ריק (FastAPI) עם /health endpoint, deployed ל-Railway
4. Supabase project יצור, עם schema ראשוני (טבלת users)
5. Login עם magic link עובד end-to-end (אני יכול להירשם וללוגאון)
6. GitHub Actions: lint + tests רצים על כל PR
7. .env.example מתועד עם כל המפתחות שצריך

אני רוצה שתעשה את זה בסדר הבא, ובכל צעד תעצור ותאשר איתי לפני שתמשיך:

צעד 1: תיצור לי checklist מסודר של כל הצעדים, עם הערכת זמן לכל אחד.
צעד 2: נתחיל מ-repo init + frontend ריק deployed.
צעד 3: backend ריק deployed.
צעד 4: Supabase + schema.
צעד 5: Login flow.
צעד 6: CI/CD.

בכל צעד, תיתן לי הוראות מדויקות מה ללחוץ, איפה, ומה להעתיק. אני לא יודע פיתוח, אז תניח אפס ידע מקדים.

חשוב מאוד: אל תכתוב קוד מורכב. הכל מינימלי. נוסיף דברים בPhases הבאים.

מה השאלה הראשונה שלך לפני שמתחילים?
```

---

## 🔌 Prompt #2 — Phase 1 Kickoff (Single IOC Lookup)

```
התחלנו Phase 1: Single IOC Lookup.

המטרה: משתמש מקליד IOC, רואה enrichment results מ-3 sources.

acceptance criteria מלא ב-PRD-MVP.md סעיף "Phase 1".

לפני שאנחנו מתחילים לקודד, אני רוצה שתעשה את הצעדים הבאים:

1. תקרא את ה-acceptance criteria ב-PRD-MVP.md
2. תיצור design document קצר (`docs/PHASE-1-DESIGN.md`) שמתאר:
   - איך ה-frontend יראה (wireframe מילולי)
   - מה ה-API endpoints שבackend נצטרך
   - מה ה-database schema (טבלאות חדשות)
   - איך נטפל ב-rate limits של VT/AbuseIPDB
   - איך נטפל בשגיאות של APIs חיצוניים
3. תציג לי את ה-design ותחכה לאישור שלי
4. אחרי שאני מאשר — נחלק ל-tasks קטנים

עוד דבר חשוב: לפני שאתה כותב כל שורת backend code שמתחבר ל-API חיצוני, תכתוב mock service קודם. ככה אני יכול לבדוק את ה-frontend בלי לבזבז API quota על free tier.

מה השאלות שלך?
```

---

## 💾 Prompt #3 — Phase 2 Kickoff (Persistence & History)

```
התחלנו Phase 2: Persistence & History.

ב-Phase 1 בנינו lookup חד-פעמי. עכשיו כל lookup נשמר ויש history.

acceptance criteria:
1. כל lookup שמתבצע נשמר אוטומטית ל-DB כ-investigation
2. ב-sidebar רואים רשימת investigations אחרונים (20 last)
3. לחיצה על investigation בhistory טוענת את התוצאות שלו
4. יש search field שמחפש ב-history (full text על IOC value + tags)
5. יש כפתור "Re-run" שמריץ את ה-enrichment שוב ומשווה
6. יש שדה tags חופשי על כל investigation

לפני שמתחילים:

1. תקרא את ה-Phase 1 code שכתבנו ותסכם בקצרה מה כבר יש לנו
2. תציע schema לטבלאות חדשות (investigations, tags) — אבל פשוט. אל תוסיף שדות "אולי בעתיד".
3. תציע איך נראה ה-UI החדש — wireframe מילולי
4. נחכה לאישור שלי לפני שכותבים קוד

חשוב: אם הוספת dependencies חדשות, תעדכן CLAUDE_CONTEXT.md סעיף 4 (Stack).

מה השאלות?
```

---

## 🕸 Prompt #4 — Phase 3 Kickoff (Investigation Graph)

```
התחלנו Phase 3: Investigation Graph. זה ה-phase הכי מורכב טכנית.

המטרה: tabular results הופכים לגרף ויזואלי אינטראקטיבי.

acceptance criteria מלא ב-PRD-MVP.md.

לפני שמתחילים, חובה:

1. תקרא Cytoscape.js docs ו-best practices. תכתוב לי סיכום של 1 עמוד עם:
   - איך מאתחלים Cytoscape ב-React
   - איך מטפלים בstate (מתי React state, מתי Cytoscape פנימי)
   - איך עושים custom node styling
   - מה ה-pitfalls הנפוצים
2. תציע לי את הארכיטקטורה: איך data flow עובד מ-DB → API → React → Cytoscape
3. נדבר על הarchitecture לפני שכותבים שורה אחת
4. כשמתחילים לכתוב — נחלק לsteps קטנים מאוד:
   - Step A: Cytoscape רץ עם static data דמה
   - Step B: load investigation data מ-API
   - Step C: node interaction (click → details panel)
   - Step D: pivot (double-click → enrich)
   - Step E: save graph state

בכל step אני בודק שזה עובד לפני שעוברים לבא.

חשוב: ה-phase הזה יכול לקחת 4 שבועות. אל תנסה לדחוף הכל לsession אחת.

יש שאלות לפני שמתחילים?
```

---

## 🐛 Prompt #5 — Bug Report Template

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

**Network tab errors (אם רלוונטי):**
[failed request URL + status code + response]

**Screenshot (אם רלוונטי):**
[paste image]

**מתי זה התחיל:**
[לדוגמה: אחרי השינוי של אתמול ל-X, או: זה תמיד היה ככה]

לפני שאתה מתחיל לתקן:
1. תן לי 3 hypotheses אפשריות, מהכי סבירה לפחות סבירה
2. לכל hypothesis, איך נוכל לאשש או לשלול אותה (בלי לכתוב קוד עדיין)
3. אחרי שאני בוחר hypothesis לחקור — נתחיל
```

---

## 🔍 Prompt #6 — Code Review (בלי לקרוא קוד)

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

**Security:**
- האם יש user input שלא validating?
- האם יש מקום שבו secrets יכולים להידלף ל-frontend?
- האם יש SQL injection risk? XSS risk?

**Tests:**
- כתבת E2E test? תראה לי את ה-test code.
- האם ה-test באמת בודק את ההתנהגות או רק את הקוד?
- מה ה-test לא מכסה?

**מה היית משנה:**
- אם היית מתחיל מחדש, מה היית עושה אחרת?
- מה ה-tech debt הראשי שיצרת?

תהיה כן. אם יש בעיות — אני מעדיף לשמוע עכשיו ולא בproduction.
```

---

## 📝 Prompt #7 — End of Session Wrap-up

```
סיימנו את ה-session. לפני שנסגור, תבצע את ה-wrap-up הבא:

1. **עדכן את `docs/CLAUDE_CONTEXT.md`:**
   - סעיף 8 (Status) — מה עובד עכשיו, מה בעבודה
   - סעיף 8 (Known Issues) — אם יש דברים שדחינו
   - סעיף 9 (DON'Ts) — אם משהו לא עבד וניסינו

2. **עדכן את `docs/DECISIONS.md`:**
   - אם החלטנו משהו טכני בsession הזה, תוסיף entry בפורמט:
     ```
     ### YYYY-MM-DD — [שם ההחלטה]
     **Context:** [למה היה צריך להחליט]
     **Decision:** [מה החלטנו]
     **Alternatives considered:** [מה לא בחרנו ולמה]
     **Trade-offs:** [מה זה עולה לנו]
     ```

3. **תיצור `SESSION-NOTES.md` (overwrite כל פעם):**
   - מה עשינו בsession
   - מה עוד צריך לעשות (TODO)
   - blockers
   - מה ה-next session אמורה להתחיל ממנו

4. **תיצור git commit עם הודעה תקנית** (לא תעשה push, רק commit מקומי)

5. **תסכם לי ב-3 משפטים:**
   - מה עשינו
   - מה השאלה הכי גדולה שנותרה פתוחה
   - מה הצעד הבא

תבצע את כל הצעדים האלה.
```

---

## 🚨 Prompt #8 — "אני תקוע / משהו השתבש"

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
   - DB issue
   - external API issue
   - auth issue
   - environment / deployment issue
   - browser cache
3. לכל ענף בעץ, איך נדע אם זה השורש?
4. תציע לי order לבדיקה מהפשוט ביותר לבדוק לקשה ביותר
5. נתחיל מהראשון

חשוב: אל תכתוב fix עד שאני מאשר את ההיפותזה.
```

---

## 🎯 Prompt #9 — Decision Point Review (סוף Phase)

```
הגענו לסוף [Phase X]. זמן ל-Decision Point פורמלי.

תעזור לי לעשות retrospective ולהחליט אם להמשיך:

**1. Actuals vs. Plan:**
- כמה זמן לקח בפועל ל-phase הזה? (vs. הערכה)
- אילו features לא הספקנו? למה?
- אילו features הוספנו שלא תכננו? למה?

**2. Quality:**
- כמה bugs נפתחו במהלך ה-phase?
- כמה מהם נפתרו? כמה עדיין פתוחים?
- ה-test coverage שלנו? (run pytest --cov)

**3. The Real Question:**
- האם אני משתמש בכלי בעבודה האמיתית שלי? כמה פעמים בשבוע האחרון?
- מה הדבר שעשה לי הכי הרבה רושם? למה?
- מה הדבר שהכי החלשני? למה?
- אם הייתי מתחיל מחדש היום, מה הייתי עושה אחרת?

**4. Tech Debt Inventory:**
- מה ה-tech debt שצברנו? תיצור רשימה מפורטת.
- מה ממנו חיוני לטפל לפני Phase הבאה?
- מה יכול לחכות?

**5. Recommendation:**
על סמך כל הנ"ל, תן לי המלצה מנומקת:
- (א) להמשיך ל-Phase הבאה
- (ב) לעצור ולשפר את הקיים לפני שממשיכים
- (ג) לעצור לגמרי — המוצר לא עומד בציפיות

אל תפחד להמליץ על (ב) או (ג). אני רוצה אמת.
```

---

## 📚 Prompt #10 — Learning Mode (כשאני רוצה להבין משהו)

```
[שאלה טכנית]

לפני שאתה עונה, אני רוצה להזכיר:
- אני לא מפתח. הסבר לי במונחים פשוטים.
- אם יש מונח טכני, תסביר אותו בפעם הראשונה שמופיע.
- אל תניח שיש לי ידע מקדים.
- תן דוגמה קונקרטית מהפרויקט שלנו, לא דוגמה כללית.

אחרי ההסבר, תשאל אותי: "מה לא ברור?" — אני רוצה להרגיש בנוח לחזור על שאלה.
```

---

## 🔧 שימוש מומלץ של הPrompts

**בכל יום:**
- פתח עם Prompt #0
- אם משימה חדשה → Prompt #1/2/3/4 לפי Phase
- אם באג → Prompt #5
- אם תקוע → Prompt #8
- אם רוצה ללמוד → Prompt #10
- סגור עם Prompt #7

**פעם בשבוע:**
- לעבור על SESSION-NOTES של השבוע
- לראות אם DECISIONS.md מתחיל להיראות עמוס מדי

**סוף Phase:**
- Prompt #9 חובה. אל תדלג עליו, גם אם זה מרגיש מיותר.

---

**זכור:** Prompts הם נקודת התחלה. כשאתה מבין יותר את הזרימה, אתה תפתח prompts משלך. הקובץ הזה הוא scaffolding, לא חוק.
