from fastapi import FastAPI
from app.routes import health, webhooks, transactions
from app.core.database import engine
from app.models.transaction import Transaction

app = FastAPI()

Transaction.metadata.create_all(bind=engine)

app.include_router(health.router, tags=["Health"])
app.include_router(webhooks.router, prefix="/v1", tags=["Webhooks"])
app.include_router(transactions.router, prefix="/v1", tags=["Transactions"])
