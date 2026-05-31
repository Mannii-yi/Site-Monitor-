# Site-Monitor-
 
# Serverless Synthetic Website Uptime Monitor

A lightweight, production-grade automated synthetic monitoring tool that tracks website availability, logs performance metrics/anomalies, and securely stores downtime records. Built entirely serverless using a Python runtime, GitHub Actions cron orchestration, and a PostgreSQL database.

## 🚀 Architectural Overview

Instead of relying on heavy, expensive third-party infrastructure, this project leverages managed serverless environments to maintain continuous checking loops completely free of cost.

* **Orchestration:** GitHub Actions triggers a headless runner every 30 minutes via a secure Linux environment (cron job).
* **Monitoring Engine:** A Python script executes synchronous HTTP connection testing with explicit request timeout handling to catch silent freezes, socket drops, and bad HTTP status codes.
* **Data Layer:** A decoupled relational database hosted via Supabase (PostgreSQL) archives immutable fault logs for historical uptime analysis.
* **Security:** Complete elimination of credential leakage using GitHub Repository Secrets to inject environment variables at runtime.

---

## 🛠️ Tech Stack & Tools

* **Language:** Python 3.x
* **Libraries:** `requests` (Network Layer), `supabase-py` (Database Driver)
* **Automation:** GitHub Actions (CI/CD / Event-driven Workflows)
* **Database:** Supabase / PostgreSQL (Cloud-managed Relational Database)

---

## 📂 Database Schema Design

The remote PostgreSQL database logs service degradation data using the following structured schema:

```sql
CREATE TABLE downtime_logs (
    id SERIAL PRIMARY KEY,
    website_url TEXT NOT NULL,
    status_code INTEGER,       -- Captures anomalous HTTP responses (e.g., 500, 404)
    error_message TEXT,        -- Logs raw system exceptions (e.g., ConnectionTimeout)
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
