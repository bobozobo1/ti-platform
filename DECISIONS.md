# DECISIONS.md — Architecture Decision Log

> כל החלטה טכנית או מוצרית מתועדת כאן. הפורמט נועד לעזור ל-Claude (וגם לך) להבין **למה** דברים בנויים כך, חודשים אחרי שההחלטה התקבלה.

**איך להוסיף entry חדש:**
1. תאריך + שם תיאורי
2. Context — מה הייתה הסיטואציה
3. Decision — מה החלטנו
4. Alternatives — מה לא בחרנו (חשוב!)
5. Trade-offs — מה זה עולה לנו

---

## 2025-XX-XX — Building Full System, Not MVP

**Context:** התלבטות בין שני מסלולים — לבנות MVP מצומצם ולהרחיב, או לבנות את המערכת המלאה מ-PRD-v2 בשכבות (גלים). ה-MVP היה פשוט יותר אבל היה דורש refactor אדיר להוספת ABAC.

**Decision:** בונים את המערכת המלאה ב-7 גלים. כל גל הוא מוצר שלם שאפשר לעצור בו. ABAC מהיום הראשון.

**Alternatives considered:**
- **MVP-first (Investigation Graph בלבד, ללא ABAC)** — נדחה כי הוספת ABAC בדיעבד למערכת קיימת היא retrofit של כל endpoint, כל query, כל component. עלות גבוהה יותר מבנייה נכונה מההתחלה.
- **כל-המערכת-בלי-נקודות-עצירה** — נדחה כי solo dev צריך exit ramps לגיטימיים. בלי נקודות עצירה, פרויקט שנכשל באמצע = הכל הולך לפח.

**Trade-offs:**
- כל גל ארוך יותר מ-MVP מקביל (ABAC בכל שכבה)
- אבל אין refactor גדול בעתיד
- נקודות עצירה אחרי כל גל מאפשרות "לעצור בכבוד"
- ~46-60 שבועות עבודה אפקטיבית למערכת המלאה (2.5-4 שנים קלנדריות)

---

## 2025-XX-XX — ABAC as Foundation, Not Feature

**Context:** ABAC עם clearance levels ו-TLP הוא דרישה קריטית. השאלה: לבנות אותו כ-feature בשלב מאוחר, או כאבן יסוד מהיום הראשון?

**Decision:** ABAC הוא אבן יסוד. גל 1 כולו מוקדש ל-Security Foundation, לפני שום פיצ'ר TI. כל endpoint, query, ו-node בגרף עובר דרך Policy Engine מרכזי.

**Alternatives considered:**
- **ABAC כ-feature בגל 5+** — נדחה. הוספת ABAC ב-retrofit היא סיוט — כל endpoint צריך לעבור עדכון, כל test צריך revision, כל query DB צריך לקבל clearance filter. עבודה כפולה לפחות.
- **Authentication בסיסי בלבד, ABAC רק לגלים מתקדמים** — נדחה כי בלי clearance filtering מההתחלה, אי אפשר לאחסן classified data בכלל. זה חוסם מ-day 1.

**Trade-offs:**
- גל 1 ארוך יותר (4-6 שבועות) ללא פיצ'רי TI גלויים
- אבל כל גל אחר-כך מתפתח טבעי מעל security foundation
- security mistakes בגל 1 = כואב לתקן בגלים 2-7. תכנון זהיר בגל 1 חיוני.

---

## 2025-XX-XX — Three Iron Rules of Security

**Context:** במערכת מסווגת, "פתרון security" לא מספיק. צריך עקרונות שמתורגמים להחלטות יומיומיות בקוד.

**Decision:** שלושה כללי ברזל מוטמעים בכל פיצ'ר ובכל test:
1. **Default Deny** — ברירת מחדל היא דחייה. גישה דורשת הוכחה.
2. **Test the Denial** — ה-test הראשון לכל פיצ'ר מוכיח שמשתמש לא מורשה *לא* רואה את המידע.
3. **No Leak Surfaces** — מידע מסווג לא דולף דרך errors, counts, search, autocomplete, logs, או timing.

**Alternatives considered:**
- **General "good security practices"** — נדחה כי גנרי מדי. לא נותן הנחיה ספציפית כשמתעורר ספק.
- **Default Allow עם blocklist** — נדחה כקלאסיקה של security failure. שכחת לחסום משהו = דליפה.
- **Backend-only filtering ללא denial tests** — נדחה כי בלי denial tests, באג בסינון נשאר חבוי עד שיגרום לדליפה.

**Trade-offs:**
- כל פיצ'ר לוקח ~30% יותר זמן (denial test + leak surface check)
- אבל כל פיצ'ר נשלח עם security ידוע, לא משוער
- שלושת הכללים מצוטטים בכל גל ב-EXECUTION-GUIDE — מבטיח עקביות

---

## 2025-XX-XX — "Not Found" vs "Access Denied"

**Context:** כשמשתמש לא-מורשה מנסה לגשת ל-object מסווג, מה התגובה? "Access denied" נראה ידידותי, אבל הוא מדליף שה-object קיים.

