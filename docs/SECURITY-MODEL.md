# 🔐 SECURITY-MODEL.md
## מודל האבטחה של מערכת TI Platform

> **סטטוס: גרסה ראשונה (v1.0)** — תוכנן בשלב 1.1 עם Claude (Opus).
> זה המסמך הכי חשוב בפרויקט. הוא מגדיר איך מידע מסווג מוגן.
> כל שורת קוד מושפעת מהמודל הזה.
> **לפני כתיבת קוד חדש** — קרא לפחות את §0, §2, §4.

---

## 📑 תוכן עניינים

- [§0 — עקרונות-על (3 כללי ברזל)](#0-עקרונות-על)
- [§1 — שלושת ממדי ההרשאה](#1-שלושת-ממדי-ההרשאה)
- [§2 — Policy Engine](#2-policy-engine)
- [§3 — Default Deny](#3-default-deny)
- [§4 — Leak Surfaces — מיפוי מלא וחסימות](#4-leak-surfaces)
- [§5 — Supabase RLS vs Application Layer](#5-supabase-rls-vs-application-layer)
- [§6 — Testing Strategy ל-Security](#6-testing-strategy)
- [§7 — Audit Log](#7-audit-log)
- [§8 — Decisions Log (security-specific)](#8-decisions-log)

---

<a name="0-עקרונות-על"></a>
## §0 — עקרונות-על (קבועים — לא משתנים)

שלושה כללי ברזל שכל המערכת בנויה סביבם:

1. **Default Deny** — כל גישה נדחית כברירת מחדל. גישה ניתנת רק כשכל תנאי ההרשאה מתקיימים.
2. **Test the Denial** — לכל פיצ'ר, ה-test הראשון מוכיח שמשתמש לא מורשה **לא** רואה את המידע. Red-Green: רואים נכשל לפני המימוש, עובר אחרי.
3. **No Leak Surfaces** — מידע מסווג לא דולף דרך error messages, counts, search, autocomplete, logs, או timing. כל אחד מאלה הוא vector שחייב חסימה אקטיבית.

---

<a name="1-שלושת-ממדי-ההרשאה"></a>
## §1 — שלושת ממדי ההרשאה

המערכת בודקת **שלושה ממדים בכל גישה — AND לוגי** (כל השלושה חייבים להתקיים).

> **חשוב — שינוי ממה שהיה ב-CLAUDE.md:**
> המודל הקלאסי של "Clearance Level (UNCLASSIFIED→TOP SECRET) + TLP (WHITE→RED)" **לא בשימוש** בפרויקט הזה.
> במקום זה — **TLP הוא הסולם היחיד של רגישות**, ו-Permission Level הוא ממד נפרד שמתאר **מודולים** במערכת.

### 1.1 — Permission Level (על המשתמש)

תכונה של המשתמש. קובעת **לאיזה מודולים במערכת** הוא יכול להיכנס.
היררכי: רמה גבוהה רואה הכל; רמה נמוכה רואה רק חלק.

#### רמות

| Level | Code | תיאור | מודולים מורשים |
|---|---|---|---|
| 5 | `admin` | מנהל מערכת | הכל + User Management + Audit Log + System Settings |
| 4 | `lead_analyst` | ראש צוות | Triage · Investigations · KB (R/W) · Reports · External Sharing |
| 3 | `senior_analyst` | חוקר בכיר | Triage · Investigations · KB (R/W) · Reports |
| 2 | `analyst` | חוקר | Triage · Investigations (שלו + משותפות) · KB (read) |
| 1 | `reader` | קורא | KB (read only) |
| — | `auditor` | מבקר | Audit Log בלבד (לא תוכן מבצעי). הרשאה נפרדת מההיררכיה. |

> **Admin כפוף ל-ABAC.** admin רואה את ה-modules הניהוליים, אבל **לא** רואה אוטומטית content מסווג שאין לו NTK עליו. ניהול ≠ קריאה. ראה §8 — Decision Log.

#### DB Schema

```sql
-- טבלת users (extends auth.users של Supabase)
CREATE TABLE public.user_profiles (
  id           UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email        TEXT NOT NULL UNIQUE,
  full_name    TEXT NOT NULL,
  perm_level   permission_level NOT NULL DEFAULT 'reader',  -- enum
  is_auditor   BOOLEAN NOT NULL DEFAULT FALSE,              -- orthogonal to perm_level
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  -- forward-compat: tenant_id (גל 7)
  tenant_id    UUID
);

CREATE TYPE permission_level AS ENUM (
  'reader', 'analyst', 'senior_analyst', 'lead_analyst', 'admin'
);
```

**מי משנה perm_level?** רק `admin`. כל שינוי → audit log entry (ראה §7).

---

### 1.2 — Need-to-Know (NTK) — על Investigation/Container

תכונה של ה-investigation: רשימת משתמשים שמורשים לראות אותה.
**ברירת מחדל:** רק היוצר (`owner`).
**השיתוף:** owner (או lead_analyst+) יכולים להוסיף משתמשים נוספים.

#### DB Schema

```sql
CREATE TABLE public.investigations (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title        TEXT NOT NULL,
  description  TEXT,
  owner_id     UUID NOT NULL REFERENCES public.user_profiles(id),
  tlp          tlp_level NOT NULL DEFAULT 'amber',
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  -- ...
  tenant_id    UUID  -- forward-compat
);

-- NTK table — relationship table של "מי רואה איזו investigation"
CREATE TABLE public.investigation_access (
  investigation_id UUID NOT NULL REFERENCES public.investigations(id) ON DELETE CASCADE,
  user_id          UUID NOT NULL REFERENCES public.user_profiles(id) ON DELETE CASCADE,
  access_role      access_role NOT NULL,  -- 'owner' | 'editor' | 'viewer'
  granted_by       UUID NOT NULL REFERENCES public.user_profiles(id),
  granted_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (investigation_id, user_id)
);

CREATE TYPE access_role AS ENUM ('owner', 'editor', 'viewer');
```

**עקרון:** **אין** investigation בלי לפחות שורה אחת ב-`investigation_access` עם `owner`. אכיפה ב-triggers.

---

### 1.3 — TLP Marking — על כל Object

תכונה של ה-object (investigation, IOC, KB entry, sighting...).
**היוצר קובע** את ה-TLP בעת יצירה. ניתן לעדכן רק כלפי מעלה (יותר מגביל), לא כלפי מטה. שינוי TLP → audit.

#### רמות (TLP 2.0 — סטנדרט FIRST.org)

| TLP | מתי משתמשים |
|---|---|
| `CLEAR` (לשעבר WHITE) | מידע ציבורי. שיתוף ללא הגבלה. |
| `GREEN` | לקהילה המקצועית. שיתוף בקהילה הרחבה, לא פרסום פומבי. |
| `AMBER` | מוגבל לארגון + שותפים מהימנים על בסיס need-to-know. |
| `AMBER+STRICT` | מוגבל לארגון בלבד. אסור לשתף עם שותפים. |
| `RED` | רק לעיניים של נמענים ספציפיים. **enforcement חזק** במערכת. |

#### DB Schema (חלק עליון של כל טבלה שמכילה data מסווג)

```sql
-- בכל טבלה שיש בה content (investigations, iocs, kb_objects, sightings)
ALTER TABLE public.investigations ADD COLUMN tlp tlp_level NOT NULL DEFAULT 'amber';

CREATE TYPE tlp_level AS ENUM ('clear', 'green', 'amber', 'amber_strict', 'red');

-- רשימת נמענים ל-RED objects בלבד
CREATE TABLE public.tlp_red_recipients (
  resource_type TEXT NOT NULL,           -- 'investigation' | 'ioc' | 'kb_object'
  resource_id   UUID NOT NULL,
  user_id       UUID NOT NULL REFERENCES public.user_profiles(id),
  granted_by    UUID NOT NULL REFERENCES public.user_profiles(id),
  granted_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (resource_type, resource_id, user_id)
);
```

#### התנהגות לפי TLP

| TLP של object | יש NTK | אין NTK |
|---|---|---|
| CLEAR / GREEN / AMBER / AMBER+STRICT | Read מלא | 404 |
| RED + ב-recipients | Read מלא | — |
| RED + לא ב-recipients | **Placeholder** ("TLP:RED · restricted") | 404 |

**הסבר Placeholder:** משתמש שיש לו NTK ל-investigation אבל לא ל-RED object בתוכה — רואה ש-object קיים, רואה את ה-TLP tag, אבל **לא** רואה תוכן (title שמדמה, ללא detail, ללא relationships). זו דליפת קיום יזומה ומקובלת — ראה §4 ו-§8.

---

<a name="2-policy-engine"></a>
## §2 — Policy Engine

**הלב של ה-security.** פונקציה מרכזית אחת ב-`backend/app/core/security.py`. כל endpoint עובר דרכה. אין בדיקות מפוזרות.

### Interface (Python / Pydantic)

```python
# backend/app/core/security.py

from enum import Enum
from typing import Literal
from pydantic import BaseModel

class Action(str, Enum):
    READ = "read"
    WRITE = "write"
    PROMOTE = "promote"      # promote investigation IOC → KB
    EXPORT = "export"        # export to external/ISAC
    REVOKE = "revoke"        # revoke KB entry
    ADMIN = "admin"          # admin action (user mgmt etc)

class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    PLACEHOLDER = "placeholder"  # see RED behavior

class PolicyResult(BaseModel):
    decision: Decision
    reason_code: str        # for audit log; NEVER returned to user
    # NOTE: no "reason" string to user — all denials look identical externally

async def check_policy(
    *,
    user: UserProfile,
    action: Action,
    resource_type: Literal["investigation", "ioc", "kb_object", "sighting", "admin"],
    resource_id: UUID | None,   # None for "list" / "create" actions
) -> PolicyResult:
    """
    The ONE function that every endpoint calls.
    Returns ALLOW / DENY / PLACEHOLDER.
    Constant-time (see §4).
    Logs to audit_log (see §7).
    """
    ...
```

### סדר הבדיקה (Flowchart)

```
                  check_policy(user, action, resource)
                              │
                              ▼
                   ┌─────────────────────┐
                   │ 0. is_active?       │
                   │    user not banned  │
                   └──────┬──────────────┘
                          │ no → DENY (reason: inactive_user)
                          ▼ yes
                   ┌─────────────────────┐
                   │ 1. Permission Level │
                   │    perm_level OK    │
                   │    for module?      │
                   └──────┬──────────────┘
                          │ no → DENY (reason: insufficient_perm_level)
                          ▼ yes
                   ┌─────────────────────┐
                   │ 2. Need-to-Know     │
                   │    has access to    │
                   │    container?       │
                   └──────┬──────────────┘
                          │ no → DENY (reason: no_ntk)
                          ▼ yes
                   ┌─────────────────────┐
                   │ 3. TLP Check        │
                   │    resource.tlp     │
                   │    == RED?          │
                   └──────┬──────────────┘
                          │ no (CLEAR/GREEN/AMBER) → ALLOW
                          ▼ yes (RED)
                   ┌─────────────────────┐
                   │ 4. RED Recipients   │
                   │    user in list?    │
                   └──────┬──────────────┘
                          │ yes → ALLOW
                          ▼ no
                   ┌─────────────────────┐
                   │ 5. Container TLP    │
                   │    container itself │
                   │    == RED?          │
                   └──────┬──────────────┘
                          │ yes → DENY (reason: red_container_no_recipient)
                          ▼ no
                   ┌─────────────────────┐
                   │ 6. PLACEHOLDER      │
                   │ user has NTK to     │
                   │ container, but RED  │
                   │ object inside is    │
                   │ not for them        │
                   └─────────────────────┘
```

> **Permission Level** = הדלת למודול.
> **NTK** = הדלת ל-container בתוך המודול.
> **TLP** = הסינון של objects בתוך ה-container.

### Constant-Time Guarantee

כל DENY מ-§2 חוזר ב-**אותו פרק זמן** כמו ALLOW. הסיבה: timing attack (ראה §4). מימוש:
- אם DENY ב-step 1 (perm_level) — עדיין נריץ dummy DB lookups שמדמים את שלבים 2–6.
- כל בדיקה מתעדת ל-audit log, גם אם תוצאתה הוחלטה כבר בשלב מוקדם יותר.

---

<a name="3-default-deny"></a>
## §3 — Default Deny

**כלל ברזל:** ברירת מחדל היא דחייה. גישה דורשת הוכחה אקטיבית.

### איך אנחנו מבטיחים את זה

| מקום | מנגנון |
|---|---|
| **Supabase RLS** | כל טבלה: `ALTER TABLE x ENABLE ROW LEVEL SECURITY` ואין policy = אפס שורות נראות. ה-policies הן ALLOW מפורש בלבד. |
| **FastAPI Routes** | Decorator `@requires_policy(action=...)` חובה על כל endpoint. בלי decorator → CI fails. |
| **New Module Check** | CI test שעובר על כל route ומוודא decorator קיים. |
| **Frontend** | אין סינון ב-frontend. אם backend לא שלח — frontend לא מנחש. |
| **Type System** | מודלים של Pydantic סומנים `restricted=True` if classified. עוטף קריאות ב-helper שדורש decision מ-Policy Engine לפני serialization. |

### ה-decorator

```python
# backend/app/core/decorators.py
def requires_policy(action: Action, resource_type: str):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(request: Request, *args, **kwargs):
            user = await get_current_user(request)
            resource_id = kwargs.get("id")  # may be None for list
            result = await check_policy(
                user=user, action=action,
                resource_type=resource_type, resource_id=resource_id,
            )
            if result.decision == Decision.DENY:
                # IMPORTANT: 404, not 403 (see §4)
                raise HTTPException(404, detail="not found")
            request.state.policy_result = result  # for downstream filtering
            return await handler(request, *args, **kwargs)
        return wrapper
    return decorator
```

---

<a name="4-leak-surfaces"></a>
## §4 — Leak Surfaces — מיפוי מלא וחסימות

**זה החלק הקריטי ביותר.** כל מקום שמידע מסווג יכול לדלוף, ואיך חוסמים אותו.

| # | Leak Surface | הסיכון | החסימה |
|---|---|---|---|
| **1** | **Error messages** | "access denied" מדליף שה-object קיים | **תמיד 404 "not found"**. לעולם לא 403. שני המקרים זהים מבחוץ. |
| **2** | **HTTP Status codes** | 403 → קיים אבל אסור · 404 → לא קיים. הבחנה = leak | **תמיד 404** ל-deny על content. 401 רק ל-not authenticated. |
| **3** | **Counts / pagination** | "showing 5 of 50" מדליף 45 מוסתרים | counts תמיד **אחרי** filtering. ה-API מחזיר רק את ה-count של מה שהמשתמש מורשה. |
| **4** | **Search results** | "3 results hidden" מדליף קיום | search מחזיר רק מה שמותר. אין "X restricted". RED placeholders **כן** מופיעים ב-search אם המשתמש יש לו NTK ל-container. |
| **5** | **Autocomplete** | השלמה אוטומטית חושפת שמות מסווגים | autocomplete מבוסס אך ורק על מה שהמשתמש כבר רשאי לראות. אין pre-fetch. |
| **6** | **Logs** | מידע מסווג בטקסט גלוי בלוגים | structured logging. שדות מסומנים `@classified` מוחלפים ב-`<REDACTED>`. Pydantic model עם `model_dump(exclude_classified=True)`. |
| **7** | **Timing** | תשובה מהירה לקיים vs not found = leak | **constant-time response**. כל check_policy לוקח min-latency אחיד (~50ms). dummy lookups ב-DENY ב-stage מוקדם. |
| **8** | **Graph nodes** | node מסווג שמגיע ל-frontend ו"מוסתר" ב-CSS | **סינון ב-backend.** API מחזיר רק nodes שהמשתמש מורשה ל. frontend לא יודע ש-nodes נוספים קיימים. Ghost edges (גל 3) — opt-in מפורש. |
| **9** | **WebSocket broadcast** | payload אחיד לכל המחוברים = דליפה לכולם | **per-recipient filtering**. כל broadcast רץ דרך check_policy לכל subscriber. אין "broadcast to room". |
| **10** | **API direct access** | עקיפת ה-UI דרך call ישיר ל-API | Policy Engine על כל endpoint. CI test מוודא decorator. אין endpoint "internal" שעוקף. |
| **11** | **RED Placeholder existence leak** (מודע) | משתמש עם NTK רואה שיש object TLP:RED בתוך container | **leak מודע ומאושר** (Q1=ג, §8). placeholder כולל **רק** type + TLP tag + ID. ללא title, description, relationships, count of similar. |
| **12** | **Email/Notification leakage** | notification email שולח details של object לא מסווג? | כל notification עובר דרך check_policy לפני שליחה. emails כוללים IDs בלבד, לא content. |
| **13** | **Export/Download** | export של list של investigations עוקף ABAC? | export עובר item-by-item דרך check_policy. format (CSV/JSON/STIX) זהה למה שהיה ב-UI. |
| **14** | **Audit log readable by wrong user** | analyst רגיל קורא audit log = רואה denials של אחרים | audit log נגיש רק ל-`auditor` role + `admin`. content של denial entries לא כולל classified payload. |
| **15** | **Error traces / Stack traces** | Python traceback בproduction מציג SQL, classified column values | production: never leak traces to client. logs only, with redaction. |
| **16** | **Network metadata** | response size שונה בין placeholder ל-real object → גודל המידע דולף | placeholder padded ל-fixed size או random-jittered. בגל 3 (גרף) — fixed-size dummy node injected if RED hidden. |
| **17** | **Cache poisoning** | TanStack Query cache mixes data בין users | per-user cache keys. logout → cache clear. שום cache לא שותף בין משתמשים. |

### Leak Surfaces חדשים — נוסיף לפי הצורך

כשמתגלה leak surface חדש בפיתוח/audit — מתעדים פה. **לא** מתקנים ושוכחים.

---

<a name="5-supabase-rls-vs-application-layer"></a>
## §5 — Supabase RLS vs Application Layer

**עיקרון: Defense in Depth.** גם RLS וגם application layer בודקים. אם אחד נכשל, השני תופס.

### חלוקת אחריות

| בדיקה | Supabase RLS | Application Policy Engine |
|---|---|---|
| user authenticated? | ✅ (auth.uid()) | ✅ (JWT validation) |
| Permission Level למודול | ❌ (לא ידוע ל-DB אם זה "module-level") | ✅ הראשי |
| NTK (יש שורה ב-investigation_access) | ✅ הראשי | ✅ duplicate check |
| TLP filtering | ✅ ברמת SELECT | ✅ לוגיקת placeholder |
| RED recipients | ✅ ברמת SELECT | ✅ לוגיקת placeholder |
| Action enforcement (write/promote/export) | ✅ ברמת INSERT/UPDATE | ✅ הראשי |
| Audit logging | ✅ trigger ב-RLS policy | ✅ check_policy |
| Constant-time | ❌ (DB עונה בזמן משתנה) | ✅ הראשי |
| Placeholder logic | ❌ (DB מחזיר שורה או לא) | ✅ הראשי |

### דוגמת RLS Policy

```sql
-- investigations: ניתן לקרוא רק אם יש NTK + TLP חוקי
CREATE POLICY "investigations_select" ON public.investigations
FOR SELECT
USING (
  -- אופציה 1: user is recipient of investigation (NTK)
  EXISTS (
    SELECT 1 FROM public.investigation_access ia
    WHERE ia.investigation_id = investigations.id
      AND ia.user_id = auth.uid()
  )
  -- TLP filtering: RED placeholder logic happens in application layer
);

-- IOCs בתוך investigation (RED hides content)
-- application layer מחליף content ב-placeholder
-- RLS מחזיר את השורה (כי NTK ל-container עבר); placeholder logic ב-application
```

> **למה לא לעשות הכל ב-RLS?** RLS לא יכול לעשות placeholder — הוא מחזיר row או לא. לוגיקת ה-placeholder היא application-only. בנוסף — RLS לא יודע על "constant-time".

---

<a name="6-testing-strategy"></a>
## §6 — Testing Strategy ל-Security

**עיקרון:** לכל פיצ'ר — denial test ראשון (Red-Green).

### דפוס Red-Green לכל פיצ'ר

```python
# tests/test_investigation_access.py

async def test_analyst_without_ntk_cannot_read_investigation():
    """RED: this MUST fail before we implement NTK filtering."""
    # given
    inv = await create_investigation(owner=other_user, tlp="amber")
    # when
    response = await client.get(f"/api/v1/investigations/{inv.id}", auth=analyst_token)
    # then
    assert response.status_code == 404           # NOT 403!
    assert response.json() == {"detail": "not found"}
    # additionally: audit log entry
    log = await get_audit_log(action="read", resource_id=inv.id, user_id=analyst.id)
    assert log.result == "deny"
    assert log.reason_code == "no_ntk"
```

### Test Categories — כל אחד חובה

| # | סוג | מה הוא בודק |
|---|---|---|
| 1 | **Denial test** | user without permission → 404 |
| 2 | **API direct test** | אותו denial test אבל ישיר ל-API (לא רק UI) |
| 3 | **Count leak test** | list endpoint לא מחזיר count של hidden items |
| 4 | **Search leak test** | search לא מצביע על קיום של מסווגים |
| 5 | **Timing test** | DENY ו-ALLOW לוקחים ±10ms זהים (95th percentile) |
| 6 | **Placeholder test** | RED object → user with NTK to container רואה placeholder, לא content |
| 7 | **Audit test** | כל denial רשום ב-audit log |
| 8 | **Network inspection test** | playwright trace — classified data לא ב-response body |
| 9 | **WebSocket per-user test** (גל 6) | user A connected, user B connected — broadcast מסונן per-user |
| 10 | **Cross-tenant test** (גל 7) | tenant A לא רואה כלום מ-tenant B |

### Test Fixtures

```python
# tests/fixtures/users.py
@pytest.fixture
async def reader(): return await create_user(perm_level="reader")
@pytest.fixture
async def analyst(): return await create_user(perm_level="analyst")
@pytest.fixture
async def senior(): return await create_user(perm_level="senior_analyst")
@pytest.fixture
async def lead(): return await create_user(perm_level="lead_analyst")
@pytest.fixture
async def admin(): return await create_user(perm_level="admin")
@pytest.fixture
async def auditor(): return await create_user(perm_level="reader", is_auditor=True)
```

### CI Gate

PR ל-`main` חייב:
1. כל ה-denial tests עוברים
2. coverage על `backend/app/core/security.py` ≥ 95%
3. אין endpoint בלי `@requires_policy` (lint rule)
4. אין serialization של model מסומן `restricted` בלי policy result attached

---

<a name="7-audit-log"></a>
## §7 — Audit Log

**עיקרון:** append-only, immutable, exportable.

### Schema

```sql
CREATE TABLE public.audit_log (
  id            BIGSERIAL PRIMARY KEY,
  timestamp     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  user_id       UUID REFERENCES public.user_profiles(id),  -- nullable (system actions)
  action        audit_action NOT NULL,
  resource_type TEXT,
  resource_id   UUID,
  result        audit_result NOT NULL,        -- 'allow' | 'deny' | 'placeholder'
  reason_code   TEXT NOT NULL,                -- machine-readable
  ip_address    INET,
  user_agent    TEXT,
  metadata      JSONB                          -- before/after values for changes
);

CREATE TYPE audit_action AS ENUM (
  'read', 'write', 'create', 'delete', 'export', 'promote',
  'revoke', 'login', 'logout', 'perm_level_change', 'ntk_grant', 'ntk_revoke',
  'tlp_change'
);

CREATE TYPE audit_result AS ENUM ('allow', 'deny', 'placeholder');

-- Indexes
CREATE INDEX idx_audit_user ON public.audit_log(user_id, timestamp DESC);
CREATE INDEX idx_audit_resource ON public.audit_log(resource_type, resource_id);
CREATE INDEX idx_audit_action ON public.audit_log(action, timestamp DESC);
```

### Immutability

```sql
-- אין UPDATE
CREATE RULE audit_log_no_update AS ON UPDATE TO public.audit_log DO INSTEAD NOTHING;
-- אין DELETE
CREATE RULE audit_log_no_delete AS ON DELETE TO public.audit_log DO INSTEAD NOTHING;

-- RLS: רק auditor + admin רואים
CREATE POLICY "audit_log_select" ON public.audit_log
FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM public.user_profiles up
    WHERE up.id = auth.uid()
      AND (up.is_auditor = TRUE OR up.perm_level = 'admin')
  )
);

-- INSERT: רק service role (אפליקציה)
CREATE POLICY "audit_log_insert" ON public.audit_log
FOR INSERT
WITH CHECK (auth.role() = 'service_role');
```

### תיעוד מינימלי לכל אירוע

| שדה | חובה? | הערה |
|---|---|---|
| timestamp | ✅ | UTC, ISO 8601 |
| user_id | ✅* | NULL מותר רק ל-system actions |
| action | ✅ | enum |
| resource_type | ✅ | אלא אם זה login/logout |
| resource_id | ⚠️ | רוב המקרים — chyba list operations |
| result | ✅ | allow / deny / placeholder |
| reason_code | ✅ | machine-readable: `no_ntk`, `insufficient_perm_level`, etc. |
| ip_address | ✅ | מ-X-Forwarded-For ב-FastAPI |
| user_agent | ✅ | לזיהוי bot/cli vs browser |
| metadata | optional | JSONB עם before/after לשינויי הרשאה |

### Retention

ברירת מחדל: **שנה**. אחרי שנה — archive ל-cold storage (gz JSON ב-Supabase Storage). אפשר להאריך לפי מדיניות ארגונית.

---

<a name="8-decisions-log"></a>
## §8 — Decisions Log (security-specific)

החלטות security שהתקבלו במהלך שלב 1.1.

### 2026-06-08 — TLP-Only Classification Model

**Context:** ההצעה הראשונית הייתה Clearance Levels (UNCLASSIFIED→TOP SECRET) **בנוסף** ל-TLP. בדיון הוחלט שהמודל הארגוני משתמש ב-TLP בלבד כסולם רגישות.

**Decision:** TLP הוא ממד הסיווג היחיד. במקום Clearance הקלאסי — Permission Level שמתאר מודולים במערכת (RBAC-style).

**Alternatives:**
- Clearance + TLP נפרדים — נדחה (מורכב מדי, לא תואם את המודל הארגוני)
- TLP בלבד בלי Permission Level — נדחה (חוקרים רגילים יראו admin panel)

**Trade-offs:**
- כל המודל פשוט יותר — ממד אחד של "רגישות תוכן"
- Permission Level הוא RBAC, לא ABAC — אבל זה תואם את המציאות הארגונית
- Need-to-Know עושה את העבודה של "fine-grained access" שClearance עשה בעבר

---

### 2026-06-08 — RED Placeholder (Q1=ג)

**Context:** TLP:RED על object בתוך investigation שהמשתמש יש לו NTK. מה הוא רואה?

**Decision:** Placeholder. המשתמש רואה ש-object קיים + TLP tag, אבל לא תוכן.

**Alternatives:**
- (א) Hidden לחלוטין — בטוח יותר, אבל מקשה על workflow ארגוני
- (ב) Visible כרגיל + תווית RED — מסוכן, לא ABAC אמיתי
- (ג) Placeholder — בחירתנו

**Trade-offs:**
- **Leak מודע:** קיום של RED objects דולף לכל מי שיש לו NTK ל-container. מתועד ב-§4 leak #11.
- חוויה ארגונית טובה: חוקר יודע שיש מידע שאסור לו, יכול לבקש גישה.
- Container TLP:RED + לא ב-recipients = NO placeholder, full 404. (Q1 follow-up answer)

---

### 2026-06-08 — Admin Subject to ABAC

**Context:** admin = single point of failure אם רואה הכל אוטומטית.

**Decision:** Admin רואה את ה-modules הניהוליים (user mgmt, audit log, system settings), אבל **לא** רואה content מסווג בלי NTK ספציפי.

**Alternatives:**
- Admin sees all — נדחה (single point of failure, חסר accountability)

**Trade-offs:**
- admin שצריך לחקור bug חייב לבקש NTK מ-owner. תיעוד מלא ב-audit.
- כל admin = שני אנשים (אחד יוצר user, שני מאשר). future enhancement, לא day 1.

---

### 2026-06-08 — Single Tenant Day 1, Multi-Tenant Schema Forward-Compat

**Context:** המערכת לארגון אחד. multi-tenant מתוכנן לגל 7.

**Decision:** כל הטבלאות יכללו `tenant_id UUID` מה-day-1, אבל לא נשתמש בו (NULL מותר). בגל 7 — מילוי + RLS policies.

**Alternatives:**
- בלי tenant_id מהתחלה — נדחה (migration גדולה בגל 7)
- multi-tenant מ-day 1 — נדחה (over-engineering לפני שצריך)

**Trade-offs:**
- ~5 שדות מיותרים בתחילה
- חוסך migration ענקית בגל 7

---

### 2026-06-08 — Email + Password Day 1, SSO Later

**Context:** איך משתמשים מתחברים?

**Decision:** Supabase Auth — email + password. session 24h, refresh 7d. 2FA אופציונלי (חובה ל-admin). SSO (Google/Entra) מתוכנן לגל 5+.

**Alternatives:**
- SSO mandatory — נדחה (יעכב dev, לא נחוץ לעבודה ראשונית)
- No 2FA at all — נדחה (admin = יעד תקיפה ראשון)

**Trade-offs:**
- חוקרים יצטרכו לזכור password (password manager required)
- admin עם 2FA חובה — קצת חיכוך, שווה את זה.

---

### 2026-06-08 — Constant-Time Policy Decisions

**Context:** Timing attack שמבדיל בין "DENY מוקדם (perm_level)" ל-"DENY מאוחר (TLP recipient)".

**Decision:** כל check_policy מבצע את כל ה-stages הלוגיים גם אם DENY מוקדם. response time בכוונה אחיד (~50ms minimum).

**Alternatives:**
- Random jitter בלבד — נדחה (סטטיסטית עדיין דליף, attacker אוסף מדגם)
- אין הגנת timing — נדחה (leak #7 מוכר)

**Trade-offs:**
- כל request לוקח לפחות 50ms — לא מורגש למשתמש, חוסם attack vector שלם

---

## 🚧 פתוחים — לדיון בעתיד

- **Group-level NTK?** האם נוסיף "team" entity ש-NTK יכול להינתן ל-team כולו (לא רק user)? — תלוי במציאות הארגונית. עדיין user-level בלבד.
- **Time-bounded NTK?** "Analyst X רואה investigation Y עד 30 לדצמבר." — feature לגל 5+.
- **Break-Glass Access?** במקרה חירום, admin יכול לפצוח NTK עם תיעוד מוגבר? — לדיון בגל 6+.
- **External Sharing UI (גל 7)** — TLP אוכף את ה-export bounds. ISAC anonymization = decision-point נפרד.

---

**v1.0 · 2026-06-08 · נכתב בשלב 1.1 (Wave 1).**
**עדכון אחרון:** התקנת המודל המלא.
