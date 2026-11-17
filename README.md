# Lab 3 – Component Modelling & Architectural Pattern Selection

**Problem Statement #49 – Webhook Ingestion & Retry Mechanism Hub** (same scenario as Lab 1 and Lab 2)

## Deliverables
| File | Description |
|---|---|
| `Component_Diagram.png` | UML component diagram: 7 components and 8 provided/required (ball-and-socket) interfaces, grouped into an edge tier, a delivery tier, and data, operations & targets, plus 2 `<<use>>` dependencies |
| `Component_Diagram.svg` | Vector source of the same diagram |
| `Architecture_Justification.docx` / `.pdf` | One-page justification: chosen architecture, styles compared, two reasons, security advantage, performance benefit |

## Architecture: Microservices (edge gateway + queue-based delivery)

| Component | Responsibility | Requirements |
|---|---|---|
| Ingestion Gateway | Public HTTPS endpoint; accepts webhooks and replies 202 Accepted | FR-002, NFR-001 |
| Signature Verifier | HMAC-SHA256 check against the source secret; drops duplicate event IDs | FR-005 |
| Event Queue | Buffers accepted events between ingestion and delivery; absorbs bursts | NFR-001 |
| Delivery Worker | Routes each event to its target and records the result | FR-001 |
| Retry & DLQ Manager | Exponential backoff (1 s, 2 s, 4 s, 8 s); dead-letter queue with replay and discard | FR-001, FR-003 |
| Event Log Store | Durable, append-only log of every request and delivery attempt | FR-002 |
| Config & Monitoring Service | Sources, secrets, routes and retry policy; delivery metrics dashboard | FR-004, NFR-002 |

External systems: **Third-Party Service** (sends webhooks) and **Internal Service** (receives deliveries).

## Interfaces

| Interface | Provider → Requirer | Technology |
|---|---|---|
| IWebhookIngest | Ingestion Gateway → Third-Party Service | HTTPS POST + HMAC signature header |
| ISignatureCheck | Signature Verifier → Ingestion Gateway | Internal API call |
| IEnqueue | Event Queue → Ingestion Gateway | Message queue (AMQP publish) |
| IEventLog | Event Log Store → Event Queue | SQL, append-only |
| IEventConsume | Event Queue → Delivery Worker | Message queue (AMQP consume) |
| IRetrySchedule | Retry & DLQ Manager → Delivery Worker | Internal API (backoff scheduling) |
| IDelivery | Internal Service → Delivery Worker | HTTPS POST |
| IRouteConfig | Config & Monitoring Service → Retry & DLQ Manager | REST (routes, retry policy) |

Usage dependencies (`<<use>>`): Ingestion Gateway → Event Log Store (write request log); Signature Verifier → Config & Monitoring Service (read source secrets).
