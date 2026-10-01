# Support Management System

Reference implementation of the support management system specified in Jira
project **CD**. Agents take customer contact by phone, email and web, record it
as a case, work it to resolution against an SLA, and draw on a knowledge base.

- **Requirements:** [CD-81](https://harvinder-vasir.atlassian.net/browse/CD-81)
- **Epics:** 8 · **Stories:** 23 · **Sprints:** 4 (all closed)

Every module maps to exactly one Jira story, and every commit carries that
story's key, so the code and the backlog can be read against each other.

## Layout
```
support_system/
  models.py   store.py        shared records and repositories
  customers   contacts  cases foundation (Sprint 1)
  intake_*                    phone / email / web channels (Sprint 1)
  assignment routing workflow priority worklog attachments   lifecycle (Sprint 2)
  sla_* escalation notifications kb_*   service levels and knowledge (Sprint 3)
  search dashboard rbac audit csat      operate and govern (Sprint 4)
```

## Traceability
| Sprint | Story | Module |
|---|---|---|
| 1 | [CD-90](https://harvinder-vasir.atlassian.net/browse/CD-90) Maintain customer records | `support_system/customers.py` |
| 1 | [CD-91](https://harvinder-vasir.atlassian.net/browse/CD-91) Maintain contacts under a customer | `support_system/contacts.py` |
| 1 | [CD-92](https://harvinder-vasir.atlassian.net/browse/CD-92) Case model and reference numbering | `support_system/cases.py` |
| 1 | [CD-93](https://harvinder-vasir.atlassian.net/browse/CD-93) Log a phone call and raise a case | `support_system/intake_phone.py` |
| 1 | [CD-94](https://harvinder-vasir.atlassian.net/browse/CD-94) Create a case from inbound email | `support_system/intake_email.py` |
| 1 | [CD-95](https://harvinder-vasir.atlassian.net/browse/CD-95) Submit a case from the web form | `support_system/intake_web.py` |
| 2 | [CD-96](https://harvinder-vasir.atlassian.net/browse/CD-96) Assign a case to an agent | `support_system/assignment.py` |
| 2 | [CD-97](https://harvinder-vasir.atlassian.net/browse/CD-97) Queues and routing rules | `support_system/routing.py` |
| 2 | [CD-98](https://harvinder-vasir.atlassian.net/browse/CD-98) Case status workflow | `support_system/workflow.py` |
| 2 | [CD-99](https://harvinder-vasir.atlassian.net/browse/CD-99) Priority from impact and urgency | `support_system/priority.py` |
| 2 | [CD-100](https://harvinder-vasir.atlassian.net/browse/CD-100) Comments and work log | `support_system/worklog.py` |
| 2 | [CD-101](https://harvinder-vasir.atlassian.net/browse/CD-101) Attachments on a case | `support_system/attachments.py` |
| 3 | [CD-102](https://harvinder-vasir.atlassian.net/browse/CD-102) Define SLA policies | `support_system/sla_policy.py` |
| 3 | [CD-103](https://harvinder-vasir.atlassian.net/browse/CD-103) SLA timers with pause | `support_system/sla_timer.py` |
| 3 | [CD-104](https://harvinder-vasir.atlassian.net/browse/CD-104) Breach detection and escalation | `support_system/escalation.py` |
| 3 | [CD-105](https://harvinder-vasir.atlassian.net/browse/CD-105) Notify customers and agents on case events | `support_system/notifications.py` |
| 3 | [CD-106](https://harvinder-vasir.atlassian.net/browse/CD-106) Author knowledge base articles | `support_system/kb_articles.py` |
| 3 | [CD-107](https://harvinder-vasir.atlassian.net/browse/CD-107) Suggest and link articles to a case | `support_system/kb_linking.py` |
| 4 | [CD-108](https://harvinder-vasir.atlassian.net/browse/CD-108) Search and filter cases | `support_system/search.py` |
| 4 | [CD-109](https://harvinder-vasir.atlassian.net/browse/CD-109) Support dashboard metrics | `support_system/dashboard.py` |
| 4 | [CD-110](https://harvinder-vasir.atlassian.net/browse/CD-110) Role-based access control | `support_system/rbac.py` |
| 4 | [CD-111](https://harvinder-vasir.atlassian.net/browse/CD-111) Immutable case audit trail | `support_system/audit.py` |
| 4 | [CD-112](https://harvinder-vasir.atlassian.net/browse/CD-112) Customer satisfaction survey | `support_system/csat.py` |