**Decision:** תמיד "404 Not Found", לעולם לא "403 Access Denied" לתוכן מסווג. שני התגובות נראות זהות למשתמש.

**Alternatives considered:**
- **"Access denied" עם הסבר** — נדחה כי זה Information Disclosure בסיסי. עצם קיום ה-object הוא לעיתים המידע המסווג.
- **תגובות זהות במלל אבל זמני תגובה שונים** — נדחה כי זה Timing Attack. constant-time response חיוני.

**Trade-offs:**
- חוקרים מורשים שעשו טעות כתיב מקבלים "not found" מבלבל
- אבל זה מחיר מקובל באבטחת מידע מסווג
- ניתן להוסיף "are you sure this exists?" hint רק למשתמשים עם clearance מספיק

---

## 2025-XX-XX — Stack Selection

**Context:** צריך לבחור stack למערכת TI מלאה עם ABAC. הקריטריונים: עלות נמוכה ($0-$50/חודש בתחילה), קל ל-Claude לעבוד איתו, scalable, יציב, תומך RLS native.

**Decision:** React + TypeScript + Vite + Tailwind + Cytoscape.js + shadcn/ui (frontend) | FastAPI + Python (backend) | **Supabase (DB + Auth + RLS — קריטי)** | Vercel (frontend hosting) | Railway (backend hosting).

**Alternatives considered:**
- **Next.js במקום React+Vite** — נדחה (Server Components מורכבים, אין צורך)
- **Express במקום FastAPI** — נדחה (Python יותר מקובל ב-TI ecosystem, יש python-stix2)
- **MongoDB במקום Postgres** — נדחה (STIX מובנה היטב ב-relational, ו-Postgres JSONB טוב לשניהם, ו-Supabase RLS דורש Postgres)
- **Self-hosted Postgres** — נדחה (Supabase RLS נותן ABAC layer חינם — קריטי לפרויקט)
- **AWS / GCP** — נדחה (overkill, יקר, מורכב ל-solo dev)

**Trade-offs:**
- Supabase free tier מוגבל (500MB DB, 50K MAU). יספיק עד ~50 active users
- Railway free tier 500h/month
- shadcn/ui דורש copy-paste של components (יותר קוד, יותר שליטה)
- **Supabase RLS חיוני** — defense in depth עם application-layer Policy Engine

---

## 2025-XX-XX — Tests are Mandatory

**Context:** כ-solo dev שלא קורא קוד היטב, איך אני יודע שהקוד עובד? איך אני יודע שה-security עובד?

**Decision:** כל פיצ'ר חייב Playwright E2E test כתנאי merge ל-main. פיצ'רים עם data מסווג חייבים **denial test ראשון** (Red-Green — נראה אותו נכשל לפני המימוש).

**Alternatives considered:**
- **Manual testing בלבד** — נדחה (לא scalable, אני אשכח regression)
- **Unit tests בלבד** — נדחה (לא תופסים integration bugs)
- **Tests אופציונליים** — נדחה (בלי דרישה לא נכתב)
- **E2E tests רק לפיצ'רים מורכבים** — נדחה (במערכת מסווגת כל פיצ'ר הוא potential leak)

**Trade-offs:**
- כל פיצ'ר לוקח ~30% יותר זמן
- חוסך זמן רב יותר ב-debugging מאוחר
- denial tests חיוניים לבטחון security
- E2E tests משמשים גם כ-documentation של behavior

---

## 2025-XX-XX — Mock APIs Before Real APIs

