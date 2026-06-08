# CLAUDE.md

> קובץ זה נקרא אוטומטית על ידי Claude Code בכל session.
> הוא מכיל את כל ההקשר הקריטי. אחרי קריאתו, קרא גם:
> - `docs/SECURITY-MODEL.md` — מודל ABAC (חובה בכל session)
> - `docs/EXECUTION-GUIDE.md` — מדריך ביצוע (שלב/פרומפט/מודל)
> - `docs/DECISIONS.md` — החלטות שכבר קיבלנו
> - `docs/MASTER-PLAN.md` — 7 הגלים (כשצריך תמונה אסטרטגית)

---

## 1. מה אנחנו בונים

**מוצר:** TI Investigation Platform — מערכת TI מלאה לחקירה, ניתוח, ושיתוף של Threat Intelligence עם תמיכה ב-classified data.

**משתמש ראשוני:** חוקר TI מקצועי שמשתמש בכלי בעבודה היומית.

**הצעת ערך:**
- Investigation Graph ויזואלי עם enrichments אוטומטיים
- Triage Inbox לניהול IOCs נכנסים
- Knowledge Base ארגוני עם STIX 2.1
- Collaboration real-time עם הרשאות ABAC מלאות
- TLP + Classification enforcement על כל object
- Actions: blocklist, detection rules (Sigma/YARA), ISAC sharing

**אנחנו בונים את המערכת המלאה** — לא MVP מצומצם. הבנייה ב-7 גלים (ראה `docs/MASTER-PLAN.md`).

**⚠️ ABAC הוא אבן יסוד — לא תוספת.** כל שורת קוד מושפעת. ראה `docs/SECURITY-MODEL.md`.

---

## 2. מי אני

- **תפקיד:** Domain Expert ב-TI + PM של הפרויקט
- **רקע פיתוח:** מוגבל — לומד תוך כדי. **לא קורא קוד מקצועית.**
- **ההשלכות:**
  - הסבר מונחים טכניים במילים פשוטות
  - תן תמיד בחירה בין אפשרויות עם trade-offs
  - הסבר ב-comments מה הקוד עושה
  - אם אני מבקש משהו שיכניס באג — **זהיר לפני שתעשה**
  - אם יש לי הנחה לא נכונה — תתקן בנימוס

---

## 3. עקרונות עבודה (Non-Negotiable)

### 3.1 — Security First
**ABAC הוא לא פיצ'ר — הוא התשתית.** כל endpoint, query, ו-node בגרף עובר דרך ה-Policy Engine.

שלושה כללי ברזל — **לעולם לא מפשרים עליהם:**
- **Default Deny** — גישה נדחית כברירת מחדל
- **Test the Denial** — ה-test הראשון תמיד מוכיח שמי שאסור לו *לא* רואה (Red-Green)
- **No Leak Surfaces** — מידע מסווג לא דולף דרך errors, counts, search, logs, timing, או autocomplete

### 3.2 — Backend Filtering, Never Frontend
מידע מסווג **לא יוצא מה-server לעולם**.
Node מסווג שמגיע ל-browser ומוסתר ב-CSS = דליפה. Network tab של DevTools = הוכחה לדליפה.

### 3.3 — Acceptance Criteria First
לכל משימה יש acceptance criteria בסגנון Given/When/Then.
אם חסרים — **שאל לפני שכותבים קוד**.

### 3.4 — Tests are Mandatory
- כל פיצ'ר → Playwright E2E test
- כל פיצ'ר עם data מסווג → **denial test ראשון** (Red-Green)
- בלי יוצא מהכלל

### 3.5 — Small Diffs
50–100 שורות בכל פעם. עצור, קבל אישור, המשך.

### 3.6 — Self-Review לפני הגשה
לפני שאני בודק כל פיצ'ר, ענה על:
- 3 הדברים הכי שבירים בקוד?
- Edge cases שלא טופלו?
- יש leak surface חדש שלא ב-`docs/SECURITY-MODEL.md`?

### 3.7 — Documentation Updates אחרי כל session
1. עדכן `CLAUDE.md` סעיף 9 (Status)
2. הוסף ל-`docs/DECISIONS.md` אם התקבלה החלטה טכנית
3. עדכן `docs/SECURITY-MODEL.md` אם נוסף leak surface חדש

### 3.8 — No Over-Engineering
מערכת enterprise — לא MVP. אבל לא מוסיפים שום דבר שלא ב-`docs/EXECUTION-GUIDE.md`.
רוצה להוסיף משהו שלא תוכנן? **שאל קודם.**

---

## 4. Stack טכני (לא משתנה ללא אישור)

