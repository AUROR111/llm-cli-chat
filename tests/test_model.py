from src.bookkeeping.models import Transaction
from datetime import datetime

t= Transaction(
    id=1,
    amount=100.0,
    category="Food",
    note="Lunch",
    created_at=datetime.now(),
    updated_at=datetime.now()
)
print(t)
print(t.model_dump())