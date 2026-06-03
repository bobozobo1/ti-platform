# 🌊 MASTER-PLAN.md
## תוכנית הפרויקט המלאה — שבעת הגלים

> זו התוכנית הגדולה. כל המערכת מ-PRD-v2, מאורגנת ב-**גלים** (Waves).
> כל גל מסתיים במוצר שלם ושמיש שאפשר לעצור בו.
> נבנה solo (אתה + Claude), עם ABAC/classified כאבן יסוד מהיום הראשון.

---

## 📐 העיקרון המארגן — Waves

המערכת בנויה ב-**7 גלים**, לא ב-phases מסורתיות. ההבדל קריטי:
- **Phases** — תכנון לפי פיצ'רים. סוף phase = אוסף features שאולי לא מרכיבים מוצר שלם.
- **Waves** — תכנון לפי **מוצרים שמישים**. סוף כל גל = משהו שאפשר להשתמש בו ביום-יום.

**הכלל:** בסוף כל גל יש לך מוצר שלם שאפשר להשתמש בו, להראות אותו, ולעצור בו בלי בושה. אין "חצי פיצ'ר". אם נגמר לך הכוח אחרי גל 3 — יש לך מוצר אמיתי, לא שלד.

**מסמך משלים:** הביצוע המפורט (שלב-שלב, פרומפט מדויק, ובחירת מודל) ב-`EXECUTION-GUIDE.md`. המסמך הזה הוא תמונה אסטרטגית; ה-EXECUTION-GUIDE הוא היומיומי.

---

## ⚠️ קריאת מציאות — קרא פעם אחת, אל תשכח

**הסקופ המלא הוא מערכת enterprise.** ABAC, multi-tenancy, real-time collaboration, STIX 2.1 מלא, TAXII, ISAC sharing. זה פרויקט רב-שנתי לאדם אחד, גם עם Claude ובקצב טוב.

**זה בסדר גמור** — בתנאי שאתה מבין את המשמעות:
- **לוח הזמנים נמדד בשנים, לא חודשים.** בקצב של ~6 שעות שבועיות, התוכנית המלאה היא מסע של 2.5-4 שנים.
- **נקודות העצירה הן לא כישלון.** אם תעצור אחרי גל 4 עם מוצר שאתה משתמש בו — זו הצלחה, לא ויתור.
- **ABAC מעלה את הרף.** security-critical code דורש זהירות מיוחדת. נבנה אותו עם בדיקות אגרסיביות.
- **המדד היחיד שחשוב:** האם אתה משתמש בכלי בעבודה האמיתית. אם לא — שום כמות features לא תציל את הפרויקט.

---

# 🗺️ מבט-על — שבעת הגלים

| גל | שם | תוצאה שמישה | משך מוערך* | תלות ABAC |
|---|---|---|---|---|
| **1** | Secure Foundation | login + הרשאות עובדות | 4-6 שבועות | הליבה נבנית כאן |
| **2** | Enrichment Core | IOC lookup עם clearance | 4-6 שבועות | כל lookup מסונן |
| **3** | Investigation Graph | גרף ויזואלי מסווג | 8-10 שבועות | nodes מסוננים לפי clearance |
| **4** | Knowledge Base | KB עם STIX + decay | 6-8 שבועות | objects מסווגים |
| **5** | Triage & Workflow | Inbox + flows מלאים | 6-8 שבועות | triage מודע-הרשאות |
| **6** | Collaboration | multi-user + sharing מאובטח | 8-10 שבועות | קריטי ל-security |
| **7** | Operationalize & Scale | actions + ISAC + multi-tenant | 10-12 שבועות | ABAC enforced cross-tenant |

*בהנחת ~6 שעות שבועיות. המציאות תהיה איטית יותר — נורמלי.*

**סך הכל מוערך:** ~46-60 שבועות עבודה אפקטיבית, מתפרסים על 2.5-4 שנים קלנדריות.

---

## 🔐 עקרון-על: Security-First Architecture