### Frontend
- React 18 + TypeScript (strict mode)
- Vite · Tailwind CSS · shadcn/ui (Radix based)
- Cytoscape.js (graph) · TanStack Query · React Router · Zustand

### Backend
- Python 3.11+ · FastAPI · Pydantic v2
- httpx (async HTTP) · python-stix2

### Infrastructure
- **Supabase** — Postgres + Auth + **RLS** (קריטי ל-ABAC) + real-time
- Vercel (frontend) · Render (backend) · GitHub Actions (CI/CD)

### Testing
- Playwright (E2E + denial tests) · Vitest (frontend unit) · pytest (backend unit)

### External APIs
| API | מטרה | Free Tier |
|---|---|---|
| VirusTotal | reputation | 4 req/min, 500/day |
| AbuseIPDB | IP reputation | 1000/day |
| WhoisXML | WHOIS | 500/month |
| crt.sh | Certificate Transparency | Unlimited |
| Shodan | Deep scan (גל 2+) | 100/month |

---

## 5. מבנה הפרויקט

```
ti-platform/
├── CLAUDE.md                    # ← הקובץ הזה (נקרא אוטומטית)
├── docs/
│   ├── SECURITY-MODEL.md        # ABAC + leak surfaces
│   ├── MASTER-PLAN.md           # 7 גלים
│   ├── EXECUTION-GUIDE.md       # שלב/פרומפט/מודל
│   ├── DECISIONS.md             # decision log
│   ├── PROMPTS.md               # prompts לסיטואציות
│   ├── PRD-v2.md                # החזון המלא
│   └── WAVE-X-DESIGN.md         # design doc לכל גל (נוצר תוך כדי)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── inbox/           # Triage Inbox (גל 5)
│   │   │   ├── investigation/   # Investigation Graph (גל 3)
│   │   │   ├── kb/              # Knowledge Base (גל 4)
│   │   │   └── collaboration/   # Collaboration (גל 6)
│   │   ├── lib/                 # utilities, API client, policy checks
│   │   ├── hooks/
│   │   ├── types/
│   │   └── pages/
│   ├── tests/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/                 # FastAPI routes
│   │   ├── core/
│   │   │   ├── security.py      # Policy Engine — כל endpoint עובר דרכו
│   │   │   └── config.py
│   │   ├── models/              # Pydantic models
│   │   ├── services/
│   │   │   ├── enrichment/      # VT, AbuseIPDB, WHOIS connectors
│   │   │   ├── abac/            # ABAC logic
│   │   │   └── stix/            # STIX 2.1 handling
│   │   └── db/                  # Supabase client
│   ├── tests/
│   └── pyproject.toml
├── tests/
│   └── e2e/                     # Playwright — כולל denial tests
├── supabase/
│   └── migrations/              # כל שינוי schema = migration file
├── .env.example
└── .github/workflows/
```

---

## 6. ABAC — סיכום מהיר

> ⚠️ המודל המלא ב-`docs/SECURITY-MODEL.md` (חובה לקרוא). הסעיף הזה = תמצית לעיון מהיר.

### 3 ממדי הרשאה (AND לוגי — כולם חייבים להתקיים)
1. **Permission Level** — רמת הרשאה לפי מודול (RBAC-style)
2. **Need-to-Know (NTK)** — גישה מפורשת לחקירה ספציפית
3. **TLP** — רמת רגישות המידע עצמו (TLP 2.0)

### Permission Levels (סדר עולה)
`reader(1)` → `analyst(2)` → `senior_analyst(3)` → `lead_analyst(4)` → `admin(5)`
- `auditor` — תפקיד נפרד (read-only לכל + audit log, ללא NTK bypass)

### TLP Levels (TLP 2.0 — סדר עולה)
`CLEAR` → `GREEN` → `AMBER` → `AMBER+STRICT` → `RED`

### Need-to-Know
- כל חקירה (investigation) מוגנת ב-NTK — רשימת גישה מפורשת
- יוצר החקירה = owner אוטומטי
- Admin **לא** bypasses NTK — חייב לקבל גישה מפורשת
- `tlp_red_recipients` — גישה מפורשת לתוכן TLP:RED

### Deny Behavior — קריטי
- גישה אסורה מחזירה תמיד **`404 Not Found`** — לעולם לא `403`
- הבחנה בין 404 ל-403 = Information Disclosure = דליפה
- Constant-time response (~50ms minimum) — מניעת Timing Attack
- TLP:RED object עם NTK לcontainer → **Placeholder** (קיום נראה, תוכן מוסתר)

