from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import func
class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = "wallets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    initial_saldo: Mapped[float] = mapped_column(Float, default=0.0)
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="wallet", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Wallet(id={self.id!r}, name={self.name!r})"


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    transaction_type: Mapped[str] = mapped_column(String(30))
    wallet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wallets.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    wallet: Mapped["Wallet"] = relationship(back_populates="transactions")

    def __repr__(self) -> str:
        return f"Transaction(id={self.id!r}, amount={self.amount!r}, type={self.transaction_type!r})"
