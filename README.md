# Agentic Ops & Reconciliation Triage System

A containerized multi-agent operations workflow built with the **OpenAI Agents SDK** that automates batch payment/settlement discrepancy detection and correlates anomalies with microservice logs to generate structured root-cause triage reports.

## Architecture

```text
+--------------------------+       +----------------------------------+
| Expected vs. Actual      |       | Microservice Operational Logs    |
| Settlement Ledgers (JSON)|       | (pos-gateway, hsm-auth, ledger)  |
+------------+-------------+       +----------------+-----------------+
             |                                      |
             v                                      v
+--------------------------+       +----------------------------------+
| inspect_settlement_      |       | search_service_logs              |
| discrepancies (Tool)     |       | (Tool)                           |
+------------+-------------+       +----------------+-----------------+
             |                                      |
             +------------------+-------------------+
                                |
                                v
              +-----------------------------------+
              | Ops_Reconciliation_Coordinator    |
              | (OpenAI Agents SDK Orchestrator)  |
              +-----------------+-----------------+
                                | Handoff
                                v
              +-----------------------------------+
              | Log_Diagnostics_Specialist        |
              | (Root-Cause Correlation Agent)    |
              +-----------------+-----------------+
                                |
                                v
              +-----------------------------------+
              | Markdown Incident Triage Report   |
              | (output/triage_report.md)         |
              +-----------------------------------+