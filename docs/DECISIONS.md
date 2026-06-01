# DECISIONS.md — Architecture Decision Log

> כל החלטה טכנית או מוצרית מתועדת כאן. הפורמט נועד לעזור לClaude (וגם לך) להבין **למה** דברים בנויים כך, חודשים אחרי שההחלטה התקבלה.

**איך להוסיף entry חדש:**
1. תאריך + שם תיאורי
2. Context — מה הייתה הסיטואציה
3. Decision — מה החלטנו
4. Alternatives — מה לא בחרנו (חשוב!)
5. Trade-offs — מה זה עולה לנו

---

## 2025-XX-XX — Stack Selection

**Context:** צריך לבחור stack ל-MVP של מערכת TI אישית. הקריטריונים: עלות נמוכה ($0-$50/חודש), קל ל-Claude לעבוד איתו, scalable עבור single user → 100 users, יציב.

**Decision:** React + TypeScript + Vite + Tailwind + Cytoscape.js + shadcn/ui (frontend) | FastAPI + Python (backend) | Supabase (DB + Auth) | Vercel (frontend hosting) | Railway (backend hosting).

**Alternatives considered:**
- **Next.js במקום React+Vite** — נדחה כי Server Components מוסיפים מורכבות שלא צריך ל-MVP.
- **Express במקום FastAPI** — נדחה כי Python יותר מקובל ב-TI ecosystem (STIX libs).
- **MongoDB במקום Postgres** — נדחה כי STIX מובנה היטב ב-relational, ו-Postgres JSONB נותן best of both.
- **Self-hosted Postgres** — נדחה כי Supabase נותן Auth + RLS + real-time בחינם.
- **AWS / GCP** — נדחה כי overkill, expensive, ומורכב לsolo dev.

**Trade-offs:**
- Supabase free tier מוגבל (500MB DB, 50K MAU). יספיק עד ~50 users אקטיביים.
- Railway free tier 500h/month — מספיק ל-1 backend אחד, לא 2.
- shadcn/ui דורש copy-paste של components, לא npm install — יותר קוד ב-repo, אבל יותר שליטה.

---

## 2025-XX-XX — MVP Scope: Investigation Graph בלבד

**Context:** ה-PRD המלא מתאר מערכת ענקית. בקצב פיתוח של 6 שעות בשבוע (solo + Claude), מערכת מלאה לוקחת 5+ שנים. צריך לחתוך scope.

**Decision:** MVP יכלול רק Investigation Graph — משתמש מקליד IOC, רואה enrichment + pivot graph. בלי triage inbox, בלי playbooks, בלי collaboration.

**Alternatives considered:**
- **Triage Inbox first** — נדחה כי דורש feed integration שזה complexity גדולה.
- **KB + search first** — נדחה כי בלי data בKB זה ריק.
- **Full feature set מצומצם** — נדחה כי כל פיצ'ר חצי-בנוי = badly broken.

**Trade-offs:**
- אנחנו מוותרים על מה שמבדל מ-OpenCTI (collaboration, multi-user).
- אנחנו מתמקדים בfeature אחד שאם נעשה אותו טוב, יוצר value אמיתי.
- אם המוצר לא יותר טוב מ-VirusTotal portal, נסגור את הפרויקט.

---

## 2025-XX-XX — Single User MVP, Auth Anyway

**Context:** במצב הראשוני אני המשתמש היחיד. הרבה מערכות mvp דוחות את ה-auth ל-Phase 2. האם לעשות אותו דבר?

**Decision:** Auth מוטמע מ-Phase 0, גם אם יש user יחיד.

**Alternatives considered:**
- **No auth ב-MVP** — נדחה כי הוספת auth מאוחר זה כאב גדול (כל endpoint צריך retrofit).
- **Hard-coded API key במקום auth** — נדחה כי לא secure ל-production.

**Trade-offs:**
- ~4 שעות עבודה נוספות ב-Phase 0.
- חוסך ~30 שעות ב-Phase 4 כשנוסיף משתמש שני.

---

## 2025-XX-XX — Tests are Mandatory

**Context:** כ-solo dev שלא קורא קוד טוב, איך אני יודע שהקוד עובד?

**Decision:** כל פיצ'ר חייב Playwright E2E test כתנאי merge ל-main. Claude כותב את ה-test יחד עם ה-feature.

**Alternatives considered:**
- **Manual testing בלבד** — נדחה כי לא scalable, אני אשכח לבדוק regression.
- **Unit tests בלבד** — נדחה כי לא תופסים integration bugs.
- **Tests אופציונליים** — נדחה כי בלי דרישה הם לא ייכתבו.

**Trade-offs:**
- כל פיצ'ר לוקח ~30% יותר זמן לפיתוח.
- חוסך זמן רב יותר בdebugging מאוחר.
- נותן לי confidence בlieu של יכולת לקרוא קוד.

---

## 2025-XX-XX — Mock APIs Before Real APIs

**Context:** APIs חיצוניים (VirusTotal וכו') יש להם rate limits נמוכים בfree tier. אם אני בודק frontend עם API אמיתי, אבזבז quota.

**Decision:** לכל API חיצוני, נכתוב mock service שמחזיר תשובות סטטיות. Frontend מתפתח מול ה-mock. רק אחרי שhfrontend עובד, נחבר ל-API אמיתי.

**Alternatives considered:**
- **לקנות paid tier מההתחלה** — נדחה בגלל budget.
- **לבדוק עם API אמיתי בזהירות** — נדחה כי שגיאות בקוד מתחילות לבזבז quota.

**Trade-offs:**
- כתיבת mock = ~2 שעות נוספות לכל connector.
- חוסך ~10 שעות של "אזלה ה-quota בבדיקות".

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