מאחר ש-ABAC הוא אבן יסוד, **כל גל בנוי סביב שלושה כללי ברזל:**

1. **Default Deny** — כל גישה נדחית כברירת מחדל. גישה ניתנת רק כשכל תנאי ההרשאה מתקיימים.
2. **Test the Denial** — לכל פיצ'ר, ה-test הראשון מוכיח ש*משתמש לא מורשה לא רואה את המידע*. לא רק שמורשה כן רואה.
3. **No Leak Surfaces** — מידע מסווג לא דולף דרך: error messages, counts, search results, autocomplete, logs, או timing. כל אחד מאלה הוא vector.

**אלה מודגשים בכל גל. אל תדלג על ה-denial tests — הם הלב של מערכת מסווגת.**

---

═══════════════════════════════════════════
# 🌊 גל 1 — Secure Foundation
═══════════════════════════════════════════

> **תוצאה שמישה:** מערכת עם login, ניהול משתמשים, ומנוע הרשאות ABAC עובד. עדיין אין פיצ'רי TI — אבל יש את התשתית שעליה הכל נבנה.

**למה זה מוצר שלם:** גם בלי TI, יש לך מערכת מאובטחת עם clearance levels שאפשר להדגים. זה ה-proof שה-security model עובד.

## 1.1 — תכנון ה-Security Model

**מודל:** 🔴 **Opus** (זו ההחלטה הכי חשובה בכל הפרויקט)

**הפרומפט:**
```
אנחנו מתחילים את הפרויקט המלא. אבן היסוד היא ABAC — המערכת חייבת לתמוך
ב-classified data מהיום הראשון. זה משפיע על כל שורת קוד בהמשך.

לפני כל קוד, תכנן איתי את ה-Security Model. תקרא את PRD-v2.md סעיף 15 (ABAC).

תיצור docs/SECURITY-MODEL.md שעונה על:
1. שלושת ממדי ההרשאה (Clearance, TLP, Permissions) — איך כל אחד מיוצג ב-DB
2. ה-Policy Engine — איך נבדקת כל בקשת גישה (ה-AND הלוגי)
3. Default Deny — איך מבטיחים שברירת המחדל היא דחייה
4. Leak surfaces — רשימה מלאה של כל המקומות שמידע יכול לדלוף
   (errors, counts, search, autocomplete, logs, timing) ואיך חוסמים כל אחד
5. איך Supabase RLS משתלב עם ABAC — מה ב-DB layer, מה ב-application layer
6. איך נבדוק את כל זה (testing strategy ל-security)

זו ההחלטה הכי קריטית בפרויקט. קח את הזמן. הצג לי את ה-design ונדון בו לעומק
לפני שכותבים שורה אחת. שאל אותי שאלות על המודל הארגוני שלי אם צריך.
```

**מה לבדוק:** שה-design מתייחס מפורשות ל-leak surfaces (לא רק "מי רואה מה" אלא "איך מידע *לא* דולף"). זה ההבדל בין מערכת מסווגת אמיתית לצעצוע.

## 1.2 — תשתית בסיסית (repo + deployment, עם security מההתחלה)

**מודל:** 🔴 **Opus** לתכנון, 🟡 **Sonnet** לביצוע

מבצעים את צעדי התשתית הבסיסיים (repo, frontend, backend, deployment, CI/CD), **בתוספת:**

**הפרומפט (אחרי ה-foundation הבסיסי):**
```
התשתית הבסיסית עומדת. עכשיו נבנה את שכבת ה-ABAC לפי SECURITY-MODEL.md.

צעד-צעד:
1. DB schema: users עם clearance_level, טבלת permissions, marking-definitions ל-TLP
2. Supabase RLS policies שמיישמות Default Deny
3. Policy Engine ב-backend — פונקציה מרכזית שכל endpoint עובר דרכה
4. Middleware שמיישם את הבדיקה על כל request

לכל צעד: קוד + test. ה-test הראשון לכל policy חייב להיות denial test —
שמוכיח שמשתמש לא מורשה *לא* מקבל גישה. נראה אותו נכשל לפני המימוש ועובר אחרי.
```

