# CLAUDE_CONTEXT.md

> **קרא קובץ זה תחילה בכל שיחה חדשה.** הוא מכיל את כל ההקשר הקריטי על המוצר, הסטאק, ומוסכמות הפיתוח. המסמך מתעדכן אחרי כל שינוי משמעותי.

---

## 1. מה אנחנו בונים

**מוצר:** TI Investigation Platform — כלי TI אישי לחקירת IOCs.

**משתמש יחיד ב-MVP:** חוקר TI מקצועי שמשתמש בכלי בעבודה היומית.

**הצעת ערך:** משתמש מקליד IOC (IP/domain/hash/URL) ומקבל גרף ויזואלי עם enrichments אוטומטיים מ-VirusTotal, AbuseIPDB, WHOIS, ו-crt.sh. שומר היסטוריה. מאפשר חקירת pivots.

**מה אנחנו לא בונים ב-MVP:**
- אין collaboration (single user)
- אין ABAC permissions / TLP
- אין STIX 2.1 import/export מלא (רק export בסיסי)
- אין playbook engine מורכב
- אין AI suggestions מבוסס ML

המוצר השלם מתואר ב-`docs/PRD-v2.md`. המסמך שמשרת את הפיתוח בפועל הוא `docs/PRD-MVP.md`.

---

## 2. מי אני (המשתמש שמדבר איתך)

- **תפקיד:** Product Manager + Domain Expert ב-TI
- **רקע פיתוח:** מוגבל. למד תוך כדי.
- **תפקידי בפרויקט:** מגדיר דרישות, בודק התנהגות, מאשר/דוחה החלטות. **לא קורא קוד מקצועית.**
- **ההשלכות בעבודה איתי:**
  - אל תניח שאני מבין מונחים טכניים. הסבר במילים פשוטות.
  - תמיד תן לי בחירה בין אפשרויות עם הסבר ה-trade-offs, אל תבחר עבורי.
  - כשאתה כותב קוד, תסביר ב-comments מה הוא עושה.
  - אם אני מבקש משהו שיכניס באג ידוע, **תזהיר אותי לפני שתעשה את זה.**
  - אם יש לי הנחה לא נכונה, תתקן אותי בנימוס.

---

## 3. עקרונות עבודה (Non-Negotiable)

### 3.1 — Acceptance Criteria First
לכל משימה אני אספק לך acceptance criteria מפורטים בסגנון Given/When/Then. אם הם לא מספקים, **תשאל לפני שתתחיל לכתוב קוד**.

### 3.2 — Tests are Mandatory
כל פיצ'ר חייב Playwright E2E test. בלי יוצא מהכלל. כשאתה כותב פיצ'ר, אתה כותב גם את הטסט שלו באותה session.

### 3.3 — Small Diffs
אל תכתוב 500 שורות בבת אחת. עבוד ב-increments של 50–100 שורות, תעצור, תאשר איתי, ותמשיך.

### 3.4 — Self-Review Required
אחרי שאתה מסיים פיצ'ר, **לפני שאני בודק**, תעשה self-review:
- מה ה-3 הדברים הכי שבירים בקוד הזה?
- מה ה-edge cases שלא טיפלתי בהם?
- מה הייתי משנה אם הייתי מתחיל מחדש?

### 3.5 — Documentation Updates
אחרי כל session:
1. עדכן את `CLAUDE_CONTEXT.md` (סעיף Status נוכחי)
2. אם החלטנו משהו טכני — הוסף ל-`docs/DECISIONS.md`
3. אם הוספנו dependency — עדכן `README.md`

### 3.6 — אסור Over-Engineering
**אנחנו בונים MVP ל-user יחיד.** לא צריך:
- microservices
- caching layers מורכבים
- queue systems
- multiple databases
- abstractions "for future flexibility"

אם אתה רוצה להוסיף משהו "ליום שצריך אותו" — **תשאל אותי קודם**. ברירת המחדל היא לא.

### 3.7 — Security Defaults
- API keys ב-`.env` בלבד, לעולם לא ב-git
- כל user input מאומת ב-backend (לא רק frontend)
- HTTPS only ב-production
- אין logging של PII או IOCs בלוגים פתוחים

---

## 4. Stack טכני (לא משתנה ללא אישור)

### Frontend
- **React 18** + **TypeScript** (strict mode)
- **Vite** (build tool, מהיר יותר מ-CRA)
- **Tailwind CSS** (styling)
- **Cytoscape.js** (graph rendering)
- **shadcn/ui** (component library — מתבסס על Radix)
- **TanStack Query** (server state management)
- **React Router** (routing)
- **Zustand** (client state, רק כשTanStack Query לא מספיק)

### Backend
- **Python 3.11+**
- **FastAPI** (web framework)
- **Pydantic v2** (validation)
- **httpx** (async HTTP client)
- **python-stix2** (STIX 2.1 handling)

### Infrastructure
- **Supabase** — Postgres + Auth + RLS + real-time
- **Vercel** — frontend hosting
- **Railway** — backend hosting (free tier 500h/month)
- **GitHub Actions** — CI/CD

### Testing
- **Playwright** — E2E
- **Vitest** — unit tests (frontend)
- **pytest** — unit tests (backend)

