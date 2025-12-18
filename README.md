# Full Stack Engineer Assessment – Backend

This project implements a **reliable webhook processing service** using **FastAPI** and **PostgreSQL**.
The service is designed to **acknowledge incoming webhooks immediately** and **process transactions asynchronously** in the background while ensuring **idempotency** and **data consistency**.

---

## 🚀 Features

* Webhook ingestion with **fast acknowledgment (`202 Accepted`)**
* Asynchronous background processing with simulated delay
* **Idempotent** transaction handling (safe for webhook retries)
* Persistent storage using PostgreSQL
* Transaction status lookup API
* Health check endpoint
* Clean, modular backend architecture

---

## 🛠️ Tech Stack

### Core Dependencies

```
fastapi==0.124.4
uvicorn==0.38.0
sqlalchemy==2.0.45
alembic==1.17.2
psycopg2-binary==2.9.11
python-dotenv==1.2.1
```

### Why These Technologies?

**FastAPI**
* Modern, fast web framework with automatic API documentation
* Built-in support for async/await and background tasks
* Excellent performance for webhook processing
* Type hints and automatic validation via Pydantic

**SQLAlchemy**
* Industry-standard ORM for Python
* Provides database abstraction and migration support
* Works seamlessly with PostgreSQL
* Ensures data integrity through declarative models

**Alembic**
* Database migration tool built on SQLAlchemy
* Enables version-controlled schema changes
* Essential for production deployments and team collaboration

**PostgreSQL (Aiven)**
* Reliable, ACID-compliant relational database
* Excellent support for concurrent transactions
* UNIQUE constraints ensure idempotency at the database level
* Using **Aiven's managed PostgreSQL** for simplified hosting and maintenance

**Uvicorn**
* Lightning-fast ASGI server
* Handles async requests efficiently
* Production-ready with minimal configuration

**psycopg2-binary**
* PostgreSQL adapter for Python
* Required for SQLAlchemy to communicate with PostgreSQL

**python-dotenv**
* Manages environment variables from `.env` files
* Keeps sensitive credentials out of source code

---

## 📂 Project Structure

```
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   └── database.py
│   ├── models/
│   │   └── transaction.py
│   ├── schemas/
│   │   └── transaction.py
│   ├── routes/
│   │   ├── health.py
│   │   ├── webhooks.py
│   │   └── transactions.py
│   └── services/
│       └── processor.py
├── alembic/
│   ├── versions/
│   └── env.py
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## 📡 API Endpoints

### Health Check

```
GET /
```

Response:

```json
{
  "status": "HEALTHY",
  "current_time": "2024-01-15T10:30:00Z"
}
```

---

### Webhook Endpoint

```
POST /v1/webhooks/transactions
```

Request Body:

```json
{
  "transaction_id": "txn_abc123",
  "source_account": "acc_user_1",
  "destination_account": "acc_merchant_1",
  "amount": 1500,
  "currency": "INR"
}
```

Response:

```
202 Accepted
```

Notes:

* Always returns `202`
* Responds within 500ms
* Safe for duplicate webhook retries

---

### Transaction Status

```
GET /v1/transactions/{transaction_id}
```

Response:

```json
{
  "transaction_id": "txn_abc123",
  "source_account": "acc_user_1",
  "destination_account": "acc_merchant_1",
  "amount": 1500,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "2024-01-15T10:30:00Z",
  "processed_at": "2024-01-15T10:30:30Z"
}
```

---

## 🔁 Background Processing

* Each webhook triggers background processing
* Processing includes a **30-second delay** to simulate external API calls
* Transaction status is updated to `PROCESSED` after completion
* Processing is fully decoupled from the webhook request lifecycle

---

## 🔐 Idempotency Strategy

* Each transaction has:
  * An internal UUID primary key
  * A unique `transaction_id` provided by the webhook sender
* A **UNIQUE constraint** on `transaction_id` ensures:
  * Duplicate webhooks do not create duplicate records
  * Only one transaction is processed per ID
* Duplicate webhooks are safely acknowledged with `202 Accepted`

---

## 🗄️ Database Migrations

This project uses **Alembic** for database schema migrations.

### Generate a new migration

After modifying your SQLAlchemy models, generate a migration:

```bash
alembic revision --autogenerate -m "describe your changes"
```

Example:

```bash
alembic revision --autogenerate -m "add transaction table"
```

### Apply migrations

To apply pending migrations to your database:

```bash
alembic upgrade head
```

### Other useful commands

```bash
# Rollback the last migration
alembic downgrade -1