## 1.3 — User Management + Clearance

**מודל:** 🔴 **Opus** (security-critical)

**הפרומפט:**
```
נבנה את ניהול המשתמשים עם clearance levels.

acceptance criteria:
1. Admin יכול ליצור משתמש עם clearance level (UNCLASSIFIED → TOP SECRET)
2. Admin יכול לשנות clearance, וזה מתועד ב-audit log
3. משתמש רואה רק את מה שה-clearance שלו מתיר
4. כל שינוי הרשאה = audit log entry (who, what, when, old/new)

חשוב: תכתוב denial tests — משתמש CONFIDENTIAL מנסה לגשת ל-SECRET object,
גם דרך UI וגם דרך API ישירות, ומקבל "not found" (לא "access denied" — כי
"access denied" עצמו מדליף שה-object קיים).
```

## 1.4 — Audit Log Foundation

**מודל:** 🟡 **Sonnet**

**הפרומפט:**
```
נבנה את תשתית ה-audit log (immutable).

acceptance criteria:
1. כל פעולת הרשאה מתועדת: clearance changes, access grants, denials, exports
2. ה-log הוא append-only — אי אפשר לערוך או למחוק entries
3. כל entry: timestamp, user, action, resource, result, reason
4. denials מתועדים גם (ניסיון גישה שנכשל הוא event חשוב)

E2E test שמוכיח שה-log לא ניתן לעריכה.
```

## 1.5 — Self-Review + Decision Point

**מודל:** 🔴 **Opus**

```
סיימנו את גל 1 — Secure Foundation. self-review מעמיק עם דגש על security:

Security audit:
- עבור על כל leak surface מ-SECURITY-MODEL.md. כל אחד חסום? תוכיח.
- האם counts/pagination מדליפים קיום של objects מסווגים?
- האם error messages מבחינים בין "not found" ל-"access denied"?
- האם יש timing attack אפשרי?
- האם logs מכילים מידע מסווג בטקסט גלוי?

Decision Point: האם ה-security model יציב מספיק לבנות עליו את כל השאר?
אם יש ספק — נתקן עכשיו. לתקן security foundation בגל 5 זה אסון.
```

---

═══════════════════════════════════════════
# 🌊 גל 2 — Enrichment Core
═══════════════════════════════════════════

> **תוצאה שמישה:** משתמש מקליד IOC, מקבל enrichment מ-3+ מקורות, והכל מסונן לפי clearance. זה כבר כלי שמיש בעבודה.

**למה זה מוצר שלם:** אתה יכול להשתמש בזה כמו ב-MVP המקורי, אבל עם security model אמיתי מתחתיו.

## 2.1 — תכנון Enrichment עם Classification

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
מתחילים גל 2: Enrichment Core. כמו ה-IOC lookup מ-MVP, אבל עם ABAC.

האתגר החדש: לכל enrichment result יש classification. תוצאה מ-feed ציבורי =
UNCLASSIFIED. תוצאה ממקור פנימי רגיש = יכולה להיות CONFIDENTIAL ומעלה.

תכנן (docs/WAVE-2-DESIGN.md):
1. איך נקבע ה-classification של כל enrichment result?
2. איך משתמש רואה רק תוצאות ב-clearance שלו?
3. מה קורה כש-enrichment מחזיר חלק מהתוצאות מעל ה-clearance? (מסתירים בשקט)
4. mock-first: mocks לכל API החיצוני
5. rate limiting ו-error handling

נאשר לפני קוד.
```

## 2.2-2.5 — ביצוע

**מודל:** 🟡 **Sonnet** (ביצוע), 🔴 **Opus** (כל מה שנוגע לסינון לפי clearance)

זרימה: mocks → backend → frontend → real APIs. כל שלב כולל classification filtering.

**הפרומפט המרכזי:**
```
בוא נבנה את [החלק]. צעד-צעד, diff קטן, E2E test לכל פיצ'ר.

