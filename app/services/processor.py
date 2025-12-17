import time
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import update  # Add this import

from app.models.transaction import Transaction

def process_transaction(db: Session, transaction_id: str):
    try:
        time.sleep(30)  # Simulate processing
        
        result = db.execute(
            update(Transaction)
            .where(
                Transaction.transaction_id == transaction_id,
                Transaction.status == "PROCESSING"
            )
            .values(
                status="PROCESSED",
                processed_at=datetime.now(timezone.utc)
            )
        )
        
        db.commit()
        
        return result.rowcount > 0  
 
    except Exception as e:
        db.rollback()
        raise