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

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy**
* **Uvicorn**

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

## 🧪 Running Locally

### 1. Clone the repository

```bash
git clone <repo-url>
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate (Windows Powershell in VS-Code)
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variable

```bash
export DATABASE_URL=postgresql://user:password@localhost:5432/webhooks_db
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

---

## ✅ Testing Scenarios

1. **Single Webhook**
   * Send one webhook
   * Verify status changes from `PROCESSING` → `PROCESSED` after ~30 seconds

2. **Duplicate Webhook**
   * Send the same webhook multiple times
   * Only one transaction is stored and processed

3. **Performance**
   * Webhook endpoint responds immediately under load

---

## 🧠 Design Decisions

* **FastAPI BackgroundTasks** were used for simplicity and reliability
* Database uniqueness guarantees idempotency
* Webhook endpoint never fails to avoid retry storms
* Clean separation between routing, business logic, and persistence

---

## 🚀 Deployment

The service can be deployed on any cloud platform that supports Python and PostgreSQL. A live instance is currently running on Render.

---

## 👤 Author

**Ricky Laikhuram**.

Built as part of the **Full Stack Engineer Assessment** , demonstrating real-world backend design patterns for webhook-based systems.