לכל פיצ'ר שמציג data: ה-test הראשון הוא denial test — משתמש עם clearance נמוך
לא רואה את התוצאות המסווגות, והן לא דולפות דרך count/error/search.
```

## 2.6 — Decision Point + בדיקת מציאות

**מודל:** 🔴 **Opus**

🎯 **בדיקת מציאות:** השתמש בכלי בעבודה אמיתית. עובד? המשך לגל 3.

---

═══════════════════════════════════════════
# 🌊 גל 3 — Investigation Graph
═══════════════════════════════════════════

> **תוצאה שמישה:** גרף ויזואלי אינטראקטיבי שמסנן nodes לפי clearance. הלב של המערכת.

**למה זה מוצר שלם:** זה ה-MVP המקורי שתכננו, עכשיו עם security. אם תעצור כאן — יש לך כלי TI ויזואלי אמיתי.

## 3.1 — לימוד Cytoscape + תכנון גרף מסווג

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
מתחילים גל 3: Investigation Graph. החלק הכי מורכב טכנית.
נשתמש ב-Cytoscape.js. קרא את הסיכום הטכני אם כבר עשינו, אחרת תלמד אותי קודם.

האתגר הייחודי: הגרף חייב לכבד ABAC. אם node דורש clearance גבוה יותר —
המשתמש לא רואה אותו בכלל (Strict mode), או רואה Ghost Edge (Connectivity Hint).
זו ההחלטה מ-PRD-v2 סעיף 15.5.

תכנן (docs/WAVE-3-DESIGN.md):
1. ארכיטקטורת data flow: DB → API (filtered by clearance) → Cytoscape
2. איך nodes מסוננים *לפני* שהם מגיעים ל-frontend (לא לסמוך על frontend!)
3. Ghost Edge policy — Strict vs Connectivity Hint per-investigation
4. Display Modes (Operational/Forensic) + Layer toggles
5. ביצועים עם 200+ nodes

קריטי: הסינון חייב לקרות ב-backend. frontend לעולם לא מקבל node שאסור לו לראות.
נאשר לפני קוד.
```

**מה לבדוק:** שהסינון ב-backend ולא ב-frontend. אם node מסווג מגיע ל-browser ו"מוסתר" ב-CSS — זו דליפה. ה-data לא יוצא מה-server.

## 3.2-3.7 — בנייה הדרגתית

**מודל:** 🟡 **Sonnet** לביצוע, 🔴 **Opus** לבאגים קשים ולסינון clearance.

בונים את הגרף ב-steps הדרגתיים, עם הוספת:
- Step F: clearance filtering על nodes
- Step G: Ghost Edge rendering
- Step H: Display Modes

## 3.8 — Self-Review + Decision Point

**מודל:** 🔴 **Opus**

```
self-review של גל 3 + security audit ספציפי לגרף:
- node מסווג אף פעם לא מגיע ל-frontend? תוכיח עם network inspection.
- Ghost edges לא מדליפים יותר מדי (timing, count)?
- pivot על node לא חושף nodes מעבר ל-clearance?

Decision Point גדול: זה היה ה-MVP המקורי. האם אני משתמש בכלי?
אם כן — נמשיך לבנות את המערכת המלאה. אם לא — עוצרים ומשפרים.
```

---

═══════════════════════════════════════════
# 🌊 גל 4 — Knowledge Base
═══════════════════════════════════════════

> **תוצאה שמישה:** KB ארגוני עם STIX 2.1, versioning, decay, וחיפוש — הכל מסווג.

**למה זה מוצר שלם:** עכשיו יש זיכרון ארגוני. ידע מחקירה אחת עובר לבאה.

## 4.1 — תכנון KB עם STIX + Classification

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
מתחילים גל 4: Knowledge Base. קרא PRD-v2 סעיפים 9, 12, 16 (KB, Continuity, STIX).

זה גל גדול. נחלק לתת-גלים:
- 4a: KB CRUD בסיסי עם STIX 2.1 objects + classification
- 4b: Versioning + audit (revoked, not deleted)
- 4c: Promote מ-investigation ל-KB (עם confirmation + undo)
- 4d: Search (exact + full-text) עם clearance filtering
- 4e: Confidence decay + auto-revalidation
- 4f: Sighting → Indicator aggregation

