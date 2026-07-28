# ⚡ Energy Data Pipeline

## Overview
An automated, idempotent data ingestion pipeline that fetches live telemetry data for Onshore Wind power generation directly from the German SMARD grid API. 

This project is designed with production-grade engineering principles, ensuring data integrity, graceful handling of missing real-world sensor data, and seamless deployment via containerization. It serves as a foundational data-gathering layer for future machine learning and predictive analytics models.

## 🏗️ Architecture & Tech Stack
* **Language:** Python 3.12
* **Data Processing:** `pandas` (for time-series data cleansing and transformation)
* **Storage:** SQLite3 (persistent local database)
* **Infrastructure:** Docker & Docker Compose
* **Data Source:** [SMARD.de API](https://www.smard.de/en) (Bundesnetzagentur)

## ✨ Key Features
* **Idempotency:** The pipeline checks the database for the most recent timestamps before insertion. It can be executed 10,000 times without ever creating duplicate records.
* **Data Cleansing:** Automatically detects and drops future/unrecorded time slots (handling `NaN` values inherent in real-world grid telemetry).
* **Containerized Execution:** Fully encapsulated environment ensuring zero dependency conflicts across different machines.
* **Persistent Storage:** Utilizes Docker volumes to ensure the SQLite database updates are safely stored on the host machine.

## 🚀 Quick Start (Running via Docker)

**Prerequisites:** Docker Desktop installed.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Nort0103/energy_data_pipeline.git](https://github.com/Nort0103/energy_data_pipeline.git)
   cd energy_data_pipeline