# View migration history
alembic history

# Check current migration version
alembic current
```

**Note:** Ensure your `DATABASE_URL` environment variable is set before running migrations.

---

## 🧪 Running Locally

### 1. Clone the repository

```bash
git clone <repo-url>
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows PowerShell
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@host:port/database
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

---

## ✅ Testing the Service

### Test 1: Health Check

```bash
curl http://localhost:8000/
```

### Test 2: Send a Webhook

```bash
curl -X POST http://localhost:8000/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_test_001",
    "source_account": "acc_user_1",
    "destination_account": "acc_merchant_1",
    "amount": 1500,
    "currency": "INR"
  }'
```

Expected: `202 Accepted` response immediately

### Test 3: Check Transaction Status

```bash
curl http://localhost:8000/v1/transactions/txn_test_001
```

Initially shows `"status": "PROCESSING"`, then after ~30 seconds shows `"status": "PROCESSED"`

### Test 4: Duplicate Webhook (Idempotency)

Send the same webhook again:

```bash
curl -X POST http://localhost:8000/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_test_001",
    "source_account": "acc_user_1",
    "destination_account": "acc_merchant_1",
    "amount": 1500,
    "currency": "INR"
  }'
```

Still returns `202 Accepted`, but no duplicate transaction is created in the database.

---

## 🌐 Live Deployment

The service is deployed on **Render** with **Aiven PostgreSQL** as the database.

**Live API URL:** `https://backend-webhook-walnut.onrender.com`

### ⚠️ Cold Start Notice

Render's free tier may spin down the application after periods of inactivity. **The first request after inactivity may take 30-60 seconds** as the service spins back up. Subsequent requests will be fast.

### Testing the Live API

```bash
# Health check
curl https://backend-webhook-walnut.onrender.com/

# Send webhook
curl -X POST https://backend-webhook-walnut.onrender.com/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_live_001",
    "source_account": "acc_user_1",
    "destination_account": "acc_merchant_1",
    "amount": 2500,
    "currency": "INR"
  }'

# Check status
curl https://backend-webhook-walnut.onrender.com/v1/transactions/txn_live_001
```

---

## 🧠 Design Decisions & Technical Choices

### Architecture Patterns

**Separation of Concerns**
* Routes handle HTTP logic
* Services contain business logic
* Models define data structure
* Schemas validate request/response data

**Background Processing**
* FastAPI's `BackgroundTasks` provides reliable async processing
* Suitable for the assessment's requirements

**Idempotency**
* Database-level UNIQUE constraint on `transaction_id`
* Prevents race conditions and duplicate processing
* Webhook retries are handled gracefully without application logic

**Immediate Acknowledgment**
* Always return `202 Accepted` to webhook sender
* Prevents timeout issues during processing
* Follows webhook best practices

### Database Choice

**PostgreSQL via Aiven**
* ACID compliance ensures data consistency
* Excellent concurrency handling
* Managed hosting reduces operational overhead
* Built-in support for UNIQUE constraints

### Deployment Strategy

**Render Platform**
* Simple deployment from GitHub
* Automatic deployments on push
* Free tier suitable for demonstration
* Note: Cold starts may occur on free tier

---

## 📦 Requirements

All dependencies are listed in `requirements.txt`:

```
fastapi==0.124.4          # Web framework
uvicorn==0.38.0           # ASGI server
sqlalchemy==2.0.45        # ORM
alembic==1.17.2           # Database migrations
psycopg2-binary==2.9.11   # PostgreSQL adapter
python-dotenv==1.2.1      # Environment variable management
```

Additional transitive dependencies are automatically installed.

---

## 🔒 Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:port/database
```

Required for both local development and production deployment.

---

## 👤 Author

**Ricky Laikhuram**

Built as part of the **Full Stack Engineer Assessment**, demonstrating real-world backend design patterns for webhook-based systems.