תכנן את כל הגל (docs/WAVE-4-DESIGN.md), אבל נבצע תת-גל אחד בכל פעם.
לכל object ב-KB יש classification + TLP. search לא מדליף objects מעל clearance.

נאשר את ה-design הכללי, ואז נתחיל מ-4a.
```

## 4.2-4.7 — ביצוע תת-גלים

**מודל:** 🟡 **Sonnet** לרוב, 🔴 **Opus** ל-search filtering (leak-prone) ול-decay logic.

**הפרומפט לכל תת-גל:**
```
בוא נבנה תת-גל [4x]: [תיאור].
צעד-צעד, diff קטן, E2E test. ל-search: denial test ש-search לא מחזיר
ולא סופר objects מעל clearance המשתמש.
```

## 4.8 — Decision Point

**מודל:** 🔴 **Opus**

---

═══════════════════════════════════════════
# 🌊 גל 5 — Triage & Workflow
═══════════════════════════════════════════

> **תוצאה שמישה:** Inbox + שלוש הזרימות המלאות (Triage, Investigation, Action) + Templates + Living Report.

**למה זה מוצר שלם:** עכשיו זה לא רק כלי lookup — זו מערכת workflow מלאה ליום עבודה.

## 5.1 — תכנון Workflows

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
מתחילים גל 5: Triage & Workflow. קרא PRD-v2 סעיפים 6, 7, 8 (שלוש הזרימות).

תת-גלים:
- 5a: Triage Inbox + Quick Add + Source Reliability tiers
- 5b: 5 Entry Points ל-investigation + Templates
- 5c: Resume Context (welcome back, auto-save)
- 5d: Living Report (מתעדכן תוך כדי)
- 5e: Decision support (recommendations engine — בסיסי, rule-based)
- 5f: FP feedback loop
- 5g: Cross-investigation discovery

תכנן (docs/WAVE-5-DESIGN.md). כל זרימה מודעת-clearance — Inbox מציג רק
IOCs שהמשתמש מורשה לראות. נאשר ונתחיל מ-5a.
```

## 5.2-5.8 — ביצוע

**מודל:** 🟡 **Sonnet** ברובו. 🔴 **Opus** ל-cross-investigation discovery (נוגע ב-clearance בין חקירות).

## 5.9 — Decision Point

**מודל:** 🔴 **Opus**

🎯 **נקודת עצירה משמעותית:** אם תעצור כאן, יש לך מערכת TI מלאה ל-single user. גל 6 פותח multi-user — צעד גדול.

---

═══════════════════════════════════════════
# 🌊 גל 6 — Collaboration
═══════════════════════════════════════════

> **תוצאה שמישה:** מספר משתמשים עובדים יחד, real-time, עם sharing מאובטח ו-handoff מובנה.

**⚠️ הגל הכי רגיש ל-security בכל הפרויקט.** multi-user + classified = כל טעות היא דליפה בין משתמשים.

## 6.1 — תכנון Collaboration (security-critical)

**מודל:** 🔴 **Opus** (אין פשרות — זה הגל הכי מסוכן)

**הפרומפט:**
```
מתחילים גל 6: Collaboration. זה הגל הכי רגיש ל-security בכל הפרויקט.
multi-user + classified data = כל באג הוא דליפה בין משתמשים.

קרא PRD-v2 סעיף 13 (Collaboration) + 15 (ABAC) שוב.

תכנן בזהירות מקסימלית (docs/WAVE-6-DESIGN.md):
1. Real-time sync (WebSocket) — איך לא מדליפים nodes מסווגים ב-broadcast?
2. כשמשתמש A ו-B באותה חקירה עם clearance שונה — כל אחד רואה view שונה
3. Invitation-only access + roles (owner/editor/viewer)
4. Conflict resolution (conversation threads + diff)
5. Soft locking
6. Structured handoff (4 types)
7. State machine + edge cases (orphaned, stale, timeout)

הסכנה הגדולה: WebSocket broadcast ששולח node מסווג לכל המחוברים, כולל מי
שאסור לו. תכנן per-user filtering על כל broadcast. נדון בזה לעומק לפני קוד.
```

