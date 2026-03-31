# OrchestraFlow: E-Commerce Data Pipeline Orchestration  Orchestration

![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)
![Next JS](https://img.shields.io/badge/Next-black?style=for-the-badge&logo=next.js&logoColor=white)

**OrchestraFlow** is a production-level workflow orchestration project showcasing advanced **Apache Airflow** capabilities. It simulates an E-commerce data pipeline (Extraction, Transformation, and Data Warehouse Loading/Reporting) applying advanced features like `TaskGroups`, `Branching`, `FileSensors`, and `TriggerRules`.

The project is paired with a stunning **Next.js** interactive dashboard (Neon Cyberpunk Theme) to visualize pipeline status visually, ready for recruiter presentations.

## 🚀 Key Features Demonstrated
- **Distributed Architecture:** Includes `docker-compose` setup for Airflow with `CeleryExecutor` + `PostgreSQL` + `Redis`.
- **Advanced Airflow Entities:**
  - `TaskGroups` for complex parallel processing logic inside Transformation.
  - `FileSensors` to conditionally execute ETL nodes based on upstream file drops.
  - `BranchPythonOperator` routing to distinct reporting patterns (Weekday vs. Weekend).
  - `TriggerRules` (e.g., `none_failed_min_one_success`) joining branching logic effectively.
  - Intelligent Error Handling (custom timeouts, retry mechanisms).
- **Quality Assurance:** Included Data Quality hooks running directly within Airflow tasks to validate transformations inline before loading to the Data Warehouse.

## 🏗️ System Architecture

*See `docs/architecture.md` for Mermaid diagrams of the pipeline structure.*

1. **Ingestion (DAG 1):** Python Extractors retrieve mock Sales and Inventory data to local staging folders `/data/raw`. Handled by parallel `BashOperators`.
2. **Transformation (DAG 2):** Monitored by a `FileSensor`. Once staging is reached, parallel `TaskGroups` trigger cleaning processes (`PythonOperator`) and Data Quality sanity checks on output files outputted to `/data/processed`.
3. **Reporting (DAG 3):** `BranchPythonOperator` identifies if the execution relates to a business weekday or weekend to load differential insights to the Postgres Data Warehouse.

## 💻 Tech Stack
- **Orchestration:** Apache Airflow 2.7+ (CeleryExecutor)
- **Database / Cache:** PostgreSQL 13, Redis
- **Data Processing:** Python (Pandas)
- **Frontend / Dashboard:** Next.js (App Router), Tailwind CSS
- **Containerization:** Docker Desktop & Docker Compose

## 🛠️ How to Run Locally

### 1. Start the Airflow Backend
Ensure Docker Desktop is running (requires ~4GB allocated RAM).
```bash
git clone https://github.com/your-username/airflow-orchestration-project.git
cd airflow-orchestration-project

# Initialize the Airflow Database (only first time)
docker-compose up airflow-init

# Start the full stack (Webserver, Scheduler, Worker, Postgres, Redis)
docker-compose up -d
```
Access the Airflow UI at `http://localhost:8080`. (User/Pass: `admin` / `admin`).

### 2. Start the Portfolio Dashboard
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to see the beautiful portfolio representation.

## ✨ About this Project
Designed as a capstone project for **Senior Data Engineer / Analytics Engineer** portfolios to prove capabilities deploying, scaling, and managing true scalable `DAG` definitions outside simple linear ETL scripts.
