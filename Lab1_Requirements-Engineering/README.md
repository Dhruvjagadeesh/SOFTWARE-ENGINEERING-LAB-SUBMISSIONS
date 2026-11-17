# Lab 1: Requirements Engineering & UML Use-Case Modelling

**Institution:** PES University – Department of Computer Science & Engineering  
**Student Name:** Dhruv Jagadeesh Hemmige  
**SRN:** PES2UG24AM053  
**Section:** 5A-AIML  

---

## 📌 Problem Statement #49
**Webhook Ingestion & Retry Mechanism Hub** (Developer Tools & IT Operations)

A resilient webhook gateway that receives third-party events, logs request payloads, delivers them to internal services, and manages dead-letter queues with exponential backoff retries. **Integration Developers** register webhook sources and target endpoints, and **System Operators** monitor delivery health and recover failed events from the dead-letter queue.

---

## 📂 Repository Contents (3 Final Deliverables)

| # | File Name | Description |
| :--- | :--- | :--- |
| **1** | `Requirements_Table_Dhruv_PES2UG24AM053.docx` | Complete Requirements Table with Functional Requirements (`FR-001` to `FR-005`) and Non-Functional Requirements (`NFR-001` to `NFR-002`), each with ID, type, description, priority, acceptance criteria (pass/fail) and rationale. |
| **2** | `Use_Case_Flow_Dhruv_PES2UG24AM053.docx` | Use-Case Flow Specification for **UC-02: Ingest and Deliver Webhook Event**, with primary/secondary actors, `<<include>>` and `<<extend>>` relationships, preconditions, postconditions, main success scenario and alternate flows (`3a`, `9a`). |
| **3** | `UML_Use_Case_Diagram_Dhruv_PES2UG24AM053.pdf` | UML Use-Case Diagram showing the system boundary, actors (**Integration Developer**, **System Operator**, plus the external **Third-Party Service** and **Internal Service**), use cases `UC-01` to `UC-07`, associations, `<<include>>`/`<<extend>>` dependencies and requirement traceability. |

---

## 👥 Actors & Core Use Cases

* **Integration Developer:**
  * `UC-01`: Register Source & Target
  * `UC-05`: Monitor Logs & Metrics
* **System Operator:**
  * `UC-04`: Manage Dead-Letter Queue *(extended by `UC-03: Replay Dead-Lettered Event`)*
  * `UC-05`: Monitor Logs & Metrics
* **Third-Party Service (external system):**
  * `UC-02`: Ingest & Deliver Webhook Event *(includes `UC-06: Verify Webhook Signature`; extended by `UC-07: Retry with Exponential Backoff`)*
* **Internal Service (external system):** receives deliveries from `UC-02` and `UC-07`

---

## 🔗 Traceability Overview

| Requirement | Use Cases |
| :--- | :--- |
| `FR-001` Ingest, forward and retry with exponential backoff | `UC-02`, `UC-07` |
| `FR-002` Durable request log before acknowledging | `UC-02`, `UC-05` |
| `FR-003` Dead-letter queue with inspect, replay and discard | `UC-04`, `UC-03` |
| `FR-004` Register sources, targets and retry policy | `UC-01` |
| `FR-005` HMAC signature verification and idempotency | `UC-06` |
| `NFR-001` 99.999% reliability, 2,500 requests/second | `UC-02` |
| `NFR-002` 99.9% uptime and live delivery metrics | `UC-05` |
