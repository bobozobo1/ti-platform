# PRD-MVP.md

> **גרסת MVP מצומצמת.** המסמך הזה מתאר רק מה שייבנה ב-Phases 0–4. החזון המלא מתואר ב-`PRD-v2.md`.

---

## עיקרון מארגן

**אנחנו בונים כלי שאני (המשתמש) ארצה להשתמש בו במקום הכלים הנוכחיים שלי.** כל פיצ'ר נמדד בשאלה אחת: "האם זה יחסוך לי זמן בחקירה אמיתית מחר בבוקר?"

---

## משתמש יחיד

חוקר TI שמקבל IOCs במהלך היום ורוצה enrichment מהיר עם פיבוט ויזואלי. עובד לבד, בלי team collaboration. חיבור לאינטרנט יציב. דפדפן Chrome/Firefox עדכני.

---

## Scope — מה נכלל

### Phase 0: Foundation
- Account management (single user, magic link login)
- Empty app deployed to production
- Database schema migrations working
- CI/CD pipeline running

### Phase 1: Single IOC Lookup
- Form עם שדה אחד — IOC input
- Auto-detection של type (IP/domain/hash/URL)
- Enrichment מ-3 sources (VT, AbuseIPDB, WHOIS)
- תצוגת תוצאות בכרטיסיות
- Error handling — אם API נכשל, מציגים partial result

### Phase 2: Persistence & History
- כל lookup נשמר ל-DB
- History sidebar — רשימת lookups קודמים
- Search ב-history
- Re-run של lookup קיים
- Tagging חופשי על investigations

### Phase 3: Investigation Graph
- Cytoscape.js graph view
- Lookup ראשוני יוצר node מרכזי
- Enrichment results הופכים ל-nodes משויכים
- Click on node → details panel
- Double-click → enrich this node
- Save/load investigations
- Export to JSON

### Phase 4: External Sharing (Optional)
- Multiple users
- Read-only sharing of investigations
- Comments on nodes
- Export to STIX 2.1 bundle

---

## Out of Scope — מה לא נכלל

- ABAC permissions / TLP / Classification
- Inbox / Triage workflow
- Playbook engine מורכב
- AI suggestions
- Inference engine
- Real-time collaboration
- Multi-tenancy
- Mobile UI
- ATT&CK mapping
- Notification center
- Webhooks
- TAXII server
- Connector registry
- Diamond Model view
- Kill Chain view

**אל תוסיף כלום מהרשימה הזו ל-MVP גם אם יש זמן.** החזון המלא בא אחרי שיש משתמשים.

---

## Acceptance Criteria — Phase 1

```
Given: I am logged in to the app
When: I enter "8.8.8.8" in the IOC input field and click "Investigate"
Then:
  - Within 2 seconds, a loading state appears
  - Within 10 seconds, results are displayed
  - I see a card for VirusTotal with detection ratio
  - I see a card for AbuseIPDB with confidence score
  - I see a card for WHOIS with registrar info
  - If any API fails, I see a clear error tag for that source
  - Other sources still display their results

Given: I enter an invalid IOC like "not-an-ip"
When: I click "Investigate"
Then:
  - I see a clear error message: "Could not detect IOC type"
  - No API calls are made
  - The form is not cleared
```

---

## Acceptance Criteria — Phase 3

```
Given: I have completed an investigation on "evil-update.com"
When: I view the investigation
Then:
  - I see a graph with the domain as a central node
  - WHOIS info appears as a related node
  - Each subdomain from CT logs appears as a connected node
  - VirusTotal detection ratio shows as a badge on the central node
  - I can click on any node to see its details

Given: I'm viewing the investigation graph
When: I double-click on a subdomain node
Then:
  - That node becomes the new center
  - Enrichment runs on that subdomain
  - New related nodes appear
  - The graph layout adjusts smoothly
  - The original "evil-update.com" remains visible
```

---

## Success Metrics

| Phase | Metric | Target |
|---|---|---|
| 0 | Deployment works | login → dashboard within 30 sec |
| 1 | Time to enrich an IOC | < 10 seconds for 3 sources |
| 1 | I use the tool at work | At least 1 real lookup |
| 2 | Migration to new tool | 50% of my lookups happen here |
| 3 | Time saved per investigation | At least 5 min vs current workflow |
| 4 | Second user | 1 colleague tries it and gives feedback |

**אם לא מגיעים למדד של phase, לא עוברים לבא.**

---

## Anti-Goals

דברים שאנחנו **לא** מנסים להשיג:

1. **לא מנסים להחליף את OpenCTI** — הם enterprise. אנחנו personal tool.
2. **לא מנסים להיות multi-tenant SaaS** ב-MVP — single user / single deployment.
3. **לא מנסים לתמוך בכל IOC type** — 4 בלבד ב-MVP.
4. **לא מנסים להיות feature-complete** — מנסים להיות useful.

---

## Decision Points

יש שני decision points פורמליים:

**End of Phase 3:**
- האם אני משתמש בכלי בעבודה האמיתית שלי לפחות 50% מהזמן?
  - **כן** → המשך ל-Phase 4
  - **לא** → עצור. Retrospective. אולי project closed.

**End of Phase 4:**
- האם משתמש שני אקטיבי?
  - **כן** → התחל לחשוב על monetization / scaling
  - **לא** → אולי המוצר הוא personal tool בלבד, וזה בסדר.

---

**גרסה:** 1.0 · **תאריך:** [תאריך התחלה]
