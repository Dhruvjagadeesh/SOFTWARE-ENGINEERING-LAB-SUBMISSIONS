# Lab 2 – Agile Backlog Creation & Sprint Simulation in Jira

**Problem Statement #49 – Webhook Ingestion & Retry Mechanism Hub.** The backlog is derived from the Lab 1 requirements FR-001 to FR-005, NFR-001 and NFR-002.

## Backlog

| Epic | Story | Req | Priority | Points | Sprint |
|---|---|---|---|---:|---|
| EPIC1 Webhook Ingestion | Receive and acknowledge webhooks | FR-002 | High | 5 | 1 |
| | Persist request log before acknowledging | FR-002 | High | 3 | 1 |
| | Buffer high-throughput bursts | NFR-001 | High | 8 | 2 |
| EPIC2 Security & Validation | Verify HMAC signature | FR-005 | High | 5 | 1 |
| | Ignore duplicate event IDs | FR-005 | High | 3 | 1 |
| EPIC3 Delivery & Retry | Route and deliver event to target | FR-001 | High | 5 | 1 |
| | Retry failed deliveries with exponential backoff | FR-001 | High | 3 | 2 |
| | Dead-letter queue with replay and discard | FR-003 | High | 8 | 2 |
| EPIC4 Configuration & Monitoring | Register sources and target routes | FR-004 | Medium | 3 | 1 |
| | Delivery metrics dashboard | NFR-002 | Medium | 5 | 2 |

**Sprint 1 (1 week): 24 points.** Goal: a signed webhook from a registered source is accepted, logged, de-duplicated and delivered to its internal target.
**Sprint 2 (1 week): 24 points.** Goal: failed deliveries are retried with backoff and dead-lettered, ingestion handles peak bursts, and operators can see delivery health.

Story points use the Fibonacci scale. High-throughput buffering (8) and the dead-letter queue (8) carry the most uncertainty: proving 2,500 requests/second under load, and handling exhausted retries, replay and discard.

`Jira_Backlog_Import.csv` holds the full user-story text (*As a … I want … so that …*) for each item. Each story can be typed into Jira as written, or the file can be loaded through **Settings → System → External system import → CSV**.

## Deliverables
| File | Content |
|---|---|
| `Lab2_Submission.pdf` | Backlog summary, answers to the 4 reflection questions, and all screenshots |
| `screenshots/1_backlog_epics_story_points.png` | Backlog with the Epic panel, 10 stories, priorities and story points (48) |
| `screenshots/2_sprint1_active_board.png` | Sprint 1 active sprint board |
| `screenshots/3_sprint1_burndown.png` | Sprint 1 completed: burndown (24/24 points) |
| `screenshots/4_sprint2_burndown.png` | Sprint 2 completed: burndown (24/24 points) |
| `screenshots/sprint1_complete_dialog.png` | Extra: Jira confirming Sprint 1 completed with all 6 work items done |