**Context:** APIs חיצוניים (VirusTotal וכו') יש להם rate limits נמוכים ב-free tier. בדיקה עם API אמיתי תבזבז quota בזמן פיתוח.

**Decision:** לכל API חיצוני, נכתוב mock service שמחזיר תשובות סטטיות עם classification levels שונים. Frontend ו-backend מתפתחים מול mock. רק אחרי שעובד, מתחברים ל-API אמיתי.

**Alternatives considered:**
- **לקנות paid tier מההתחלה** — נדחה ($)
- **לבדוק עם API אמיתי בזהירות** — נדחה (שגיאות בקוד יבזבזו quota)

**Trade-offs:**
- כתיבת mock = ~2 שעות נוספות לכל connector
- חוסך ~10 שעות של "אזלה ה-quota בבדיקות"
- mocks עם classification levels גם בודקים את ה-clearance filtering

---

## 2025-XX-XX — Backend Filtering, Never Frontend

**Context:** במערכת מסווגת, איפה הסינון של data מסווג קורה?

**Decision:** **סינון תמיד ב-backend**. Frontend לעולם לא מקבל data שאסור למשתמש לראות. גם לא "מקבל ומסתיר ב-CSS".

**Alternatives considered:**
- **שליחת כל ה-data ו-filter ב-frontend** — נדחה (נראה ב-DevTools, זו דליפה)
- **שליחת data מוצפן וה-frontend מפענח** — נדחה (overkill, ה-key חייב להיות איפשהו)
- **Hybrid — חלק ב-backend, חלק ב-frontend** — נדחה (קשה לחשוב על איזה case שזה הגיוני)

**Trade-offs:**
- API endpoints מורכבים יותר (clearance filtering לכל query)
- אבל זו הדרך היחידה למנוע דליפה
- network inspection בדפדפן לא יראה classified data שהמשתמש לא מורשה לו

---

## 2025-XX-XX — Wave-Based Architecture, Not Phase-Based

**Context:** איך מארגנים פרויקט של 2.5-4 שנים בלי לאבד מומנטום?

**Decision:** המערכת בנויה ב-**7 גלים**. כל גל הוא מוצר שלם שאפשר לעצור בו. בסוף כל גל יש Decision Point פורמלי: "האם אני משתמש בכלי? להמשיך?"

**Alternatives considered:**
- **Phases מסורתיות (Phase 1, 2, 3...)** — נדחה כי phases לא בהכרח מסתיימים במוצר שמיש. גל 2 לבד = כלי IOC lookup שלם.
- **Agile sprints של שבועיים** — נדחה כי solo dev בלי team לא צריך ceremony של sprints.
- **Feature-by-feature ללא מבנה גלים** — נדחה כי אין נקודות עצירה ברורות, קל לאבד track.

**Trade-offs:**
- כל גל מרגיש "ארוך" (8-12 שבועות)
- אבל בסוף כל גל יש מוצר אמיתי
- Decision Points מונעים sunk cost fallacy — לגיטימי לעצור אחרי גל 3 עם כלי מצוין

---

## 2025-XX-XX — Opus for Security, Without Compromise

**Context:** Claude Opus יקר יותר מ-Sonnet. בפרויקט רגיל, רוב העבודה ב-Sonnet. במערכת מסווגת, מתי כדאי לעלות ל-Opus?

**Decision:** **כל קוד שנוגע ב-clearance/ABAC/RLS/multi-tenancy — Opus**. ללא קמצנות. Sonnet ל-UI ו-code רגיל. Haiku ל-wrap-ups.

**Alternatives considered:**
- **Sonnet ל-הכל, Opus רק ל-debugging קשה** — נדחה. security flaw במערכת מסווגת = דליפת מידע. עלות הרבה יותר מהפרש מודלים.
- **Opus ל-הכל** — נדחה (יקר מדי לפרויקט solo)

**Trade-offs:**
- ~40% מהזמן ב-Opus (לעומת ~15% בפרויקט רגיל)
- עלות מודל גבוהה יותר
- אבל זו השקעה נכונה — debugging של security leak לאחר production עולה הרבה יותר

---

## 2026-06-10 — Render כ-Backend Hosting (במקום Railway)

**Context:** Railway שינה את מודל ה-free tier ואינו זמין בחינם.

**Decision:** Render — free tier עם Web Service, Python runtime, auto-deploy מ-GitHub.

**Alternatives considered:**
- **Railway** — נדחה, אין free tier
- **Fly.io** — אפשרי אבל מורכב יותר לsetup ראשוני
- **Vercel Serverless** — לא מתאים ל-FastAPI עם long-running connections

**Trade-offs:**
- Render Free tier "spins down" אחרי 15 דקות חוסר שימוש (cold start ~30 שניות)
- אבל חינמי לחלוטין לפיתוח ו-demo

---

## 2026-06-10 — CORS_ORIGINS כ-string (לא list) ב-pydantic-settings

**Context:** pydantic-settings v2 לא יודע לפרס `list[str]` מ-env var רגיל (ציפה ל-JSON array). field_validator עם mode="before" לא פתר.

**Decision:** `cors_origins: str` עם method `get_cors_origins()` שמחלק ב-comma. פשוט ואמין.

**Alternatives considered:**
- **field_validator mode="before"** — ניסינו, לא עבד ב-Render
- **JSON env var** (`["https://..."]`) — מכוער וטעות-prone לאנשים שמגדירים env vars

**Trade-offs:**
- פחות "pythonicׁ" אבל עובד בכל סביבה
- צריך לקרוא `settings.get_cors_origins()` ולא `settings.cors_origins`

---

## 2026-06-10 — Backend deps מינימליות לשלב 1.2

**Context:** `supabase` ו-`stix2` packages גרמו לcrash בstartup ב-Render (Python 3.14).

**Decision:** שלב 1.2 מכיל רק `fastapi + uvicorn + pydantic + pydantic-settings`. `supabase` ו-`stix2` יתווספו בשלב 1.3 כשנממש ABAC.

**Alternatives considered:**
- **Pin Python 3.11** ב-Render — אפשרי אבל דורש render.yaml config
- **Debug crash** — לא הצלחנו לראות runtime logs ב-Render free tier API

**Trade-offs:**
- /health endpoint עובד בלי DB connectivity בשלב זה
- בשלב 1.3 נוסיף supabase ונממש חיבור אמיתי

---

<!--
Template ל-entry חדש — תעתיק את זה:

## YYYY-MM-DD — [שם תיאורי]

**Context:**

**Decision:**

**Alternatives considered:**
- **[Alt 1]** — נדחה כי [סיבה]
- **[Alt 2]** — נדחה כי [סיבה]

**Trade-offs:**
- [trade-off 1]
- [trade-off 2]

---
-->