**מה לבדוק:** שכל broadcast מסונן per-recipient. WebSocket ששולח את אותו payload לכולם הוא דליפה קלאסית במערכת מסווגת.

## 6.2-6.8 — ביצוע (זהירות מוגברת)

**מודל:** 🔴 **Opus** לכל מה שנוגע ל-real-time filtering ו-sharing. 🟡 **Sonnet** ל-UI.

**הפרומפט המרכזי:**
```
בוא נבנה [החלק]. זה security-critical.
לכל פיצ'ר: denial test מקיף. במיוחד — בדיקה ששני משתמשים עם clearance שונה
באותה חקירה לא רואים אחד את ה-data של השני מעבר להרשאה.
Red-Green: נראה את ה-denial test נכשל לפני המימוש.
```

## 6.9 — Security Audit מקיף + Decision Point

**מודל:** 🔴 **Opus**

```
סיימנו גל 6. זה דורש security audit הכי מקיף עד כה:
- penetration test מחשבתי: איך משתמש זדוני ינסה לראות data של אחר?
- WebSocket: כל broadcast מסונן? אין race condition שמדליף?
- sharing: אפשר לשתף רק מה שמותר? TLP:RED לא ניתן לשיתוף?
- handoff: receiver מקבל רק מה שמותר לו?

אל תמשיך לגל 7 עד שה-security של גל 6 הוכח. זה הגל שבו דליפה הכי סבירה.
```

---

═══════════════════════════════════════════
# 🌊 גל 7 — Operationalize & Scale
═══════════════════════════════════════════

> **תוצאה שמישה:** המערכת המלאה — actions (block/detect), ISAC sharing, multi-tenancy, ו-deployment production-grade.

**למה זה מוצר שלם:** זו המערכת המלאה מ-PRD-v2. ה-endgame.

## 7.1 — תכנון Scale + Multi-Tenancy

**מודל:** 🔴 **Opus**

**הפרומפט:**
```
מתחילים גל 7: Operationalize & Scale. הגל האחרון. קרא PRD-v2 סעיפים 8, 17.

תת-גלים:
- 7a: Action Outputs (blocklist, Sigma/YARA export, hunting queries)
- 7b: External Sharing / ISAC / Trust Circles (עם anonymization)
- 7c: Multi-tenancy מלא (tenant isolation)
- 7d: TAXII server
- 7e: Production hardening (backup, DR, monitoring, secret management)

תכנן (docs/WAVE-7-DESIGN.md). הקריטי ביותר: multi-tenancy + ABAC =
tenant isolation מושלם. tenant A לא רואה כלום מ-tenant B, ובתוך כל tenant
ה-clearance עדיין נאכף. נאשר ונתחיל מ-7a.
```

## 7.2-7.8 — ביצוע

**מודל:** 🔴 **Opus** ל-multi-tenancy ו-ISAC anonymization (leak-critical). 🟡 **Sonnet** לשאר.

## 7.9 — Final Security Audit + Production Readiness

**מודל:** 🔴 **Opus**

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

---

# 🔁 שגרות קבועות (לאורך כל הגלים)

זהות לאלה ב-EXECUTION-GUIDE.md:
- **פתיחת session:** קריאת CLAUDE_CONTEXT + PRD + DECISIONS (מודל לפי המשימה)
- **באג:** Prompt #5 (Sonnet רגיל / Opus קשה)
- **סגירת session:** Prompt #7 (Haiku)
- **learning:** Prompt #10 (Sonnet/Opus)

**תוספת ייחודית לפרויקט המסווג — שגרת Security Check שבועית:**

