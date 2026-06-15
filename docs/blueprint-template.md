# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Đặng Minh Chức (Cá nhân)
- [REPO_URL]: https://github.com/chuc1230/2A202600611-Dang_Minh_Chuc-Day13
- [MEMBERS]:
  - Member A: Đặng Minh Chúc | Role: All Roles (Individual Assignment)

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 10
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/pic1.PNG
- [EVIDENCE_PII_REDACTION_SCREENSHOT]:  docs/pic2.PNG
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/pic3.PNG
- [TRACE_WATERFALL_EXPLANATION]: In the Langfuse trace waterfall, the root trace `run` is executed first. It nests the RAG span `retrieve` (which fetches relevant documents based on the prompt) and the LLM span `generate` (which generates the answer using the retrieved context). Since both functions are decorated with `@observe()`, they appear as nested child spans of the main trace, allowing easy comparison of latency between retrieval and generation steps.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: docs/pic4.PNG
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 170ms |
| Error Rate | < 2% | 28d | 0% |
| Cost Budget | < $2.5/day | 1d | $0.02 |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: docs/pic5.PNG
- [SAMPLE_RUNBOOK_LINK]: docs/alerts.md#1-high-latency-p95

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: The API requests became very slow, with response latency spiking from ~170ms to over 2600ms.
- [ROOT_CAUSE_PROVED_BY]: The log entries show `latency_ms` above 2600ms, and the Langfuse trace waterfall shows the `retrieve` (RAG) span taking 2.5 seconds out of the total execution time of 2.6 seconds.
- [FIX_ACTION]: Disabled the simulated incident using `python scripts/inject_incident.py --scenario rag_slow --disable`. In a real-world system, we would add RAG request timeouts, cache frequently accessed vector search queries, or fall back to a database/lighter search index.
- [PREVENTIVE_MEASURE]: Establish a dedicated alert rule on RAG span latency, implement circuit breakers, and monitor the RAG service performance independently.

---

## 5. Individual Contributions & Evidence

### Đặng Minh Chúc
- [TASKS_COMPLETED]: Completed all technical and documentation tasks for the lab: implemented the correlation ID middleware, added log enrichment context, configured the recursive PII scrubber, resolved compatibility for Langfuse SDK v3 context updates, and simulated/resolved the RAG latency incident.
- [EVIDENCE_LINK]: (Local workspace implementation in app/middleware.py, app/main.py, app/logging_config.py, app/tracing.py)

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
