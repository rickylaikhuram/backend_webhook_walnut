from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime,timezone
from app.core.database import Base
import uuid

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(String, unique=True, nullable=False, index=True)
    source_account = Column(String, nullable=False)
    destination_account = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)

    status = Column(String, default="PROCESSING")

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    processed_at = Column(DateTime, nullable=True)