### Policy Engine
נקודה מרכזית אחת ב-`backend/app/core/security.py`.
כל endpoint עובר דרכו. אין בדיקות מפוזרות.
החלטה אפשרית: `ALLOW` · `DENY` · `PLACEHOLDER`

---

## 7. TI Domain Knowledge

### IOC Types
- IP Address (IPv4, IPv6 בגל 2+)
- Domain · URL · File Hash (MD5/SHA1/SHA256)
- Email (גל 5+) · Certificate

### STIX 2.1 Objects
- `indicator`, `observed-data`, `sighting`, `relationship`
- `threat-actor`, `campaign`, `malware`, `attack-pattern`, `bundle`

### Confidence Scoring
- **High** (80–100): VT > 5/30, או AbuseIPDB > 75
- **Medium** (50–79): VT 1–5, או AbuseIPDB 25–75
- **Low** (0–49): שאר המקרים
- **Stale**: יורד אוטומטית עם הזמן (גל 4)

---

## 8. Conventions

### Naming
- Files: `kebab-case` · Components: `PascalCase` · Functions: `camelCase`
- Types: `PascalCase` · DB columns: `snake_case`
- API endpoints: `/api/v1/kebab-case/{id}/action`

### Git Commits
```
<type>: <short description>
```
Types: `feat` · `fix` · `refactor` · `test` · `docs` · `chore` · **`security`**

### Branch Strategy
- `main` — תמיד יציב, deployed
- `feature/<name>` — לכל פיצ'ר
- PR ל-main: כל tests עוברים (כולל denial tests) + my approval

### Error Handling
- 404 גם כשיש "access denied"
- Backend: HTTP status codes נכונים
- Frontend: user-friendly messages
- External API failure: partial result, לא crash

---

## 9. Status נוכחי

### גל נוכחי
**גל 1 — Secure Foundation** · שלב: 1.2 — תשתית בסיסית

### מה כבר עובד
- ✅ GitHub repo: `bobozobo1/ti-platform` (main branch)
- ✅ כל מסמכי הדוקומנטציה ב-`docs/` (SECURITY-MODEL, MASTER-PLAN, EXECUTION-GUIDE, DECISIONS, PROMPTS)
- ✅ `docs/SECURITY-MODEL.md` v1.0 — מודל ABAC מלא (663 שורות, 8 סעיפים)

### בעבודה כרגע
- שלב 1.2 — תשתית בסיסית (repo structure + frontend ריק + backend ריק + deployments)

### Known Issues
- `docs/PRD-v2.md` — placeholder בלבד (קובץ .docx לא הומר עדיין)

### TODOs
- [ ] פתיחת חשבון Supabase + יצירת project
- [ ] פתיחת חשבון Vercel (לfrontend)
- [ ] פתיחת חשבון Render (לbackend)
- [ ] API keys: VirusTotal, AbuseIPDB, WhoisXML
- [ ] המרת PRD-v2.docx ל-Markdown

---

## 10. DON'Ts — דברים שניסינו ולא עבדו

- [יתמלא תוך כדי פיתוח]

---

## 11. בחירת מודל לכל משימה

| משימה | מודל |
|---|---|
| תכנון ארכיטקטורה / security design | 🔴 Opus |
| כל קוד ABAC / RLS / clearance filtering | 🔴 Opus |
| Debugging קשה / security bugs | 🔴 Opus |
| Decision Points + security audits | 🔴 Opus |
| WebSocket filtering / multi-tenancy | 🔴 Opus |
| כתיבת קוד רגיל / UI / features | 🟡 Sonnet |
| Tests / refactoring / הסברים | 🟡 Sonnet |
| Wrap-ups / commits / סיכומים | 🟢 Haiku |

**~40% Opus** בפרויקט זה (לעומת ~15% בפרויקט רגיל). זה המחיר של מערכת מסווגת.

---

## 12. Resources

- [STIX 2.1 Spec](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html)
- [VirusTotal API v3](https://docs.virustotal.com/reference/overview)
- [AbuseIPDB API](https://docs.abuseipdb.com/)
- [Cytoscape.js](https://js.cytoscape.org/)
- [Supabase Docs](https://supabase.com/docs)
- [Supabase RLS](https://supabase.com/docs/guides/auth/row-level-security)
- [shadcn/ui](https://ui.shadcn.com/)
- [python-stix2](https://stix2.readthedocs.io/)
- [Claude Code Docs](https://docs.claude.com/en/docs/claude-code/overview)

---

**עדכון אחרון:** 2026-06-08 · **גרסה:** v1.1 · **גל נוכחי:** גל 1 שלב 1.2
