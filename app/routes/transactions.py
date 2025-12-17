from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.transaction import Transaction

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/transactions/{transaction_id}")
def get_transaction_status(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.transaction_id == transaction_id)
        .first()
    )

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {
        "transaction_id": transaction.transaction_id,
        "source_account": transaction.source_account,
        "destination_account": transaction.destination_account,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "status": transaction.status,
        "created_at": transaction.created_at,
        "processed_at": transaction.processed_at,
    }
