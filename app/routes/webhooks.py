from fastapi import APIRouter, BackgroundTasks, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.transaction import TransactionCreate
from app.models.transaction import Transaction
from app.core.database import SessionLocal
from app.services.processor import process_transaction

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/webhooks/transactions",
    status_code=status.HTTP_202_ACCEPTED
)
async def receive_webhook(
    payload: TransactionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    transaction = Transaction(
        transaction_id=payload.transaction_id,
        source_account=payload.source_account,
        destination_account=payload.destination_account,
        amount=payload.amount,
        currency=payload.currency,
        status="PROCESSING",
    )

    try:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
    except IntegrityError:
        # Duplicate webhook if already exists
        db.rollback()
        return {"message": "Transaction already exists", "transaction_id": payload.transaction_id}

    # Trigger background processing
    background_tasks.add_task(
        process_transaction,
        db,
        payload.transaction_id
    )

    return {
        "message": "Transaction added successfully",
        "transaction_id": payload.transaction_id,
        "status": "PROCESSING"
    }