### External APIs
| API | Purpose | Free Tier Limit |
|---|---|---|
| VirusTotal | IP/domain/hash reputation | 4 req/min, 500/day |
| AbuseIPDB | IP reputation | 1000/day |
| WhoisXML | WHOIS lookups | 500/month |
| crt.sh | Certificate Transparency | Unlimited |
| Shodan | (Phase 4) | 100/month |

**אם אתה רוצה להוסיף API, dependency, או service — תשאל אותי קודם.**

---

## 5. מבנה הפרויקט

```
ti-platform/
├── README.md
├── docs/
│   ├── PRD-MVP.md              # הדרישות המצומצמות שאנחנו בונים
│   ├── PRD-v2.md               # החזון המלא (reference)
│   ├── ARCHITECTURE.md         # החלטות ארכיטקטורה
│   ├── DECISIONS.md            # Decision log
│   └── CLAUDE_CONTEXT.md       # הקובץ הזה
├── frontend/
│   ├── src/
│   │   ├── components/         # רכיבי UI
│   │   ├── features/           # פיצ'רים שלמים (Investigation, Inbox, KB)
│   │   ├── lib/                # utilities, API client
│   │   ├── hooks/              # custom React hooks
│   │   ├── types/              # TypeScript types (משותפים עם backend)
│   │   └── pages/              # routing pages
│   ├── tests/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/                # FastAPI routes
│   │   ├── core/               # config, security
│   │   ├── models/             # Pydantic models
│   │   ├── services/           # business logic
│   │   │   └── enrichment/     # VT, AbuseIPDB, WHOIS connectors
│   │   └── db/                 # Supabase client
│   ├── tests/
│   └── pyproject.toml
├── tests/
│   └── e2e/                    # Playwright cross-stack tests
├── supabase/
│   └── migrations/             # SQL migrations
├── .env.example
└── .github/workflows/
```

---

## 6. Conventions

### 6.1 — Naming
- **Files:** kebab-case (`investigation-graph.tsx`)
- **Components:** PascalCase (`InvestigationGraph`)
- **Functions:** camelCase (`fetchEnrichment`)
- **Types/Interfaces:** PascalCase (`Investigation`, `IocResult`)
- **Database:** snake_case (`investigation_id`, `created_at`)
- **API endpoints:** kebab-case (`/api/v1/investigations/{id}/enrichments`)

### 6.2 — Git Commits
תבנית: `<type>: <short description>`

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

דוגמאות:
- `feat: add VirusTotal enrichment for IPs`
- `fix: handle empty WHOIS response gracefully`
- `test: add E2E for graph node click`

### 6.3 — Branch Strategy
- `main` — תמיד יציב, deployed ל-production
- `feature/<name>` — לכל פיצ'ר חדש
- PR ל-main דורש: tests passing, my approval

### 6.4 — Error Handling
- Backend מחזיר HTTP status codes נכונים (400/401/403/404/500)
- Frontend תופס שגיאות ומציג user-friendly messages
- שגיאות מ-external APIs לא קורסות את הפיצ'ר — מציגים partial result

---

## 7. Domain Knowledge — TI Concepts (Reference מהיר)

### IOC Types (שתומכים ב-MVP)
- **IP Address** — IPv4 (IPv6 ב-Phase 2)
- **Domain** — example.com
- **URL** — https://example.com/path
- **File Hash** — MD5, SHA1, SHA256
- **Email** — Phase 2

### STIX 2.1 Objects (משתמשים בלבד באלה ב-MVP)
- `indicator` — IOC עם pattern
- `observed-data` — תצפית בודדת
- `relationship` — קשר בין objects
- `bundle` — אוסף objects

### Enrichment Sources (מהי תוצאה שמורה)
- **VirusTotal:** detection ratio, last analysis date, malicious vendors list
- **AbuseIPDB:** confidence score, abuse categories, country
- **WHOIS:** registrar, creation date, contacts (privacy-aware)
- **crt.sh:** SAN list, issuer, validity period

### Confidence Scoring (החלטה ב-MVP)
פשוט. שלוש רמות:
- **High** (80–100): VT detection ratio > 5/30, או AbuseIPDB > 75
- **Medium** (50–79): VT detection 1–5, או AbuseIPDB 25–75
- **Low** (0–49): שאר המקרים

ב-Phase 3 נחליף ב-confidence model מורכב יותר.

---

## 8. Status נוכחי

### גרסה
**v0.1.0** — Phase 0 (Foundation)

### מה כבר עובד
- (כשמתחילים: ריק. תעדכן אחרי כל phase)

### בעבודה כרגע
- Setup ראשוני

### Known Issues
- (תוסיף issues שאנחנו מודעים אליהם אבל דחינו פתרון)

### TODOs (קצרי טווח)
- (משימות שמופיעות ונשכחות, תעדכן ידנית)

---

## 9. DON'Ts — דברים שכבר ניסינו ולא עבדו

(תעדכן בכל פעם שמסקנה כזו עולה. דוגמאות יבואו תוך כדי פיתוח.)

- אין דוגמאות עדיין

---

## 10. Resources — לינקים שימושיים

- [STIX 2.1 Specification](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html)
- [VirusTotal API v3 Docs](https://docs.virustotal.com/reference/overview)
- [AbuseIPDB API Docs](https://docs.abuseipdb.com/)
- [Cytoscape.js Docs](https://js.cytoscape.org/)
- [Supabase Docs](https://supabase.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)

---

**עדכון אחרון:** [תאריך] · **גרסה:** [version] · **Phase נוכחי:** [phase]