**מודל:** 🔴 **Opus**
```
security check שבועי. עבור על מה שבנינו השבוע ושאל:
- הוספנו endpoint חדש? הוא עובר דרך ה-Policy Engine?
- הוספנו מקום שמציג data? הוא מסונן לפי clearance?
- יצרנו leak surface חדש (count, error, log)? חסמנו אותו?
תן לי רשימה קצרה של ממצאים ותיקונים נדרשים.
```

---

# 📊 טבלת בחירת מודל — מותאמת לפרויקט מסווג

| משימה | מודל | הערה |
|---|---|---|
| תכנון Security Model | 🔴 Opus | ההחלטה הכי חשובה |
| תכנון כל גל | 🔴 Opus | architecture decisions |
| כל קוד security/clearance/RLS | 🔴 Opus | טעות = דליפה |
| Multi-tenancy / isolation | 🔴 Opus | leak-critical |
| WebSocket filtering | 🔴 Opus | leak-critical |
| ISAC anonymization | 🔴 Opus | leak-critical |
| Security audits | 🔴 Opus | תופס מה ש-Sonnet מפספס |
| Decision Points | 🔴 Opus | אסטרטגי |
| Debugging קשה | 🔴 Opus | root cause |
| כתיבת UI / קוד רגיל | 🟡 Sonnet | ברירת מחדל |
| כתיבת tests | 🟡 Sonnet | מאוזן |
| Refactoring | 🟡 Sonnet | מאוזן |
| באג פשוט | 🟡 Sonnet | מספיק |
| Wrap-ups / commits | 🟢 Haiku | חיסכון |
| סיכומים / typos | 🟢 Haiku | טריוויאלי |

**שים לב:** בפרויקט מסווג, חלק ה-Opus גדול יותר מבפרויקט רגיל. כל קוד שנוגע ב-clearance הוא Opus. זה עולה יותר — אבל security flaw עולה הרבה יותר.

---

# 🎯 נקודות העצירה — מתי לגיטימי לעצור

כל גל הוא נקודת עצירה לגיטימית. הנה מה שיש לך בכל אחת:

| עוצר אחרי גל | מה יש לך ביד |
|---|---|
| **1** | מערכת מאובטחת עם הרשאות — proof שה-security model עובד |
| **2** | כלי IOC enrichment מסווג — שמיש בעבודה |
| **3** | כלי TI ויזואלי מלא — ה-MVP המקורי + security |
| **4** | מערכת עם זיכרון ארגוני (KB) |
| **5** | מערכת workflow מלאה ל-single user |
| **6** | מערכת collaboration רב-משתמשים |
| **7** | המערכת המלאה מ-PRD-v2 |

**אין בושה לעצור.** המדד הוא לא "כמה גלים סיימת" אלא "האם אתה משתמש בכלי". מערכת שעוצרת בגל 3 ואתה משתמש בה יומיום שווה יותר ממערכת בגל 7 שיושבת ריקה.

---

# כללי הזהב — לפרויקט המלא

1. **Security foundation לפני הכל.** גל 1 הוא הבסיס. אל תתפשר עליו.
2. **Denial tests, תמיד.** במערכת מסווגת, ה-test שמוכיח ש*אסור* רואה — חשוב יותר מזה שמוכיח ש*מותר* רואה.
3. **Backend filtering, לא frontend.** מידע מסווג לא יוצא מה-server. נקודה.
4. **Opus ל-security, בלי קמצנות.** זה המקום שבו לחסוך על מודל יקר ביותר.
5. **גל = מוצר שלם.** אל תתחיל גל אם אתה לא מסיים אותו. חצי גל = שבור.
6. **Decision Point בסוף כל גל.** כן עם עצמך: אתה משתמש בכלי?
7. **Security check שבועי.** leak surface חדש מתגלה? חסום מיד.
8. **לוח הזמנים בשנים.** זה מסע. תחגוג כל גל.

---

**זו התוכנית המלאה. שבעה גלים, מ-foundation מאובטח ועד מערכת enterprise מלאה.**
**הצעד הבא: גל 1, שלב 1.1 — תכנון ה-Security Model. זו אבן היסוד של הכל.**
